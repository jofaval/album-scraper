"""Album"""

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

from album_chapters_scraper import AlbumChaptersScraper
from album_config import AlbumConfig
from chapter_config import ChapterConfig
from chapter_scraper import ChapterScraper
from image_config import ImageConfig
from image_scraper import ImageScraper


class Album():
    """A collection of chapters"""
    config: AlbumConfig
    album_chapters_scraper: AlbumChaptersScraper
    chapter_scraper: ChapterScraper
    image_scraper: ImageScraper

    def __init__(self, config: AlbumConfig) -> None:
        assert config.chapter_end > config.chapter_start

        logging.getLogger("album").setLevel(config.logging_level)
        logging.getLogger("webscrapper").setLevel(config.logging_level)

        logging.info("Initializing webscraper...")

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
