import re
import typing


def andformat(coll: typing.Collection[str], middle=", ", final=" and ") -> str:
    """Convert a collection (such as a :class:`list`) to a :class:`str` by adding ``final`` between the last two
    elements and ``middle`` between the others.

    Args:
        coll: the input collection.
        middle: the :class:`str` to be added between the middle elements.
        final: the :class:`str` to be added between the last two elements.

    Returns:
        The resulting :py:class:`str`.

    Examples:
        ::

            >>> andformat(["Steffo", "Kappa", "Proto"])
            "Steffo, Kappa and Proto"

            >>> andformat(["Viktya", "Sensei", "Cate"], final=" e ")
            "Viktya, Sensei e Cate"

            >>> andformat(["Paltri", "Spaggia", "Gesù", "Mallllco"], middle="+", final="+")
            "Paltri+Spaggia+Gesù+Mallllco"
    """
    result = ""
    for index, item in enumerate(coll):
        result += item
        if index == len(coll) - 2:
            result += final
        elif index != len(coll) - 1:
            result += middle
    return result


def underscorize(string: str) -> str:
    """Replace all non-word characters in a :class:`str` with underscores.

    It is particularly useful when you want to use random strings from the Internet as filenames.
    
    Parameters:
        string: the input string.
    
    Returns:
        The resulting string.

    Example:
        ::

            >>> underscorize("LE EPIC PRANK [GONE WRONG!?!?]")
            "LE_EPIC_PRANK__GONE_WRONG_____"

    """
    return re.sub(r"\W", "_", string)


def ytdldateformat(string: typing.Optional[str], separator: str = "-") -> str:
    """Convert the date :class:`str` returned by `youtube_dl <https://ytdl-org.github.io/youtube-dl/index.html>`_  into
     the ``YYYY-MM-DD`` format.
    
    Parameters:
        string: the input :class:`str`, in the ``YYYYMMDD`` format used by youtube_dl.
        separator: the :class:`str` to add between the years, the months and the days. Defaults to ``"-"``.
        
    Returns:
        The resulting :class:`str` in the new format.

    Example:
        ::

            >>> ytdldateformat("20111111")
            "2011-11-11"

            >>> ytdldateformat("20200202", separator=".")
            "2020.02.02"

    """
    if string is None:
        return ""
    return f"{string[0:4]}{separator}{string[4:6]}{separator}{string[6:8]}"


def numberemojiformat(li: typing.Collection[str]) -> str:
    """Convert a collection to a string with one item on every line numbered with emojis.

    Parameters:
        li: the list to convert.

    Returns:
        The resulting Unicode string.

    Examples:
        Cannot be displayed, as Sphinx does not render emojis properly.
    """
    number_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    extra_emoji = "*️⃣"
    result = ""
    for index, element in enumerate(li):
        try:
            result += f"{number_emojis[index]} {element}\n"
        except IndexError:
            result += f"{extra_emoji} {element}\n"
    return result


def ordinalformat(number: int) -> str:
    """Convert a :class:`int` to the corresponding English ordinal :class:`str`.

    Parameters:
        number: the number to convert.

    Returns:
        The corresponding English `ordinal numeral <https://en.wikipedia.org/wiki/Ordinal_numeral>`_.

    Examples:
        ::

            >>> ordinalformat(1)
            "1st"
            >>> ordinalformat(2)
            "2nd"
            >>> ordinalformat(11)
            "11th"
            >>> ordinalformat(101)
            "101st"
            >>> ordinalformat(112)
            "112th"
            >>> ordinalformat(0)
            "0th"
    """
    if 10 <= number % 100 < 20:
        return f"{number}th"
    if number % 10 == 1:
        return f"{number}st"
    elif number % 10 == 2:
        return f"{number}nd"
    elif number % 10 == 3:
        return f"{number}rd"
    return f"{number}th"
