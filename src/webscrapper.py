"""
Main entrypoint and workflow for the scraper
"""


# |---------------------------|
# |         CONSTANTS         |
# |---------------------------|

import logging
import os
import shutil
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
from operator import attrgetter
# from multiprocessing import Pool
from typing import Callable, Generator, List, Tuple, Union

from bs4 import BeautifulSoup, Tag
from pydantic import BaseModel
from requests import Response, get
from validators import url as is_url

DEBUG = True
SHOULD_LOG = True

# TODO: attempt to code-split?!


def is_valid_url(url: str) -> bool:
    """Detects if the URL is valid for a request"""
    return not url or not is_url(url)


def get_url_content(
    url: str,
    timeout: float = 25,
    should_retry: bool = True,
    retry_times: int = 3
):
    """Retrieves the URL's content"""
    if is_valid_url(url):
        return None

    # https://www.whatismybrowser.com/detect/what-http-headers-is-my-browser-sending?sort=dont-sort
    headers = {
        # "Content-Type": "",
        # "Content-Length": "",
        # "Host": "www.whatismybrowser.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.google.com/",
        # "Upgrade-Insecure-Requests": "1",
        # "Sec-Fetch-Dest": "document",
        # "Sec-Fetch-Mode": "navigate",
        # "Sec-Fetch-Site": "same-origin",
        # "Sec-Fetch-User": "?1",
        # "Sec-Gpc": "1",
        # "Te": "trailers",
    }

    # -1 implements a pseudo do-while
    max_retry = retry_times if should_retry else -1
    retry_attempt = 0

    while True:
        if retry_attempt >= 1:
            logging.warning(
                "Retrying %s for the %d failed attempt(s)", url, retry_attempt
            )

        try:
            response = get(
                url,
                timeout=timeout,
                # headers=headers,
                allow_redirects=True
            )

            if not response.ok:
                raise Exception(f'Response for "{url}" failed')

            return response.content
        except Exception as error:
            logging.exception(error)
        finally:
            retry_attempt += 1
            if retry_attempt >= max_retry:
                break

        return None


class AlbumConfig(BaseModel):
    """All the necessary configuration for an album"""
    # album
    chapter_link_query: str
    """CSS query to get the chapters links"""
    get_link_from_tag: Union[Callable[[Tag], None], None]
    """Extracts the link from the chapter tag"""
    is_reverse_order: bool = True
    """Does it show first the latest chapters? If so, it's in reverse order"""
    slug: str
    """Filepath slug for the album"""
    starting_url: str
    """Base url from which to scrape the chapters links"""

    # chapters
    chapter_end: int = 1_000_000_000
    """Last chapter to scrape"""
    chapter_index_len: int = 4
    """Length of the index in the filepath, e.g. 4 would be 0000-chapter-name"""
    chapter_start: int = 0
    """Start chapter to scrape"""
    get_chapter_index: Union[Callable[[str, int], int], None]
    """Custom function for the chapter index extraction"""
    get_chapter_name: Callable[[str], str]
    """Function to extrapolate the chapter's name from the url"""
    max_chapter_workers: int = 4
    """Maximum amount of concurrent threads for the chapter extraction"""
    max_retry_attempts_per_chapter: int = 3
    """Maximum amount of retries per chapter, when scraping image links"""
    should_retry_chapters: bool = True
    """Should it even retry at all?"""

    # images
    get_source_from_tag: Union[Callable[[BeautifulSoup], str], None]
    """Gets the source link, usually from an image tag"""
    image_index_len: int = 3
    """Length of the index in the filepath, e.g. 3 would be chapter-name/000.jpg"""
    image_source_query: str
    """CSS Query to retrieve all the images tags"""
    max_image_processes: int = 4
    """Maximum amount of processes to download the images"""
    max_retry_attempts_per_image: int = 3
    """Maximum amount of retries per image, when downloading an image"""
    should_retry_images: bool = True
    """Should it even retry at all?"""


