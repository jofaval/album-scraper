# types
from ..config.type import ConfigType
# constants
from ..constants import EVERYTHING


DEFAULT_CONFIG: ConfigType = {
    'DOMAIN': 'https://example.com/',
    'BASE_URL': 'https://example.com/',
    'PARSER': 'html.parser',
    'URL_SEPARATOR': '/',

    'CHAPTER_IMG_QUERY': '.entry-inner .entry-content p img',
    'CHAPTERS_FOLDER': 'chapters',
    'CHAPTERS_QUERY': '#Chapters_List li a',

    'EXTRA_TITLE_CONTENT': '/images/',
    'FILE_EXTENSION': '.jpg',
    'LOG_EXTENSION': '.log.txt',

    'SHOULD_RENAME_IMAGES': True,

    'THREADS': [],
    'LIMIT_THREADS': 10,

    'SEPARATOR': '.',
    'EVERYTHING': EVERYTHING,
    'IMG_SRC_ATTRIBUTE': 'src',

    'LOGS_FOLDER': 'logs'
}
