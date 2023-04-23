"""Album Config"""

import logging
import os
from typing import Callable, Union

from bs4 import BeautifulSoup, Tag
from pydantic import BaseModel


class AlbumConfig(BaseModel):
    """All the necessary configuration for an album"""
    # album
    album_path: str = ""
    """[Internal] album's download path, automatically generated"""
    chapter_link_query: str
    """CSS query to get the chapters links"""
    should_check_health: bool = True
    """Wether it will check a correct health within the local files"""
    should_detect_updates: bool = True
    """Will it check for non-downloaded chapters?"""
    download_dir: str = os.path.dirname(__file__)
    """The directory to download the album in, if it doesn't exist, it will create it"""
    download_updates: bool = True
    """Will it download those non-downloaded chapters?"""
    get_link_from_tag: Union[Callable[[Tag], None], None]
    """Extracts the link from the chapter tag"""
    is_reverse_order: bool = True
    """Does it show first the latest chapters? If so, it's in reverse order"""
    logging_level: int = logging.NOTSET
    """Desired logging level"""
    should_scrape: bool = True
    """Wether it will attempt to scrape or not"""
    slug: str
    """Filepath slug for the album"""
    starting_health_check_image_index: int = 0
    """Base starting index for an image"""
    starting_url: str
    """Base url from which to scrape the chapters links"""
    use_slug_on_download_path: bool = True
    """When generating the download path, will it use the slug"""

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
