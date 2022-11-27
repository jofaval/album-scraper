# types
from pydantic import BaseModel
# constants
from ..constants import DEFAULT_IMG_DOWNLOAD_RETRIES
# models
from .chapter import Chapter


class Image(BaseModel):
    """An instance of a Chapter's Image"""
    chapter: Chapter
    link: str
    index: int
    should_be_renamed: bool

    def scrape_img(self) -> None:
        """"""
        pass

    def download_img(self) -> None:
        """"""
        pass

    def download_img_with_retries(self, retries: int = DEFAULT_IMG_DOWNLOAD_RETRIES) -> None:
        """"""
        pass

    def get_filename(self) -> str:
        """"""
        pass

    def save_img(self) -> bool:
        """"""
        pass

    def is_healthy(self) -> bool:
        """"""
        pass

    pass
