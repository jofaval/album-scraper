"""Chapter Config"""

# from multiprocessing import Pool
from typing import Callable, Union

from bs4 import BeautifulSoup
from pydantic import BaseModel

from src.album_config import AlbumConfig


class ChapterConfig(BaseModel):
    """All the necessary configuration for a chapter"""
    album: AlbumConfig
    """Album's configuration"""
    get_source_from_tag: Union[Callable[[BeautifulSoup], str], None]
    """Gets the source link, usually from an image tag"""
    image_source_query: str
    """CSS Query to retrieve all the images tags"""
    index: int
    """Chapter's index"""
    name: str
    """Chapter's name"""
    url: str
    """Chapter's url"""
