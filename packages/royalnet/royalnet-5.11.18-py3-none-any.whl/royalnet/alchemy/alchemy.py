import contextlib
import logging
from typing import *

from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.schema import Table

from royalnet.alchemy.errors import TableNotFoundError
from royalnet.utils import asyncify

if TYPE_CHECKING:
    # noinspection PyProtectedMember
    from sqlalchemy.engine import Engine

log = logging.getLogger(__name__)


class Alchemy:
    """A wrapper around :mod:`sqlalchemy.orm` that allows the instantiation of multiple engines at once while
    maintaining a single declarative class for all of them."""

    def __init__(self, database_uri: str, tables: Set):
        """Create a new :class:`.Alchemy` object.

        Args:
            database_uri: The `database URI <https://docs.sqlalchemy.org/en/13/core/engines.html>`_  .
            tables: The :class:`set` of tables to be created and used in the selected database.
                    Check the tables submodule for more details.
        """
        if database_uri.startswith("sqlite"):
            raise NotImplementedError("sqlite databases aren't supported, as they can't be used in multithreaded"
                                      " applications")
        self._engine: "Engine" = create_engine(database_uri)
        self._Base = declarative_base(bind=self._engine)
        self.Session: sessionmaker = sessionmaker(bind=self._engine)
        self._tables: Dict[str, Table] = {}
        for table in tables:
            name = table.__name__
            assert self._tables.get(name) is None
            assert isinstance(name, str)
            # noinspection PyTypeChecker
            bound_table: Table = type(name, (self._Base, table), {})
            self._tables[name] = bound_table
        # FIXME: Dirty hack
        try:
            self._Base.metadata.create_all()
        except ProgrammingError:
            log.warning("Skipping table creation, as it is probably being created by a different process.")

    def get(self, table: Union[str, type]) -> Any:
        """Get the table with a specified name or class.

        Args:
            table: The table name or table class you want to get.

        Raises:
            TableNotFoundError: if the requested table was not found."""
        if isinstance(table, str):
            result = self._tables.get(table)
            if result is None:
                raise TableNotFoundError(f"Table '{table}' isn't present in this Alchemy instance")
            return result
        elif isinstance(table, type):
            name = table.__name__
            result = self._tables.get(name)
            if result is None:
                raise TableNotFoundError(f"Table '{table}' isn't present in this Alchemy instance")
            return result
        else:
            raise TypeError(f"Can't get tables with objects of type '{table.__class__.__qualname__}'")

    @contextlib.contextmanager
    def session_cm(self) -> Iterator[Session]:
        """Create a Session as a context manager (that can be used in ``with`` statements).

        The Session will be closed safely when the context manager exits (even in case of error).

        Example:
            You can use the context manager like this: ::

                with alchemy.session_cm() as session:
                    # Do some stuff
                    ...
                    # Commit the session
                    session.commit()

        """
        session = self.Session()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @contextlib.asynccontextmanager
    async def session_acm(self) -> AsyncIterator[Session]:
        """Create a Session as a async context manager (that can be used in ``async with`` statements).

        The Session will be closed safely when the context manager exits (even in case of error).

        Example:
            You can use the async context manager like this: ::

                async with alchemy.session_acm() as session:
                    # Do some stuff
                    ...
                    # Commit the session
                    await asyncify(session.commit)"""
        session = await asyncify(self.Session)
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
