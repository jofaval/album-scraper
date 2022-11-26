# system
from os import listdir
from os.path import isfile, join as join_paths, dirname, realpath
import os
import shutil
# scraping
from bs4 import BeautifulSoup
import requests
import validators
# performance
import threading
import cchardet  # only needs to be imported, not used
# types
from typing import List
from bs4 import Tag

# types
from scripts.config.type import ConfigType
from scripts.types import ScrapeProps
# custom translator
from scripts.lang import t
# utils
from scripts.utils import check_folder_or_create, cls
# config
from scripts.config.default import DEFAULT_CONFIG


DEBUG = True


def log(*args, display: bool = True) -> None:
    """Logs information if we're in debug mode"""
    # TODO: create a logging system, per module, on the physical drive

    if not DEBUG:
        return

    if display:
        print(*args)


# |---------------------------|
# |         CONSTANTS         |
# |---------------------------|

CONF: ConfigType = {
    **DEFAULT_CONFIG,
    'BASE_DIR': dirname(realpath(__file__))
}


def get(url: str):
    if not validators.url(url):
        return None

    try:
        response = requests.get(url)
        return response.content
    except:
        log(t('ERRORS.GET_PAGE', {'url': url}))
        return None


def parse_html(raw_html: str):
    return BeautifulSoup(raw_html, features=CONF['PARSER'])


def get_chapters(start_at: int = 1):
    log(t('CHAPTERS.GET_ALL', {'start_at': start_at}))
    content = get(CONF['BASE_URL'])
    soup = parse_html(content)

    chapter_a_tags = soup.select(CONF['CHAPTERS_QUERY'])
    # reverse the order, first becomes last, and so on and so forth
    chapter_a_tags = chapter_a_tags[::-1]
    chapter_links = [a['href'] for a in chapter_a_tags[(start_at - 1):]]

    return chapter_links


def parse_img(img: Tag):
    return img.get('src')


def parse_chapter_title(title: str):
    title = title.replace(CONF['BASE_URL'], '')
    title = title.replace(CONF['EXTRA_TITLE_CONTENT'], '')
    title = title.replace(CONF['URL_SEPARATOR'], '')

    return join_paths(CONF['CHAPTERS_FOLDER'], title)


def get_image_filename(url: str):
    if CONF['URL_SEPARATOR'] not in url:
        return url

    start_at = url.rfind(CONF['URL_SEPARATOR']) + 1
    return url[start_at:]


def download_img(dir: str, img_details: List[str, str]):
    [url, filename] = img_details
    filename = get_image_filename(filename)

    if not url or not validators.url(url):
        log(t('ERRORS.INVALID_URL', {'filename': filename, 'url': url}))
        return

    img_content = requests.get(url, stream=True)
    img_content.raw.decode_content = True
    with open(join_paths(CONF['BASE_DIR'], dir, filename), "wb") as img_file:
        shutil.copyfileobj(img_content.raw, img_file)

    log(t('IMAGES.IMAGE_SUCCESS', {'filename': filename}))


def empty_threads():
    while CONF['THREADS']:
        del CONF['THREADS'][0]


def wait_all_threads():
    log(t('THREADS.WAIT_ALL'))

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
    log(t('IMAGES.FOUND_TOTAL_IMAGES', {'total_imgs': total_imgs}))

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
            log(t('ERRORS.IMAGE_DIDNT_DOWNLOAD', {'img': img}))
            not_downloaded.append(img)

    for thread in THREADS:
        thread.join()

    log(t('IMAGES.IMAGES_DOWNLOADED'))
    if len(not_downloaded) > 0:
        log('IMAGES.NOT_DOWNLOADED', {'not_downloaded': len(not_downloaded)})


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
    if not validators.url(chapter_url):
        return None

    log(t('CHAPTERS.CHAPTER_DOWNLOAD_STARTS', {'chapter_url': chapter_url}))

    title = parse_chapter_title(chapter_url)

    content = get(chapter_url)
    soup = parse_html(content)
    img_tags = soup.select(CONF['CHAPTER_IMG_QUERY'])
    if limit != CONF['EVERYTHING']:
        img_tags = img_tags[:limit]

    check_folder_or_create(title)

    parsed_imgs = [parse_img(img) for img in img_tags]
    renamed_imgs = rename_imgs(parsed_imgs)

    download_imgs(show_progress, title, renamed_imgs)

    return soup


def detect_missing_imgs(stacktrace: bool = True):
    log(t('CHAPTERS.CORRUPT_CHAPTERS_DETECTION'))
    incomplete_chapters = []

    dir_elements = listdir(CONF['CHAPTERS_FOLDER'])
    chapters = [elem for elem in dir_elements if not isfile(elem)]

    for chapter in chapters:
        log(t('IMAGES.ANALYZING_IMAGES', {'chapter': chapter}))

        chapter_path = join_paths(CONF['CHAPTERS_FOLDER'], chapter)
        chapter_elements = listdir(chapter_path)
        imgs = [img.split(CONF['SEPARATOR'])[0] for img in chapter_elements]

        new_imgs = []
        for img in imgs:
            if '-' not in img:
                continue

            # edge case, there might be some sort of dash to filter from
            try:
                new_imgs.append(int(img.split('-')[-1]))
            except:
                log(t('ERRORS.PARSE_ERROR'))
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
                    log(t('ERRORS.CORRPUT_IMAGE_FOUND', {
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

    if chapter_links is None:
        chapter_links = get_chapters(props.start_at)[:props.limit_chapters]
    if props.limit_chapters != CONF['EVERYTHING']:
        chapter_links = chapter_links[:props.limit_chapters]

    check_folder_or_create(CONF['CHAPTERS_FOLDER'])

    log(t('CHAPTERS.TOTAL_CHAPTERS_RETRIEVED', {
        'chapter_links': len(chapter_links)
    }))

    for chapter_link in chapter_links:
        get_chapter(chapter_link, limit=props.imgs_per_chapter)

    wait_all_threads()

    if props.detect_corrupt:
        incomplete_chapters = detect_missing_imgs()
        log(t('CHAPTERS.TOTAL_CORRUPTED_CHAPTERS', {
            'incomplete_chapters': len(incomplete_chapters),
            'incomplete_chapters': '\n'.join(incomplete_chapters)
        }))


def detect_updates(chapters: List[str] = None):
    downloaded_chapters = listdir(CONF['CHAPTERS_FOLDER'])

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

    log(t('UPDATES.NEWS_ARE', {'updates': updates}))

    prompt = t('UPDATES.DOWNLOAD_PROMPT')
    option = input(prompt)

    log(t('UPDATES.CHOSEN_OPTION', {'option': option}))

    if not option.lower() == 's':

        return log(t('UPDATES.NOT_DOWNLOADING_NEWS'))

    scrape(chapter_links=updates, detect_corrupt=False)

    log(t('UPDATES.NEWS_DOWNLOADED'))


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
    set_configuration(conf)
    scrape(props)
