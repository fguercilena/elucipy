from collections import namedtuple
from regex import compile, MULTILINE, VERBOSE, VERSION1


_REGEX_FLAGS = VERBOSE | VERSION1 | MULTILINE


Language = namedtuple("Language", ("elucipy_regex", "elucipy_trash",
                                   "header", "header_trash",
                                   "explanation", "explanation_trash",
                                   "tabsize"))

LANGUAGES = {}


###############################################################################
# Python
###############################################################################

_LITERAL_STRINGS = r"""
    (  # Start group 1 encompassing the entire expression
    '''(?:[^']|\\')*'''(*SKIP)(*FAIL)        # ''' string literal, ignored
    |
    '(?:[^']|\\')*'(*SKIP)(*FAIL)            # ' string literal, ignored
    |
    \"\"\"(?:[^"]|\\")*\"\"\"(*SKIP)(*FAIL)  # ""\" string literal, ignored
    |
    "(?:[^"]|\\")*"(*SKIP)(*FAIL)            # " string literal, ignored
    |
    """

_ELUCIPY_REGEX = compile(_LITERAL_STRINGS + r"""
    ^\#\ elucipy{([^}]*)}{([^}]*)}\n*
    ) # End group 1
    """, flags=_REGEX_FLAGS)

_ELUCIPY_TRASH = compile(r"^[\ \t]*\#\ |[\ \t]*$", flags=_REGEX_FLAGS)

_HEADER = compile(_LITERAL_STRINGS + r"""
    ^([\ \t]*)(\#{2,})\n^\2\#\ [^\n]*\n^\2\3\n\n*
    ) # End group 1
    """, flags=_REGEX_FLAGS)

_HEADER_TRASH = compile(r"""
        ^[\ \t]*\#+[\ \t]*
        |
        [\ \t]*\#*[\ \t]*$\n*
        """, flags=_REGEX_FLAGS)

_EXPLANATION = compile(_LITERAL_STRINGS + r"""
    (?:^[\ \t]*\#\ [^\n]*\n)+\n*
    ) # End group 1
    """, flags=_REGEX_FLAGS)

_EXPLANATION_trash = compile(r"""
        ^[\ \t]*\#[\ \t]*
        |
        [\ \t]*$
        |
        \n*\Z
        """, flags=_REGEX_FLAGS)

_PYTHON = Language(_ELUCIPY_REGEX, _ELUCIPY_TRASH, _HEADER, _HEADER_TRASH,
                   _EXPLANATION, _EXPLANATION_trash, 4)

LANGUAGES["python"] = _PYTHON
LANGUAGES["numpy"] = _PYTHON


###############################################################################
# Fortran
###############################################################################

_LITERAL_STRINGS = r"""
    (  # Start group 1 encompassing the entire expression
    '(?:[^']|\\')*'(*SKIP)(*FAIL)            # ' string literal, ignored
    |
    "(?:[^"]|\\")*"(*SKIP)(*FAIL)            # " string literal, ignored
    |
    """

_ELUCIPY_REGEX = compile(_LITERAL_STRINGS + r"""
    ^!\ elucipy{([^}]*)}{([^}]*)}\n*
    ) # End group 1
    """, flags=_REGEX_FLAGS)

_ELUCIPY_TRASH = compile(r"^[\ \t]*!\ |[\ \t]*$", flags=_REGEX_FLAGS)

_HEADER = compile(_LITERAL_STRINGS + r"""
    ^([\ \t]*)(!{2,})\n^\2!\ [^\n]*\n^\2\3\n\n*
    ) # End group 1
    """, flags=_REGEX_FLAGS)

_HEADER_TRASH = compile(r"""
        ^[\ \t]*!+[\ \t]*
        |
        [\ \t]*!*[\ \t]*$
        """, flags=_REGEX_FLAGS)

_EXPLANATION = compile(_LITERAL_STRINGS + r"""
    (?:^[\ \t]*!\ [^\n]*\n)+\n*
    ) # End group 1
    """, flags=_REGEX_FLAGS)

_EXPLANATION_trash = compile(r"""
        ^[\ \t]*![\ \t]*
        |
        [\ \t]*$
        |
        \n*\Z
        """, flags=_REGEX_FLAGS)

_FORTRAN = Language(_ELUCIPY_REGEX, _ELUCIPY_TRASH, _HEADER, _HEADER_TRASH,
                    _EXPLANATION, _EXPLANATION_trash, 3)

LANGUAGES["fortran"] = _FORTRAN


###############################################################################
# C/C++/Objective-C/Objective-C++
###############################################################################

_LITERAL_STRINGS = r"""
    (  # Start group 1 encompassing the entire expression
    '(?:[^']|\\')*'(*SKIP)(*FAIL)            # ' string literal, ignored
    |
    "(?:[^"]|\\")*"(*SKIP)(*FAIL)            # " string literal, ignored
    |
    """

_ELUCIPY_REGEX = compile(_LITERAL_STRINGS + r"""
    ^//\ elucipy{([^}]*)}{([^}]*)}\n*
    ) # End group 1
    """, flags=_REGEX_FLAGS)

_ELUCIPY_TRASH = compile(r"^[\ \t]*/{2,}\ |[\ \t]*$", flags=_REGEX_FLAGS)

_HEADER = compile(_LITERAL_STRINGS + r"""
    ^([\ \t]*)(/{3,})\n^\2//\ [^\n]*\n^\2\3\n\n*
    ) # End group 1
    """, flags=_REGEX_FLAGS)

_HEADER_TRASH = compile(r"""
        ^[\ \t]*/+[\ \t]*
        |
        [\ \t]*/*[\ \t]*$
        """, flags=_REGEX_FLAGS)

_EXPLANATION = compile(_LITERAL_STRINGS + r"""
    (?:^[\ \t]*//\ [^\n]*\n)+\n*
    ) # End group 1
    """, flags=_REGEX_FLAGS)

_EXPLANATION_trash = compile(r"""
        ^[\ \t]*//[\ \t]*
        |
        [\ \t]*$
        |
        \n*\Z
        """, flags=_REGEX_FLAGS)

_CLANGS = Language(_ELUCIPY_REGEX, _ELUCIPY_TRASH, _HEADER, _HEADER_TRASH,
                   _EXPLANATION, _EXPLANATION_trash, 4)

LANGUAGES["c"] = _CLANGS
LANGUAGES["c++"] = _CLANGS
LANGUAGES["objective-c"] = _CLANGS
LANGUAGES["objective-c++"] = _CLANGS
