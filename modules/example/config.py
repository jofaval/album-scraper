"""
Example module config
"""

# system
from os.path import dirname, realpath
# types
from scripts.config.type import ConfigType


CONFIG: ConfigType = {
    'DOMAIN': 'https://example.com',
    'BASE_URL': 'https://example.com',
    'PARSER': 'html.parser',

    'CHAPTER_IMG_QUERY': ','.join([
        '.article__img',
        '.other-class img',
    ]),
    'CHAPTERS_FOLDER': 'chapters',
    'CHAPTERS_QUERY': '#chapters > li > a',

    'EXTRA_TITLE_CONTENT': '/chapters/',
    'FILE_EXTENSION': '.jpg',

    'SHOULD_RENAME_IMAGES': True,
    'BASE_DIR': dirname(realpath(__file__)).replace('example_with_spaces', 'Example with spaces'),
}
