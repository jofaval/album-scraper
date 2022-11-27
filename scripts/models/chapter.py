# types
from typing import List, Union
from pydantic import BaseModel
# models
from .image import Image


class Chapter(BaseModel):
    """An instance of an album chapter"""
    images: List[Image]
    index: int
    should_be_indexed: bool

    def scrape_chatper(self) -> None:
        """"""
        pass

    def scrape_images(self) -> List[Image]:
        """"""
        pass

    def check_health(self) -> Union[bool, List[str]]:
        """"""
        pass

    def get_filename(self) -> str:
        """"""
        pass

    pass
