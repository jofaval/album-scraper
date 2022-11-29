# system
from os import listdir
from os.path import isfile, join as join_paths, dirname, realpath, getsize
import cchardet  # only needs to be imported, not used
# types
from typing import List


# local

# constants
from .constants import END_OF_LINE, EVERYTHING
# types
from .config.type import ConfigType
from .models.album_types import ScrapeProps
# custom translator
from .lang import t
# utils
from .utils import check_folder_or_create, cls
from .logger import Logger
# config
from .config.default import DEFAULT_CONFIG


# |---------------------------|
# |         CONSTANTS         |
# |---------------------------|

DEBUG = True

CONF: ConfigType = {
    **DEFAULT_CONFIG,
    'BASE_DIR': dirname(realpath(__file__))
}
SHOULD_LOG = True

LOGGER_INSTANCE: Logger = None


def detect_missing_imgs(stacktrace: bool = True):
    LOGGER_INSTANCE.log(t('CHAPTERS.CORRUPT_CHAPTERS_DETECTION'))
    incomplete_chapters = []

    chapters_path = join_paths(CONF['BASE_DIR'], CONF['CHAPTERS_FOLDER'])
    dir_elements = listdir(chapters_path)
    chapters = [elem for elem in dir_elements if not isfile(elem)]

    for chapter in chapters:
        LOGGER_INSTANCE.log(t('IMAGES.ANALYZING_IMAGES', {'chapter': chapter}))

        chapter_path = join_paths(chapters_path, chapter)
        chapter_elements = listdir(chapter_path)
        imgs = [img.split(CONF['SEPARATOR'])[0] for img in chapter_elements]

        new_imgs = []
        for img in imgs:
            if '-' not in img:
                new_imgs.append(img)
                continue

            # edge case, there might be some sort of dash to filter from
            try:
                new_imgs.append(int(img.split('-')[-1]))
            except:
                LOGGER_INSTANCE.log(t('ERRORS.PARSE_ERROR'))
        imgs = new_imgs

        imgs.sort()

        if not imgs:
            incomplete_chapters.append(chapter)
            continue

        for index, img in enumerate(imgs):
            try:
                filesize = getsize(
                    join_paths(chapter_path, str(img) + CONF['FILE_EXTENSION']))
            except:
                filesize = 0
            if (not int(img) == (index + 1)) | (not filesize > 0):
                if stacktrace:
                    LOGGER_INSTANCE.log(t('ERRORS.CORRPUT_IMAGE_FOUND', {
                        'chapter': chapter,
                        'index': (index + 1),
                        'extension': CONF['FILE_EXTENSION'],
                        'filesize': filesize,
                    }))
                incomplete_chapters.append(chapter)
                break

    return incomplete_chapters


def detect_updates(chapters: List[str] = None):
    downloaded_chapters = listdir(join_paths(
        CONF['BASE_DIR'], CONF['CHAPTERS_FOLDER']
    ))

    if chapters is None:
        chapters = get_chapters()

    not_downloaded = []
    for chapter in chapters:
        found = False

        for download in downloaded_chapters:
            if download in chapter:
                found = True
                break

        if not found:
            not_downloaded.append(chapter)

    return not_downloaded


def download_updates():
    updates = detect_updates()

    LOGGER_INSTANCE.log(t('UPDATES.NEWS_ARE', {'updates': updates}))

    prompt = t('UPDATES.DOWNLOAD_PROMPT')
    option = input(prompt)

    LOGGER_INSTANCE.log(t('UPDATES.CHOSEN_OPTION', {'option': option}))

    if option.lower() not in ['s', 'y']:
        return LOGGER_INSTANCE.log(t('UPDATES.NOT_DOWNLOADING_NEWS'))

    scrape(chapter_links=updates, detect_corrupt=False)

    LOGGER_INSTANCE.log(t('UPDATES.NEWS_DOWNLOADED'))


def set_configuration(configuration: ConfigType) -> None:
    """
    Sets the configuration values to use

    configuration : ConfigType
        The dictionary object of key, values

    returns None
    """
    for key, value in configuration.items():
        CONF[key] = value


def start(conf: ConfigType, props: ScrapeProps) -> None:
    """Starts all the processes"""
    global LOGGER_INSTANCE

    set_configuration(conf)

    default_scrape_props: ScrapeProps = {
        'chapter_links': None,
        'detect_corrupt': True,
        'imgs_per_chapter': EVERYTHING,
        'limit_chapters': EVERYTHING,
        'start_at': 1,
    }

    LOGGER_INSTANCE = Logger()

    scrape({
        **default_scrape_props,
        **props,
    })
