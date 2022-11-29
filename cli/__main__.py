"""
Main CLI execution entrypoint,
calling this file will provide the CLI experience
"""

from argparse import ArgumentParser

from .create_module import init_args as create_module_args


def init() -> ArgumentParser:
    """Initialize args"""
    parser = ArgumentParser()

    # main args

    return parser


def main() -> None:
    """Main flow of execution for the CLI"""
    parser = init()
    parser = create_module_args(parser)

    args = parser.parse_args()


if __name__ == '__main__':
    main()
