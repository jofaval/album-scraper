# system
from os import listdir
from os.path import isfile, join as join_paths
import os
import shutil
# scraping
from bs4 import BeautifulSoup
import requests
import validators
# performance
import threading
# types
from typing import List
from bs4 import Tag

# custom translator
from scripts.lang.index import t
# utils
from scripts.utils import check_folder_or_create, cls


DEBUG = True


def log(*args) -> None:
    """Logs information if we're in debug mode"""
    # TODO: create a logging system, per module, on the physical drive

    if not DEBUG:
        return

    log(*args)


# |---------------------------|
# |         CONSTANTS         |
# |---------------------------|

BASE_URL = ''
PARSER = ''
URL_SEPARATOR = ''

CHAPTER_IMG_QUERY = ''
CHAPTERS_FOLDER = ''
CHAPTERS_QUERY = ''

EXTRA_TITLE_CONTENT = ''
FILE_EXTENSION = ''

SHOULD_RENAME_IMAGES = None

THREADS = None
LIMIT_THREADS = 0

SEPARATOR = ''
EVERYTHING = -1


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
    return BeautifulSoup(raw_html, features=PARSER)


def get_chapters(start_at: int = 1):
    log(t('CHAPTERS.GET_ALL', {'start_at': start_at}))
    content = get(BASE_URL)
    soup = parse_html(content)

    chapter_a_tags = soup.select(CHAPTERS_QUERY)
    chapter_a_tags = chapter_a_tags[::-1]
    chapter_links = [a['href'] for a in chapter_a_tags[(start_at - 1):]]

    return chapter_links


def parse_img(img: Tag):
    return img.get('src')


def parse_chapter_title(title: str):
    title = title.replace(BASE_URL, '')
    title = title.replace(EXTRA_TITLE_CONTENT, '')
    title = title.replace(URL_SEPARATOR, '')

    return join_paths(CHAPTERS_FOLDER, title)


def get_image_filename(url: str):
    if URL_SEPARATOR not in url:
        return url

    start_at = url.rfind(URL_SEPARATOR) + 1
    return url[start_at:]


def download_img(dir: str, img_details: List[str, str]):
    [url, filename] = img_details
    filename = get_image_filename(filename)

    if not url or not validators.url(url):
        log(t('ERRORS.INVALID_URL', {'filename': filename, 'url': url}))
        return

    img_content = requests.get(url, stream=True)
    img_content.raw.decode_content = True
    with open(join_paths(dir, filename), "wb") as img_file:
        shutil.copyfileobj(img_content.raw, img_file)

    log(t('IMAGES.IMAGE_SUCCESS', {'filename': filename}))


def empty_threads():
    while THREADS:
        del THREADS[0]


def wait_all_threads():
    log(t('THREADS.WAIT_ALL'))

    for thread in THREADS:
        thread.join()

    empty_threads()


def threadify(target, args):
    img_download_thread = threading.Thread(target=target, args=args)
    img_download_thread.start()
    THREADS.append(img_download_thread)

    if (len(THREADS) >= LIMIT_THREADS):
        wait_all_threads()


def download_imgs(show_progress: bool, title: str, imgs: List[str]):
    total_imgs = len(imgs)
    log(t('IMAGES.FOUND_TOTAL_IMAGES', {'total_imgs': total_imgs}))

    THREADS = []

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
                  'url_separator': URL_SEPARATOR,
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
    return [
        [img, f'{str(index + 1).zfill(3)}{FILE_EXTENSION}' if SHOULD_RENAME_IMAGES else img]
        for index, img in enumerate(imgs)
    ]


def get_chapter(chapter_url: str, show_progress: bool = True, limit: int = EVERYTHING):
    if not validators.url(chapter_url):
        return None

    log(t('CHAPTERS.CHAPTER_DOWNLOAD_STARTS', {'chapter_url': chapter_url}))

    title = parse_chapter_title(chapter_url)

    content = get(chapter_url)
    soup = parse_html(content)
    img_tags = soup.select(CHAPTER_IMG_QUERY)
    if limit != EVERYTHING:
        img_tags = img_tags[:limit]

    check_folder_or_create(title)

    parsed_imgs = [parse_img(img) for img in img_tags]
    renamed_imgs = rename_imgs(parsed_imgs)

    download_imgs(show_progress, title, renamed_imgs)

    return soup


def detect_missing_imgs(stacktrace: bool = True):
    log(t('CHAPTERS.CORRUPT_CHAPTERS_DETECTION'))
    incomplete_chapters = []

    dir_elements = listdir(CHAPTERS_FOLDER)
    chapters = [elem for elem in dir_elements if not isfile(elem)]

    for chapter in chapters:
        log(t('IMAGES.ANALYZING_IMAGES', {'chapter': chapter}))

        chapter_path = join_paths(CHAPTERS_FOLDER, chapter)
        chapter_elements = listdir(chapter_path)
        imgs = [img.split(SEPARATOR)[0] for img in chapter_elements]

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
                    join_paths(chapter_path, str(img) + FILE_EXTENSION))
            except:
                filesize = 0
            if (not int(img) == (index + 1)) | (not filesize > 0):
                if stacktrace:
                    log(t('ERRORS.CORRPUT_IMAGE_FOUND', {
                        'chapter': chapter,
                        'index': (index + 1),
                        'extension': FILE_EXTENSION,
                        'filesize': filesize,
                    }))
                incomplete_chapters.append(chapter)
                break

    return incomplete_chapters


def scrape(
    start_at: int = 1,
    limit_chapters: int = EVERYTHING,
    imgs_per_chapter: int = EVERYTHING,
    chapter_links: List[str] = None,
    detect_corrupt: bool = True
) -> None:
    cls()

    if chapter_links is None:
        chapter_links = get_chapters(start_at)[:limit_chapters]
    if limit_chapters != EVERYTHING:
        chapter_links = chapter_links[:limit_chapters]

    check_folder_or_create(CHAPTERS_FOLDER)

    log(t('CHAPTERS.TOTAL_CHAPTERS_RETRIEVED', {
        'chapter_links': len(chapter_links)
    }))

    for chapter_link in chapter_links:
        get_chapter(chapter_link, limit=imgs_per_chapter)

    wait_all_threads()

    if detect_corrupt:
        incomplete_chapters = detect_missing_imgs()
        log(t('CHAPTERS.TOTAL_CORRUPTED_CHAPTERS', {
            'incomplete_chapters': len(incomplete_chapters),
            'incomplete_chapters': '\n'.join(incomplete_chapters)
        }))


def detect_updates(chapters: List[str] = None):
    downloaded_chapters = listdir(CHAPTERS_FOLDER)

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
