# vendor
from argparse import ArgumentParser
# multilang
from .lang import t


def init_args(parser: ArgumentParser):
    """Initialize args"""
    parser.add_argument(
        "--module_name",
        help=t('CREATE_MODULE.ARGS.MODULE_NAME.DESCRIPTIONS'),
        type=str,
        # remove if more options (create module, delete, download via script)
        required=True,
    )

    return parser
