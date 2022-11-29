"""
Request utilities
"""

# requests
from typing import Any, Union
from requests import get
from validators import url as is_url
# parser
from bs4 import BeautifulSoup
from bs4 import Tag
import cchardet  # only needs to be imported, not used

# logger
from ..logger.logger import Logger
# custom translator
from ..lang import t


class Requester():
    logger: Logger
    """The logger instance"""

    parser: str
    """BS4's parser to use"""

    src_attribute: str
    """The img's attribute for the link"""

    timeout: float = 5
    """Request's timeout, expressed in seconds"""

    def __init__(self, logger, parser, src_attribute='src') -> None:
        self.logger = logger
        self.parser = parser
        self.src_attribute = src_attribute

    def is_valid_url(self, url: str) -> bool:
        """Detects if the URL is valid for a request"""
        return not url or not is_url(url)

    def get(self, url: str):
        """Retrives the URL's content"""
        if self.is_valid_url(url):
            return None

        try:
            response = get(url, timeout=self.timeout)
            return response.content
        except:
            self.logger.log(t('ERRORS.GET_PAGE', {'url': url}))
            return None

    def get_parsed(self, url: str) -> Union[None, BeautifulSoup]:
        """Retrieves the URL content, parsed"""
        content = self.get(url)
        if not content:
            return None

        return self.parse_html(content)

    def parse_html(self, raw_html: str) -> BeautifulSoup:
        """Wraps the URL's content with BeautifulSoup"""
        return BeautifulSoup(raw_html, features=self.parser)

    def parse_img(self, img: Tag) -> str:
        """Gets the img's SRC content"""
        return img.get(self.src_attribute)

    def get_img(self, url: str) -> Union[bool, Any]:
        """Get the image's content"""
        if self.is_valid_url(url):
            return False

        try:
            img_content = get(url, stream=True, timeout=self.timeout)
            img_content.raw.decode_content = True
        except:
            self.logger.log(t('ERRORS.GET_IMG', {'url': url}))
            return False

        return img_content.raw
