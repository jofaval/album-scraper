# types
from typing import List
from pydantic import BaseModel

# models
from .chapter import Chapter
from .image import Image


class Album(BaseModel):
    """An instance of an Album"""
    chapters: List[Chapter]
    images: List[Image]

    def scrape_all_chapters(self) -> List[str]:
        """Get a list of all the chapters"""
        pass

    def start(self) -> None:
        pass

    def check_health(self) -> None:
        pass

    def detct_updates(self) -> None:
        pass

    def scrape_chapters(self) -> None:
        pass

    pass
