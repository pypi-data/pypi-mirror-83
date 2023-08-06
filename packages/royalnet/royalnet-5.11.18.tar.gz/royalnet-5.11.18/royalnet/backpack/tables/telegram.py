from sqlalchemy import Column, \
    Integer, \
    String, \
    BigInteger, \
    ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

# noinspection PyUnresolvedReferences
from .users import User


class Telegram:
    __tablename__ = "telegram"

    @declared_attr
    def user_id(self):
        return Column(Integer, ForeignKey("users.uid"), nullable=False)

    @declared_attr
    def user(self):
        return relationship("User", backref="telegram")

    @declared_attr
    def tg_id(self):
        return Column(BigInteger, primary_key=True)

    @declared_attr
    def first_name(self):
        return Column(String)

    @declared_attr
    def last_name(self):
        return Column(String)

    @declared_attr
    def username(self):
        return Column(String)

    def __repr__(self):
        return f"<Telegram {str(self)}>"

    def __str__(self):
        return f"[c]telegram:{self.mention()}[/c]"

    def name(self) -> str:
        if self.username is not None:
            return f"{self.username}"
        elif self.last_name is not None:
            return f"{self.first_name} {self.last_name}"
        else:
            return f"{self.first_name}"

    def mention(self) -> str:
        if self.username is not None:
            return f"@{self.username}"
        elif self.last_name is not None:
            return f"[url=tg://user?id={self.tg_id}]{self.first_name} {self.last_name}[/url]"
        else:
            return f"[url=tg://user?id={self.tg_id}]{self.first_name}[/url]"
