# -*- coding: utf-8 -*-

"""
:platform: Mac, Unix, Windows, python 2.7, 3.4+
:synopsis: A module for unpacking basic data objects from a text string.

Author  - Jens B. Helmers
Created - 2020-10-23
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from distutils.util import strtobool

__all__ = ["Unpack", "unpack"]


def _bool(s):
    """Convert a string representation of truth to True or False.
    Same as distutils.util.strtobool but the result is True or False not 1 or 0.

    Parameters
    ----------
    s : str
        Input text element representing True or False

    Returns
    -------
    bool
        True/False representation of s.
        True if s.lower() = "y", "yes", "t", "true", "on" and "1"
        False if s.lower() = "n", "no", "f", "false", "off" and "0"

    Raises
    ------
    ValueError
        If s.lower() does not match True or False criteria.

    """
    return bool(strtobool(s))


def unpack(fmt, text, *args, **kwargs):
    """Extract basic data types from text based on fmt.

    Parameters
    ----------
    fmt : str
        fmt[i] defines the type of item i in the output tuple.
        fmt[i] must be 'i', 'f', 's', '?' or '.'. Item i will be ignored if fmt[i]=='.'.
    text : str
        The text string to extract the objects from

    Other Parameters
    ----------------
    *args : list, optional
        Additional variable length argument list to be submitted to the constructor of Unpack
    **kwargs : dict, optional
        Additional keyword arguments to be submitted to the constructor of Unpack

    Returns
    -------
    tuple
        The tuple of objects parsed from text.

    Raises
    ------
    ValueError
        If any parsing error occur.

    Examples
    --------

    >>> unpack("ifs?", "5 2.3   ole  True")
    (5, 2.3, 'ole', True)
    >>> unpack("isf", "100 'Donald Duck' 125.6", quote="'")
    (100, 'Donald Duck', 125.6)

    """
    try:
        return Unpack(fmt, *args, **kwargs)(text)
    except Exception as e:
        msg = "strup.unpack()\nfmt=%s\ntext=%s\nargv=%s, kwargs=%s\n%s" % (
            repr(fmt),
            repr(text),
            args,
            kwargs,
            e,
        )
        raise ValueError(msg)


class Unpack:
    """
    Unpack is a Python package for unpacking basic data types from a text string.

    Each item is of type 'int', 'float', 'string' or 'bool' depending on a format code
    in the constructor.
    """

    def __init__(self, fmt, sep=None, none=False, quote=None, quote_escape=None):
        """Constructor for Unpack.

        Parameters
        ----------
        fmt : str
            fmt[i] defines the type of item i in the output tuple.
            fmt[i] must be 'i', 'f', 's', '?' or '.'. Item i will be ignored if fmt[i]=='.'.
        sep : str or None, optional
            String to separate items. See string.split() method.
        none : bool, optional
            If True: Zero-sized items are interpreted as None.
        quote : str or None, optional
            String items are sometimes enclosed by quote characters.
            Quotes are mandatory if string items includes the sep or
            quote characters. A quote character inside an item must be
            escaped by 'quote_escape'. (See example below). It is not
            possible to apply quotes if quote==''.
        quote_escape : str or None, optional
            Typical values are '""', "''", r'\"' or "\'".
            quote_escape = None is interpreted as quote_escape = quote*2

        Raises
        ------
        ValueError
            If any parsing error occur.

        Examples
        --------

        See the __call__() examples for application of these decoders:

        >>> decode1 = Unpack('ifssis')
        >>> decode2 = Unpack('.fs', sep=',')
        >>> decode3 = Unpack('isfs', sep=' ', quote='"', quote_escape='""')

        """
        self._white = " \t\n\r"
        self._none = none
        if sep == "":
            raise ValueError("sep can not be empty.")
        if quote is not None:
            if not (quote in ['"', "'"]):
                raise ValueError("quote character must %s or %s" % ('"', "'"))
            if not (quote_escape in [None, '""', "''", r"\"", r"\'"]):
                raise ValueError(
                    "quote_escape character should be None, %s, %s, %s or %s"
                    % ('""', "''", r"\"", r"\'")
                )
            if quote == sep:
                raise ValueError("quote character must differ from sep character")
        for char in fmt:
            if char not in ".ifs?":
                raise ValueError(
                    "All characters in fmt must be 'i', 'f', 's', '?' or '.' fmt=%s"
                    % fmt
                )
        if fmt[-1] == ".":
            raise ValueError("Trailing dots should not be present in fmt=%s" % fmt)
        typ = {"i": int, "f": float, "s": str, "?": _bool}
        self._fmt = fmt
        self._nitems = len(fmt)
        self._items = []
        self._sep = sep
        self._quote = quote
        if quote_escape is None and quote:
            self._quote_escape = quote + quote
        else:
            self._quote_escape = quote_escape
        for pos, item in enumerate(fmt):
            if item != ".":
                self._items.append((pos, typ[item]))

    def _item_inside_quote(self, start, text):
        """
        Return string item located inside quotes. text[start]==self._quote.
        """
        pos = start
        while True:
            pos += 1
            if text[pos:].startswith(self._quote_escape):
                pos += 1
            elif text[pos] == self._quote:
                break
        item = text[start + 1 : pos].replace(self._quote_escape, self._quote)
        return pos + 1, item

    def __call__(self, text):
        """Extract the tuple of objects by parsing text based on self._fmt

        Parameters
        ----------
        text : str
            The text string to extract the objects from

        Returns
        -------
        tuple
            The tuple of objects parsed from text.

        Raises
        ------
        ValueError
            If any parsing error occur.

        Examples
        --------

        decode1, decode2 and decode3 as defined in the  __init__() examples:

        >>> decode1("3 4.5  ole dole 5 doffen")
        (3, 4.5, 'ole', 'dole', 5, 'doffen')
        >>> decode2("3,4.5,  ole,dole,5,doffen")
        (4.5, '  ole')
        >>> decode3('3 "A ""quote"" test" 93.4 knut ignored')
        (3, 'A "quote" test', 93.4, 'knut')

        """
        if self._quote is None:
            # Strings can not be quoted. Efficient method applied.
            items = text.split(self._sep, self._nitems)
            # note: len(items) == self._nitems + 1 in case of trailing data.
        else:
            items = []
            pos = 0
            if self._sep is None:
                # items are separated by one or more 'white' characters.
                for _i in range(self._nitems):
                    while text[pos] in self._white:
                        pos += 1
                    if text[pos] == self._quote:
                        # Quoted strings may include self._sep
                        pos, item = self._item_inside_quote(pos, text)
                    else:
                        start = pos
                        pos += 1
                        try:
                            while text[pos] not in self._white:
                                pos += 1
                        except IndexError:
                            pos = len(text)
                        item = text[start:pos]
                    items.append(item)
            else:
                # items are separated by self._sep...
                lensep = len(self._sep)
                posmax = len(text) - 1
                for _i in range(self._nitems):
                    if text[pos:].startswith(self._sep):
                        item = ""
                    elif text[pos] == self._quote:
                        # Quoted strings may include self._sep
                        pos, item = self._item_inside_quote(pos, text)
                    else:
                        start = pos
                        try:
                            pos = text.index(self._sep, pos)
                        except ValueError:
                            pos = len(text)
                        item = text[start:pos]
                    items.append(item)
                    if pos < posmax:
                        pos += lensep
        res = []
        for pos, typ in self._items:
            if self._none and items[pos] == "":
                res.append(None)
            else:
                try:
                    res.append(typ(items[pos]))
                except ValueError:
                    raise ValueError(
                        "Error decoding element %i:%s of items=%s"
                        % (pos, repr(items[pos]), repr(items[: self._nitems]))
                    )

        return tuple(res)
