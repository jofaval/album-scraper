"""
Number utilities
"""


def pad(number: int, padding: int = 3) -> str:
    """Pads to the left a number"""
    return str(number).zfill(padding)
