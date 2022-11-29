# dates
from datetime import datetime


def get_now_as_str(format: str = '%Y-%m-%d_%H-%M-%S') -> str:
    """
    Creates a string from the current timestamp

    format : str
        The date format, `%Y-%m-%d_%H-%M-%S` by default

    return str
    """
    return datetime.now().strftime(format)