class Scraper():
    """Base scraper"""

    def __init__(self) -> None:
        pass

    def parse_content(self, content: Union[str, None]) -> Union[BeautifulSoup, None]:
        """Parse the content, can fail"""
        if not content:
            return None

        return BeautifulSoup(content, features="lxml")

    def scrape_url(self, url: str, should_retry: bool, retry_times: int) -> Union[BeautifulSoup, None]:
        """Gets the url's content"""
        content = get_url_content(
            url,
            should_retry=should_retry,
            retry_times=retry_times
        )
        if not content:
            logging.warning("No content was retrieved from: %s", url)
            return None

        return self.parse_content(content)


class AlbumChaptersScraper(Scraper):
    """Scrapers all the chapter links for an album"""
    config: AlbumConfig

    def __init__(self, config: AlbumConfig) -> None:
        self.config = config

    def get_chapter_links_from_content(self, content: BeautifulSoup) -> List[str]:
        """Get chapter links from the page content"""
        chapter_links_tags = content.select(self.config.chapter_link_query)
        if not chapter_links_tags:
            return None

        chapter_links = []
        for element_tag in chapter_links_tags:
            link = ""

            if self.config.get_link_from_tag:
                link = self.config.get_link_from_tag(element_tag)
            else:
                link = element_tag.attrs["href"]

            if not link:
                continue

            chapter_links.append(link)

        return chapter_links

    def scrape(self, page_start=0, page_end=1_000_000_000) -> Union[List[str], None]:
        """Scrapers all the chapter links from the starting page"""
        starting_page_content = self.scrape_url(
            self.config.starting_url,
            self.config.should_retry_chapters,
            self.config.max_retry_attempts_per_chapter
        )
        if not starting_page_content:
            logging.warning(
                "No content was found for chapter links to be retrieved from"
            )
            return None

        chapter_links = []

        # TODO: implement pagination
        page_contents = [starting_page_content]
        for content in page_contents:
            links_from_content = self.get_chapter_links_from_content(content)
            if not links_from_content:
                continue

            chapter_links.extend(links_from_content)

        return chapter_links


class ChapterConfig(BaseModel):
    """All the necessary configuration for a chapter"""
    album: AlbumConfig
    """Album's configuration"""
    get_source_from_tag: Union[Callable[[BeautifulSoup], str], None]
    """Gets the source link, usually from an image tag"""
    image_source_query: str
    """CSS Query to retrieve all the images tags"""
    index: int
    """Chapter's index"""
    name: str
    """Chapter's name"""
    url: str
    """Chapter's url"""


class ImageConfig(BaseModel):
    """All the necessary configuration for an image"""
    index: int
    """Image's index"""
    url: str
    """Image's url"""
    # TODO: include format?
    chapter: ChapterConfig
    """Chapter's configuration"""


class ChapterScraper(Scraper):
    """Chapter scraper"""

    def get_images_sources_from_content(
        self,
        content: BeautifulSoup,
        config: ChapterConfig
    ) -> Union[List[str], None]:
        """Gets all the images sources from the content"""
        images_tags = content.select(config.image_source_query)
        if not images_tags:
            return None

        images_sources = []
        for image_tag in images_tags:
            source = ""

            if config.get_source_from_tag:
                source = config.get_source_from_tag(image_tag)
            else:
                source = image_tag.attrs["src"]

            if not source:
                continue

            images_sources.append(source)

        return images_sources

    def scrape(self, config: ChapterConfig) -> Union[List[ImageConfig], None]:
        """Gets all the image's links"""
        content = self.scrape_url(
            config.url,
            config.album.should_retry_chapters,
            config.album.max_retry_attempts_per_chapter,
        )
        if not content:
            return None

        image_sources = self.get_images_sources_from_content(content, config)
        if not image_sources:
            return None

        return [
            ImageConfig(url=image, index=index, chapter=config)
            for index, image in enumerate(image_sources)
        ]


