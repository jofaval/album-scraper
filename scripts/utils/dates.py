"""
Date utilities
"""

# dates
from datetime import datetime


def get_now_as_str(date_format: str = '%Y-%m-%d_%H-%M-%S') -> str:
    """
    Creates a string from the current timestamp

    date_format : str
        The date format, `%Y-%m-%d_%H-%M-%S` by default

    return str
    """
    return datetime.now().strftime(date_format)
