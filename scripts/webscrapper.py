# system
from os import listdir
from os.path import isfile, join as join_paths, dirname, realpath, getsize
import shutil
# scraping
import requests
import validators
# performance
import threading
import cchardet  # only needs to be imported, not used
# types
from typing import List


# local

# constants
from .constants import END_OF_LINE, EVERYTHING
# types
from .config.type import ConfigType
from .types import ScrapeProps
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


def get(url: str):
    if not validators.url(url):
        return None

    try:
        response = requests.get(url)
        return response.content
    except:
        LOGGER_INSTANCE.log(t('ERRORS.GET_PAGE', {'url': url}))
        return None


def parse_html(raw_html: str):
    return BeautifulSoup(raw_html, features=CONF['PARSER'])


def get_chapters(start_at: int = 1):
    LOGGER_INSTANCE.log(t('CHAPTERS.GET_ALL', {'start_at': start_at}))
    content = get(CONF['BASE_URL'])
    soup = parse_html(content)

    chapter_a_tags = soup.select(CONF['CHAPTERS_QUERY'])
    # reverse the order, first becomes last, and so on and so forth
    chapter_a_tags = chapter_a_tags[::-1]
    chapter_links = [a['href'] for a in chapter_a_tags[(start_at - 1):]]

    return chapter_links


def parse_img(img: Tag):
    return img.get(CONF['IMG_SRC_ATTRIBUTE'])


def parse_chapter_title(title: str):
    title = title.replace(CONF['BASE_URL'], '')
    title = title.replace(CONF['EXTRA_TITLE_CONTENT'], '')
    title = title.replace(CONF['URL_SEPARATOR'], '')

    return join_paths(CONF['BASE_DIR'], CONF['CHAPTERS_FOLDER'], title)


def get_image_filename(url: str):
    if CONF['URL_SEPARATOR'] not in url:
        return url

    start_at = url.rfind(CONF['URL_SEPARATOR']) + 1
    return url[start_at:]


def download_img(dir: str, img_details: List[str]):
    [url, filename] = img_details
    filename = get_image_filename(filename)

    if not url or not validators.url(url):
        LOGGER_INSTANCE.log(
            t('ERRORS.INVALID_URL', {'filename': filename, 'url': url}))
        return

    img_content = requests.get(url, stream=True)
    img_content.raw.decode_content = True
    with open(join_paths(CONF['BASE_DIR'], dir, filename), "wb") as img_file:
        shutil.copyfileobj(img_content.raw, img_file)

    LOGGER_INSTANCE.log(t('IMAGES.IMAGE_SUCCESS', {'filename': filename}))


def empty_threads():
    while CONF['THREADS']:
        del CONF['THREADS'][0]


def wait_all_threads():
    LOGGER_INSTANCE.log(t('THREADS.WAIT_ALL'))

    for thread in CONF['THREADS']:
        thread.join()

    empty_threads()


def threadify(target, args):
    img_download_thread = threading.Thread(target=target, args=args)
    img_download_thread.start()
    CONF['THREADS'].append(img_download_thread)

    if (len(CONF['THREADS']) >= CONF['LIMIT_THREADS']):
        wait_all_threads()


def download_imgs(show_progress: bool, title: str, imgs: List[str]):
    total_imgs = len(imgs)
    LOGGER_INSTANCE.log(t('IMAGES.FOUND_TOTAL_IMAGES',
                          {'total_imgs': total_imgs}))

    THREADS: List[threading.Thread] = []

    # TODO: add queues?
    not_downloaded = []
    percentage = 100
    for index, img in enumerate(imgs):
        percentage = '{0:.2%}'.format((index + 1) / total_imgs)

        try:
            img_download_thread = threading.Thread(
                target=download_img, args=(title, img))
            img_download_thread.start()
            THREADS.append(img_download_thread)

            if show_progress:
                t('CHAPTERS.PROGRESS_PERCENTAGE', {
                  'title': title,
                  'percentage': percentage,
                  'index': index,
                  'url_separator': CONF['URL_SEPARATOR'],
                  'total_imgs': total_imgs
                  })
        except:
            LOGGER_INSTANCE.log(t('ERRORS.IMAGE_DIDNT_DOWNLOAD', {'img': img}))
            not_downloaded.append(img)

    for thread in THREADS:
        thread.join()

    LOGGER_INSTANCE.log(t('IMAGES.IMAGES_DOWNLOADED'))
    if len(not_downloaded) > 0:
        LOGGER_INSTANCE.log('IMAGES.NOT_DOWNLOADED', {
                            'not_downloaded': len(not_downloaded)})


