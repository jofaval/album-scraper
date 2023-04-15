"""
Main entrypoint and workflow for the scraper
"""


# |---------------------------|
# |         CONSTANTS         |
# |---------------------------|

import logging
import urllib.request
from typing import Callable, List, Union

from bs4 import BeautifulSoup, Tag
from pydantic import BaseModel
from requests import get
from validators import url as is_url

DEBUG = True
SHOULD_LOG = True


def is_valid_url(url: str) -> bool:
    """Detects if the URL is valid for a request"""
    return not url or not is_url(url)


def get_url_content(url: str, timeout: float = 25):
    """Retrieves the URL's content"""
    if is_valid_url(url):
        return None

    try:
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
        response = get(
            url,
            timeout=timeout,
            headers=headers
        )
        return response.content
    except Exception:
        # logger.log(t('ERRORS.GET_PAGE', {'url': url}))
        return None


class AlbumConfig(BaseModel):
    """All the necessary configuration for an album"""
    starting_url: str
    chapter_link_query: str
    get_link_from_anchor: Union[Callable[[Tag], None], None]
    is_reverse_order: bool = True
    get_chapter_name: Callable[[str], str]
    image_source_query: str
    get_source_from_tag: Union[Callable[[BeautifulSoup], str], None]


class Scraper():
    """Base scraper"""

    def __init__(self) -> None:
        pass

    def parse_content(self, content: Union[str, None]) -> Union[BeautifulSoup, None]:
        """Parse the content, can fail"""
        if not content:
            return None

        return BeautifulSoup(content, features="lxml-xml")

    def scrape_url(self, url: str) -> Union[BeautifulSoup, None]:
        """Gets the url's content"""
        content = get_url_content(url)

        if not content:
            logging.warning("No content was retrieved from: %s", url)
            return None

        logging.info(content)

        return self.parse_content(content)


class AlbumChaptersScraper(Scraper):
    """Scrapers all the chapter links for an album"""
    config: AlbumConfig

    def __init__(self, config: AlbumConfig) -> None:
        self.config = config

    def get_chapter_links_from_content(self, content: BeautifulSoup) -> List[str]:
        """Get chapter links from the page content"""
        chapter_anchors = content.select(self.config.chapter_link_query)
        if not chapter_anchors:
            return None

        chapter_links = []
        for anchor in chapter_anchors:
            link = ""

            if self.config.get_link_from_anchor:
                link = self.config.get_link_from_anchor(anchor)
            else:
                link = anchor.attrs["href"]

            if not link:
                continue

            chapter_links.append(link)

        return chapter_links

    def scrape(self, page_start=0, page_end=1_000_000_000) -> Union[List[str], None]:
        """Scrapers all the chapter links from the starting page"""
        starting_page_content = self.scrape_url(self.config.starting_url)
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

            chapter_links.append(links_from_content)

        return chapter_links


class ChapterConfig(BaseModel):
    """All the necessary configuration for a chapter"""
    name: str
    url: str
    index: int
    image_source_query: str
    get_source_from_tag: Union[Callable[[BeautifulSoup], str], None]
    album: AlbumConfig


class ImageConfig(BaseModel):
    """All the necessary configuration for an image"""
    index: int
    url: str
    # TODO: include format?
    chapter: ChapterConfig


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
        content = self.scrape_url(config.url)
        if not content:
            return None

        return [
            ImageConfig(url=image, index=index, chapter=config)
            for index, image in enumerate(self.get_images_sources_from_content(content, config))
        ]


class ImageScraper():
    """Scrapes an image and properly retrieves it's metadata"""

    def get_metadata(self) -> None:
        """Gets the image metadata"""

    def save(self, content: str, meta_image_name: str) -> None:
        """Writes the image into a file"""

    def get_image_path(self, meta_image_name: str, config: ImageConfig) -> str:
        """Generates the image's final path"""
        # TODO: move to configuration, at least to a constant
        chapter_index = str(config.chapter.index).zfill(4)
        # TODO: move to configuration, at least to a constant
        image_index = str(config.index).zfill(3)

        return f'{chapter_index}-{config.chapter.name}/{image_index}-{meta_image_name}'

    def scrape(self, config: ImageConfig) -> None:
        """Scrapes an image and writes it with metadata"""
        image = urllib.request.urlretrieve(config.url)
        # image = Image.open(config.url)
        logging.info("image %s", image)
        # logging.warning({"name": image.filename, "format": image.format})


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

        if self.config.is_reverse_order:
            chapters_links = chapters_links[::-1]
        return list(set(chapters_links))

    def scrape_chapters(self) -> None:
        """Get the raw HTML chapter content"""
        chapters_links = self.get_chapters_links()
        if not chapters_links:
            logging.warning("No chapters were found, it won't try to scrape")
            return None

        # TODO: remove, for testing purposes
        chapters_links = chapters_links[:1]

        chapters_configs = (
            ChapterConfig(
                url=chapter_link,
                name=self.config.get_chapter_name(chapter_link),
                image_source_query=self.config.image_source_query,
                get_source_from_tag=self.config.get_source_from_tag,
                # TODO: careful with subsets of chapters, a more complex method should be provided
                index=index,
                album=self.config,
            )
            for index, chapter_link in enumerate(chapters_links)
        )

        # use pool for max download/scraping speed
        images_configs: List[ImageConfig] = []
        for chapter_config in chapters_configs:
            inner_images_configs = self.chapter_scraper.scrape(chapter_config)
            if not inner_images_configs:
                continue

            images_configs.extend(inner_images_configs)

        # TODO: remove, for testing purposes, use the whole
        images_configs = images_configs[:1]

        for image_config in images_configs:
            self.image_scraper.scrape(image_config)


def start() -> None:
    """
    Starts all the processes

    Serves as the orchestrator for the scraping
    """

    def get_chapter_name(chapter_url: str) -> str:
        """Gets the chapter url"""
        if not chapter_url:
            return ""

        if chapter_url.endswith("/"):
            chapter_url = chapter_url[:-1]

        return chapter_url.split("/")[-1]

    # Example config
    album_config = AlbumConfig(
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
