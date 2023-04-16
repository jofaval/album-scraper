"""Scraper"""

import logging
# from multiprocessing import Pool
from typing import Union

from bs4 import BeautifulSoup

from request_utils import get_url_content


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
