"""
This module helps with translation,
specifically the CLI's translations,
a simplified version of the scripts
"""

# types
from typing import Dict, Union
# a simpler and "far nicer" version of a "translator"
from .es import STRINGS as esLangs
from .en import STRINGS as enLangs

LANGS: Dict[str, Dict[str, str]] = {
    'ES': esLangs,
    'EN': enLangs,
}

CURRENT_LANG = 'ES'
STRINGS = LANGS[CURRENT_LANG]


def t(key: str) -> Union[str, None]:
    """
    Translate a string

    key : str
        The key to translate

    return str
    """
    if key not in STRINGS:
        return

    return STRINGS[key]