class ImageScraper():
    """Scrapes an image and properly retrieves it's metadata"""

    def save(self, content: str, image_path: str) -> None:
        """Writes the image into a file"""
        image_path_dir = os.path.dirname(image_path)
        if not os.path.exists(image_path_dir):
            os.makedirs(image_path_dir)

        try:
            if os.path.exists(image_path):
                os.remove(image_path)

            with open(image_path, 'wb') as writer:
                shutil.copyfileobj(content, writer)
        except Exception as error:
            logging.exception(
                "Could not save image %s, error: %s",
                image_path,
                error
            )

    def get_image_extension(self, img_format: str) -> str:
        """Parses the image format into an extension"""
        if img_format == "image/jpeg":
            return "jpg"
        if img_format == "image/png":
            return "png"

        return "jpg"

    def get_image_path(self, meta_image_name: str, config: ImageConfig, img_format: str) -> str:
        """Generates the image's final path"""
        chapter_index = str(config.chapter.index).zfill(
            config.chapter.album.chapter_index_len
        )
        image_index = str(config.index).zfill(
            config.chapter.album.image_index_len
        )

        extension = self.get_image_extension(img_format)
        # return f'{chapter_index}-{config.chapter.name}/{image_index}-{meta_image_name}'

        return os.path.join(
            config.chapter.album.slug,
            f"{chapter_index}-{config.chapter.name}",
            f"{image_index}.{extension}"
        )

    def get_image_content(self, config: ImageConfig) -> Union[Response, None]:
        """Downloads the image with retries"""
        # -1 implements a pseudo do-while
        max_retry = config.chapter.album.max_retry_attempts_per_image if config.chapter.album.should_retry_images else -1
        retry_attempt = 0

        while True:
            logging.info("Attempting image download for %s", config.url)
            if retry_attempt > 0:
                logging.info("Attempt number %d", retry_attempt)

            try:
                response = get(config.url, stream=True, timeout=30)
                if not response.ok:
                    logging.warning(
                        "%s failed download, might retry",
                        config.url
                    )
                    raise Exception("%s failed download, might retry")

                return response
            except Exception as error:
                logging.exception(error)
            finally:
                retry_attempt += 1
                if retry_attempt >= max_retry:
                    return None

    def scrape(self, config: ImageConfig) -> None:
        """Scrapes an image and writes it with metadata"""
        logging.info("Start scraper for image: %s", config.url)
        response = self.get_image_content(config)
        if not response or not response.ok:
            logging.warning("%s could not be downloaded", config.url)
            return None

        image_path = self.get_image_path(
            # TODO: properly detect the image name, or content-disposition
            # meta_image_name=config.url.split("/")[-1],
            meta_image_name="",
            config=config,
            img_format=response.headers.get("Content-Type")
        )

        logging.info("Attempting to save image %s %s", image_path, config.url)
        try:
            # TODO: implement base path
            self.save(response.raw, image_path)
            # TODO: implement proper threading with file as tuple space
        except Exception as error:
            logging.exception(
                "Image could not be saved %s %s, %s", image_path, config.url, error
            )
            return None

        logging.info("Image saved %s %s!!", image_path, config.url)
        return None


