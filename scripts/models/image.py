# types
from typing import List
from pydantic import BaseModel
# models
from .chapter import Chapter


class Image(BaseModel):
    """An instance of a Chapter's Image"""
    chapter: Chapter
    img_link: str

    def scrape_img(self) -> None:
        """"""
        pass

    def download_img(self) -> None:
        """"""
        pass

    pass
