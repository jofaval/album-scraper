from argparse import ArgumentParser


def init_args() -> ArgumentParser:
    """Initialize args"""
    parser = ArgumentParser()

    parser.add_argument("--module_name", help="Do the bar option")
    parser.add_argument("--foo", help="Foo the program")

    return parser
    # args = parser.parse_args()
