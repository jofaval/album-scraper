"""Album"""


import os
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
from operator import attrgetter
# from multiprocessing import Pool
from typing import Generator, List, Tuple, Union

from src.album_chapters_scraper import AlbumChaptersScraper
from src.album_config import AlbumConfig
from src.chapter_config import ChapterConfig
from src.chapter_scraper import ChapterScraper
from src.health_checker import HealthChecker
from src.image_config import ImageConfig
from src.image_scraper import ImageScraper
from src.logger import get_logger


class Album():
    """A collection of chapters"""
    config: AlbumConfig
    album_chapters_scraper: AlbumChaptersScraper
    chapter_scraper: ChapterScraper
    image_scraper: ImageScraper
    chapters_links: List[str] = None

    def __init__(self, config: AlbumConfig) -> None:
        assert config.chapter_end > config.chapter_start

        get_logger().info("Initializing web scraper...")

        self.config = config

        list_of_paths = [self.config.download_dir]
        if self.config.use_slug_on_download_path:
            list_of_paths.append(self.config.slug)
        self.config.album_path = os.path.realpath(os.path.join(*list_of_paths))

    def reverse_chapters(self, chapters_links: List[str]) -> List[str]:
        """Reverse a set list of chapters"""
        return [
            link
            for _, link in sorted((
                (self.config.get_chapter_index(link, index), link)
                for index, link in enumerate(chapters_links)
            ))
        ]

    def get_chapters_links(self) -> List[str]:
        """Gets the links from all the chapters"""
        chapters_links = self.album_chapters_scraper.scrape()
        if not chapters_links:
            get_logger().warning("No chapters were found, can't reverse it")
            return None

        chapters_links = list(set(chapters_links))

        if not self.config.is_reverse_order:
            return chapters_links

        if self.config.get_chapter_index:
            chapters_links = self.reverse_chapters(chapters_links)
        else:
            chapters_links = chapters_links[::-1]

        return chapters_links

    def generate_chapters_configs(
        self,
        chapters_links: List[str],
    ) -> Generator[ChapterConfig, None, None]:
        """Generates the configuration for all the given chapters"""
        get_logger().info("Generating configuration for the chapters scraping...")
        chapter_configs = (
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
        get_logger().info("Configuration for the chapters scraping generated!!")

        return chapter_configs

    def scrape_chapter_images_thread(self, data: Tuple[ChapterConfig, List[ImageConfig]]) -> None:
        """Closure function to scrape images links and append them"""
        chapter_config, images_configs = data
        name, url = attrgetter("name", "url")(chapter_config)
        get_logger().info('Scraping chapter "%s" (%s)', name, url)

        inner_images_configs = self.chapter_scraper.scrape(chapter_config)
        if not inner_images_configs:
            get_logger().info('Could not scrape chapter "%s" (%s)', name, url)
            return None

        images_configs.extend(inner_images_configs)
        get_logger().info('Chapter "%s" (%s) scraped successfully', name, url)
        return None

    def scrape_chapters(self) -> Union[List[str], None]:
        """Get the chapter's links"""
        if self.chapters_links:
            return self.chapters_links

        get_logger().info("Starts scraping chapters, looking for links...")

        chapters_links = self.get_chapters_links()
        get_logger().info("Chapters links retrieved!")
        if not chapters_links:
            get_logger().warning("No chapters were found, it won't try to scrape")
            return None
        get_logger().info("Chapters links were successfully retrieved")

        chapters_links = chapters_links[self.config.chapter_start:self.config.chapter_end]
        self.chapters_links = chapters_links
        return chapters_links

    def download_images(self, images_configs: List[ImageConfig]) -> None:
        """Downloads the scraped images"""
        get_logger().info('Polishing the configuration for the images scraper')

        backup_album_config = images_configs[0].chapter.album
        get_chapter_index = backup_album_config.get_chapter_index
        get_chapter_name = backup_album_config.get_chapter_name
        get_link_from_tag = backup_album_config.get_link_from_tag
        get_source_from_tag = backup_album_config.get_source_from_tag

        if images_configs and len(images_configs) > 1:
            # Deletes local attributes so that it can be pickled (multiprocessing requirement)
            dummy_album_config = images_configs[0].chapter.album
            del dummy_album_config.get_chapter_index
            del dummy_album_config.get_chapter_name
            del dummy_album_config.get_link_from_tag
            del dummy_album_config.get_source_from_tag

        get_logger().info('Starting images scraper')
        with Pool(processes=self.config.max_image_processes) as executor:
            executor.map(self.image_scraper.scrape, images_configs)
        get_logger().info('Images scraped successfully!!')

        backup_album_config.get_chapter_index = get_chapter_index
        backup_album_config.get_chapter_name = get_chapter_name
        backup_album_config.get_link_from_tag = get_link_from_tag
        backup_album_config.get_source_from_tag = get_source_from_tag

    def scrape_images_from_chapter_links(
        self,
        chapters_configs: List[ChapterConfig]
    ) -> List[ImageConfig]:
        """Scrapes all the images links from every chapter"""
        images_configs: List[ImageConfig] = []

        get_logger().info("Starting to scrape the chapters, looking for images...")
        # TODO: convert to pool using a common file to write to? can't pickle local objects
        with ThreadPoolExecutor(max_workers=self.config.max_chapter_workers) as executor:
            executor.map(self.scrape_chapter_images_thread, (
                (chapter_config, images_configs)
                for chapter_config in chapters_configs
            ))
            executor.shutdown(wait=True)

        if not images_configs:
            get_logger().warning("No images could be retrieved or configured")
            return None
        get_logger().info('Chapters scraped successfully')

        return images_configs

    def prepare_scraper(self) -> None:
        """Prepares all the necessary steps to scrape"""
        self.album_chapters_scraper = AlbumChaptersScraper(self.config)
        self.chapter_scraper = ChapterScraper()
        self.image_scraper = ImageScraper()

    def scrape(self, chapters_links: List[str] = None) -> None:
        """Album's scrape orchestrator"""
        self.prepare_scraper()

        if not chapters_links:
            chapters_links = self.scrape_chapters()
            if not chapters_links:
                get_logger().warning("No chapter links were retrieved, stopping...")
                return

        if self.config.chapter_indices:
            chapters_links = [
                chapters_links[index]
                for index in self.config.chapter_indices
            ]
        get_logger().warning("%d chapter(s) was/were detected", len(chapters_links))

        chapters_configs = self.generate_chapters_configs(chapters_links)

        images_configs = self.scrape_images_from_chapter_links(
            chapters_configs
        )
        if not images_configs:
            get_logger().warning("No images could be configured, stopping...")
            return
        get_logger().warning("%d image(s) was/were detected", len(images_configs))

        self.download_images(images_configs)

        get_logger().info('\nEverything went smoothly\n')

    def check_health(self) -> None:
        """Checks the album's health"""
        get_logger().warning("Checking chapter health...")

        health_checker = HealthChecker(self.config)
        is_healthy = health_checker.is_album_healthy()

        if is_healthy:
            get_logger().warning("Album is healthy")
        else:
            get_logger().warning("Album is NOT healthy")

    def download_updates(self, updates: List[str]) -> None:
        """Downloads the given updates, overriding locally if necessary"""
        get_logger().warning("Downloading updates...")
        return self.scrape(chapters_links=updates)

    def detect_updates(self) -> None:
        """Detect updates, and conditionally download them"""
        self.prepare_scraper()

        local_chapters = [
            "-".join(chapter_folder.split("-")[1:])
            for chapter_folder in os.listdir(self.config.album_path)
        ]

        chapters_links = self.scrape_chapters()
        updates: List[str] = []
        for chapter_link in chapters_links:
            chapter_name = self.config.get_chapter_name(chapter_link)

            if chapter_name not in local_chapters:
                updates.append(chapter_link)

        if not updates:
            get_logger().warning("No updates were found")
            return

        total_updates = len(updates)
        get_logger().warning(
            "%d chapter updates were detected"
            if total_updates != 1 else "%d chapter update was detected",
            total_updates
        )
        get_logger().warning('\n'.join(updates))

        if self.config.should_download_updates:
            self.download_updates(updates)

    def start(self) -> None:
        """Album's orchestrator"""
        if self.config.should_scrape:
            self.scrape()

        if self.config.should_detect_updates:
            self.detect_updates()

        if self.config.should_check_health:
            self.check_health()
