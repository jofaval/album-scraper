"""Album Config"""

import logging
import os
from logging import _Level
from typing import Callable, Union

from bs4 import BeautifulSoup, Tag
from pydantic import BaseModel


class AlbumConfig(BaseModel):
    """All the necessary configuration for an album"""
    # album
    chapter_link_query: str
    """CSS query to get the chapters links"""
    download_dir: str = os.path.dirname(__file__)
    """The directory to download the album in, if it doesn't exist, it will create it"""
    get_link_from_tag: Union[Callable[[Tag], None], None]
    """Extracts the link from the chapter tag"""
    is_reverse_order: bool = True
    """Does it show first the latest chapters? If so, it's in reverse order"""
    slug: str
    """Filepath slug for the album"""
    starting_url: str
    """Base url from which to scrape the chapters links"""
    logging_level: _Level = logging.INFO
    """Desired logging level"""

    # chapters
    chapter_end: int = 1_000_000_000
    """Last chapter to scrape, it should be the desired end chapter"""
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
