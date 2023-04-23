"""Chapter Config"""

# from multiprocessing import Pool
import os
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
    image_source_query: str = ""
    """CSS Query to retrieve all the images tags"""
    index: int
    """Chapter's index"""
    name: str
    """Chapter's name"""
    url: str
    """Chapter's url"""
    chapter_path: str = ""
    """[Internal] chapter's download path, automatically generated"""

    def generate_chapter_path(self) -> None:
        """Generates the path for the chapter"""
        if not self.chapter_path:
            chapter_index = str(self.index).zfill(self.album.chapter_index_len)
            self.chapter_path = os.path.join(
                self.album.album_path,
                f"{chapter_index}-{self.name}"
            )

        return self.chapter_path