class Album():
    """A collection of chapters"""
    config: AlbumConfig
    album_chapters_scraper: AlbumChaptersScraper
    chapter_scraper: ChapterScraper
    image_scraper: ImageScraper

    def __init__(self, config: AlbumConfig) -> None:
        self.config = config
        self.album_chapters_scraper = AlbumChaptersScraper(config)
        self.chapter_scraper = ChapterScraper()
        self.image_scraper = ImageScraper()

    def get_chapters_links(self) -> List[str]:
        """Gets the links from all the chapters"""
        chapters_links = self.album_chapters_scraper.scrape()
        if not chapters_links:
            logging.warning("No chapters were found, can't reverse it")
            return None

        chapters_links = list(set(chapters_links))

        if self.config.is_reverse_order:
            # chapters_links = chapters_links[::-1]
            if self.config.get_chapter_index:
                chapters_links = [
                    link
                    for index, link in sorted((
                        (self.config.get_chapter_index(link, index), link)
                        for index, link in enumerate(chapters_links)
                    ))
                ]
            else:
                chapters_links = chapters_links[::-1]

        return chapters_links

    def generate_chapters_configs(self, chapters_links: List[str]) -> Generator[ChapterConfig, None, None]:
        """Generates the configuration for all the given chapters"""
        return (
            ChapterConfig(
                url=chapter_link,
                name=self.config.get_chapter_name(chapter_link),
                image_source_query=self.config.image_source_query,
                get_source_from_tag=self.config.get_source_from_tag,
                # TODO: careful with subsets of chapters, a more complex method should be provided
                index=self.config.get_chapter_index(chapter_link, index)
                if self.config.get_chapter_index else index,
                album=self.config,
            )
            for index, chapter_link in enumerate(chapters_links)
        )

    def scrape_chapter_images_thread(self, data: Tuple[ChapterConfig, List[ImageConfig]]) -> None:
        """Closure function to scrape images links and append them"""
        chapter_config, images_configs = data
        name, url = attrgetter("name", "url")(chapter_config)
        logging.info('Scraping chapter "%s" (%s)', name, url)

        inner_images_configs = self.chapter_scraper.scrape(chapter_config)
        if not inner_images_configs:
            logging.info('Could not scrape chapter "%s" (%s)', name, url)
            return None

        images_configs.extend(inner_images_configs)
        logging.info('Chapter "%s" (%s) scraped successfully', name, url)
        return None

    def scrape_chapters(self) -> None:
        """Get the raw HTML chapter content"""
        logging.info("Starts scraping chapters, looking for links...")

        chapters_links = self.get_chapters_links()
        logging.info("Chapters links retrieved!")
        if not chapters_links:
            logging.warning("No chapters were found, it won't try to scrape")
            return None
        logging.info("Chapters links were successfully retrieved")

        # TODO: remove, for testing purposes
        # chapters_links = chapters_links[:8]
        # chapters_links = chapters_links[:5]
        # chapters_links = chapters_links[8:10]
        chapters_links = chapters_links[10:11]

        logging.info("Generating configuration for the chapters scraping...")
        chapters_configs = self.generate_chapters_configs(chapters_links)
        logging.info("Configuration for the chapters scraping generated!!")

        images_configs: List[ImageConfig] = []

        logging.info("Starting to scrape the chapters, looking for images...")
        # TODO: convert to pool using a common file to write to? can't pickle local objects
        with ThreadPoolExecutor(max_workers=self.config.max_chapter_workers) as executor:
            executor.map(self.scrape_chapter_images_thread, (
                (chapter_config, images_configs)
                for chapter_config in chapters_configs
            ))
            executor.shutdown(wait=True)

        if not images_configs:
            logging.warning("No images could be retrieved or configured")
            return None
        logging.info('Chapters scraped successfully')

        # TODO: remove, for testing purposes, use the whole
        # images_configs = images_configs[:1]

        logging.info('Polishing the configuration for the images scraper')
        if images_configs and len(images_configs) > 1:
            del images_configs[1].chapter.album.get_chapter_index
            del images_configs[1].chapter.album.get_chapter_name
            del images_configs[1].chapter.album.get_link_from_tag
            del images_configs[1].chapter.album.get_source_from_tag

        logging.info('Starting images scraper')
        with Pool(processes=self.config.max_image_processes) as executor:
            executor.map(self.image_scraper.scrape, images_configs)
        logging.info('Images scraped successfully!!')

        logging.info('\nEverything went smoothly\n')
        return None


def start() -> None:
    """
    Starts all the processes

    Serves as the orchestrator for the scraping
    """
    # TODO: move to a configuration param that requires the logging.LEVEL
    logging.getLogger("webscrapper").setLevel(logging.ERROR)

    logging.info("Initializing webscraper...")

    def get_chapter_name(chapter_url: str) -> str:
        """Gets the chapter url"""
        if not chapter_url:
            return ""

        if chapter_url.endswith("/"):
            chapter_url = chapter_url[:-1]

        return chapter_url.split("/")[-1]

    # TODO: implement download path

    # Example config
    album_config = AlbumConfig(
        slug="example",
        chapter_link_query=".chapters li a",
        starting_url="https://favorite-album.com/album/",
        is_reverse_order=True,
        get_chapter_name=get_chapter_name,
        image_source_query=".chapter_content img.chapter_img"
    )

    album = Album(album_config)

    try:
        album.scrape_chapters()
    except Exception as error:
        logging.exception("error %s", error)

# TODO: refactor into generators as much as possible for an efficient memory usage


if __name__ == "__main__":
    start()
