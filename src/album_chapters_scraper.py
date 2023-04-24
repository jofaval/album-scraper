"""Album Chapters Scraper"""

import logging
from typing import List, Union

from bs4 import BeautifulSoup

from src.album_config import AlbumConfig
from src.scraper import Scraper


class AlbumChaptersScraper(Scraper):
    """Scrapers all the chapter links for an album"""
    config: AlbumConfig

    def __init__(self, config: AlbumConfig) -> None:
        self.config = config

    def get_chapter_links_from_content(self, content: BeautifulSoup) -> List[str]:
        """Get chapter links from the page content"""
        chapter_links_tags = content.select(self.config.chapter_link_query)
        if not chapter_links_tags:
            logging.warning("No chapter links were found... sorry")
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

    def scrape(
        self,
        # initial page index
        page_start=0,
        # last page index
        page_end=1_000_000_000
    ) -> Union[List[str], None]:
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
