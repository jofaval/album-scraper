"""Chapter Scraper"""

# from multiprocessing import Pool
from typing import List, Union

from bs4 import BeautifulSoup

from chapter_config import ChapterConfig
from image_config import ImageConfig
from scraper import Scraper


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
