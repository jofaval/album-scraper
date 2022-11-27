# types
from typing import List
from pydantic import BaseModel
# models
from .image import Image


class Chapter(BaseModel):
    """An instance of an album chapter"""
    images: List[Image]

    def scrape_chatper(self) -> None:
        pass

    def scrape_images(self) -> List[Image]:
        pass

    def check_health(self) -> bool or List[str]:
        pass

    pass
