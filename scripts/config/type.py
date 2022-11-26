import threading
from typing import List, TypedDict


class ConfigType(TypedDict):
    DOMAIN: str
    """Domain of the target page to scrape"""
    BASE_URL: str
    """Base url from where to start scraping"""
    PARSER: str
    """BS4 parser, be wary of performance"""
    URL_SEPARATOR: str
    """It's usually "/" but you could change it if needed"""

    CHAPTER_IMG_QUERY: str
    """The CSS query to retrieve all the <img> elements"""
    CHAPTERS_FOLDER: str
    """The folder in which to store the chapters"""
    CHAPTERS_QUERY: str
    """The query to retrieve all the chapters from the main url"""

    EXTRA_TITLE_CONTENT: str
    """Is there any subfolder element to get the img? ex: domain.com/images/image-1.jpg"""
    FILE_EXTENSION: str
    """Usually .jpg"""

    SHOULD_RENAME_IMAGES: bool
    """It's so that the downloded images are numeric and not the usual hash id (by usual, I mean somewhat common)"""

    THREADS: List[threading.Thread]
    """The array of threads, should be later deprecated for a queue or pool"""
    LIMIT_THREADS: int
    """The max amount of concurrent workers"""

    SEPARATOR: str
    """The image/files/names separator, usually a dot"""
    EVERYTHING: int
    """A constant to indicate the number to download up to infinity, and beyond ;)"""

    BASE_DIR: str
    """Base directory from which to store logs and chapters/imgs"""
    IMG_SRC_ATTRIBUTE: str
    """The attribute from which to retrieve the img's src, "src" by default"""
