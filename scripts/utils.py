from os import name as os_name, system as cmd, makedirs
from os.path import exists
from datetime import datetime


def cls() -> None:
    """Clears the console"""
    cmd('cls' if os_name == 'nt' else 'clear')


def check_folder_or_create(path: str) -> bool:
    """
    Creates a folder if it doesn't exist

    path : str
        The filename path

    return bool
    """
    if not exists(path):
        makedirs(path)


def get_now_as_str(format: str = '%Y-%m-%d_%H-%M-%S') -> str:
    """
    Creates a string from the current timestamp

    format : str
        The date format, `%Y-%m-%d_%H-%M-%S` by default

    return str
    """
    return datetime.now().strftime(format)
