"""
Example config
"""

# system
from os.path import dirname, realpath
# types
from scripts.config.type import ConfigType


CONFIG: ConfigType = {
    'DOMAIN': 'https://',
    'BASE_URL': 'https://',  # [https]domain.com/special-album
    'PARSER': 'html.parser',

    'CHAPTER_IMG_QUERY': 'main img',
    'CHAPTERS_FOLDER': 'chapters',
    'CHAPTERS_QUERY': 'a.chapter-name',

    'EXTRA_TITLE_CONTENT': '/chapter/',
    'FILE_EXTENSION': '.jpg',

    'SHOULD_RENAME_IMAGES': True,
    'BASE_DIR': dirname(realpath(__file__)).replace('serpent_case', 'Real name of the Album'),

    'IMG_SRC_ATTRIBUTE': 'src',
}
