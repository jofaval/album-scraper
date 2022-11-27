# a simpler and "far nicer" version of a "translator"
from .es import STRINGS as esLangs
from .en import STRINGS as enLangs
# types
from typing import Dict

LANGS: Dict[str, Dict[str, str]] = {
    'ES': esLangs,
    'EN': enLangs,
}

CURRENT_LANG = 'ES'
STRINGS = LANGS[CURRENT_LANG]


def t(key: str) -> str or None:
    """
    Translate a string

    key : str
        The key to translate

    return str
    """
    if key not in STRINGS:
        return

    return STRINGS[key]