def rename_imgs(imgs: List[str]) -> List[str]:
    """
    Renombra las imágenes, del nombre que sea, a un índice

    imgs : List[str]
        Todas las imágenes, en formato de string

    devuelve las imágenes renombradas
    returns List[str]
    """
    extension = CONF['FILE_EXTENSION']
    should_rename = CONF['SHOULD_RENAME_IMAGES']

    return [
        [img, f'{str(index + 1).zfill(3)}{extension}' if should_rename else img]
        for index, img in enumerate(imgs)
    ]


def get_chapter(chapter_url: str, show_progress: bool = True, limit: int = CONF['EVERYTHING']):
    parsed_chapter_url = chapter_url

    # attempts to add the domain, if not already provided
    if not validators.url(parsed_chapter_url):
        if CONF['DOMAIN'].endswith(CONF['URL_SEPARATOR']):
            parsed_chapter_url = CONF['DOMAIN'] + parsed_chapter_url
        else:
            parsed_chapter_url = f'{CONF["DOMAIN"]}{CONF["URL_SEPARATOR"]}{parsed_chapter_url}'

    if not validators.url(parsed_chapter_url):
        LOGGER_INSTANCE.log(t('ERRORS.INVALID_CHAPTER_URL', {
            'chapter_url': parsed_chapter_url}))
        return None

    LOGGER_INSTANCE.log(t('CHAPTERS.CHAPTER_DOWNLOAD_STARTS',
                          {'chapter_url': parsed_chapter_url}))

    title = parse_chapter_title(chapter_url)

    content = get(parsed_chapter_url)
    soup = parse_html(content)
    img_tags = soup.select(CONF['CHAPTER_IMG_QUERY'])
    if limit != CONF['EVERYTHING']:
        img_tags = img_tags[:limit]

    check_folder_or_create(join_paths(CONF['BASE_DIR'], title))

    parsed_imgs = [parse_img(img) for img in img_tags]
    renamed_imgs = rename_imgs(parsed_imgs)

    download_imgs(show_progress, title, renamed_imgs)

    return soup


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
                filesize = os.path.getsize(
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


def scrape(props: ScrapeProps) -> None:
    cls()
    check_folder_or_create(CONF['BASE_DIR'])

    usable_props: ScrapeProps = {**props}

    if usable_props['chapter_links'] is None:
        usable_props['chapter_links'] = get_chapters(usable_props['start_at'])
    if usable_props['limit_chapters'] != CONF['EVERYTHING']:
        usable_props['chapter_links'] = usable_props['chapter_links'][:usable_props['limit_chapters']]

    check_folder_or_create(
        join_paths(CONF['BASE_DIR'], CONF['CHAPTERS_FOLDER'])
    )

    LOGGER_INSTANCE.log(t('CHAPTERS.TOTAL_CHAPTERS_RETRIEVED', {
        'chapter_links': len(usable_props['chapter_links'])
    }))

    for chapter_link in usable_props['chapter_links']:
        get_chapter(chapter_link, limit=usable_props['imgs_per_chapter'])

    wait_all_threads()

    if usable_props['detect_corrupt']:
        incomplete_chapters = detect_missing_imgs()
        LOGGER_INSTANCE.log(t('CHAPTERS.TOTAL_CORRUPTED_CHAPTERS', {
            'total_incomplete_chapters': len(incomplete_chapters),
            'incomplete_chapters': END_OF_LINE.join(incomplete_chapters)
        }))


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
