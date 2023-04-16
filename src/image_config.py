"""Image Config"""

# from multiprocessing import Pool

from pydantic import BaseModel

from chapter_config import ChapterConfig


class ImageConfig(BaseModel):
    """All the necessary configuration for an image"""
    index: int
    """Image's index"""
    url: str
    """Image's url"""
    # TODO: include format?
    chapter: ChapterConfig
    """Chapter's configuration"""
