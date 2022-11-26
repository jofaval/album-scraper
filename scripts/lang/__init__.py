from .es import STRINGS as esLangs
from functools import reduce
from typing import TypedDict, Dict


LANGS: Dict[str, str] = {
    'ES': esLangs
}


class OptionsDict(TypedDict):
    separator: str
    """The key separator for the translation strings"""


DEFAULT_SEPARATOR: str = '.'
DEFAULT_OPTIONS: OptionsDict = {
    "separator": DEFAULT_SEPARATOR
}
CURRENT_LANG: str = 'ES'

# fake implementation
# TODO: use a stronger type system for the langs?


def get_translation_key(key: str, strings: dict, separator: str = DEFAULT_SEPARATOR) -> str:
    """
    Gets the actual key from the dict

    key : str
        Gets the actual key, "recursively" if needed, probably just reducing
        - example: "ERRORS.GET_PAGE"
    strings : dict
        The dictionary with all the strings
    separator : str
        The separator to use, a point by default

    return str
    """
    return reduce(lambda strings_dict, k: strings_dict[k], key.split(separator), strings)


def translate(key: str, params: dict = {}, options: OptionsDict = DEFAULT_OPTIONS) -> str:
    """
    Translates a string, with params

    key : str
        The key of the string to translate
    params : dict = {}
        The params or variables of the string to translate, direct match

    return str
    """
    current_strings = LANGS[CURRENT_LANG]

    real_key = get_translation_key(
        key=key.upper(),
        strings=current_strings,
        separator=options['separator']
    )

    # apply params
    raw_string = real_key
    for key, value in params.items():
        raw_string = raw_string.replace('{{' + key + '}}', str(value))

    return raw_string


def t(key: str, params: dict = {}, options: OptionsDict = DEFAULT_OPTIONS) -> str:
    """
    Translates a string, with params

    key : str
        The key of the string to translate
    params : dict = {}
        The params or variables of the string to translate, direct match

    return str
    """
    return translate(key, params, options)
