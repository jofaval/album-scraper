# system
from os.path import join
# constants
from ..constants import EVERYTHING
# types
from typing import List, Union
from pydantic import BaseModel
from logger import Logger
from ..utils import Requester
from bs4 import Tag
from ..models.album import Album
# models
from .image import Image
# utils
from validators import url as is_url
from ..utils import check_folder_or_create, pad
# translator
from ..lang import t


class Chapter(BaseModel):
    """An instance of an album chapter"""
    images: List[Image]
    index: int
    should_be_indexed: bool
    url: str
    base_url: str
    url_separator: str
    extra_title: str
    base_dir: str
    folder_name: str
    chapters_folder_name: str
    domain: str
    logger: Logger
    title: str
    requester: Requester
    chapter_img_query: str
    images: List[Image]
    album: Album

    def get_parsed_chapter_url(self) -> Union[str, None]:
        parsed_url = self.url

        # attempts to add the domain, if not already provided
        if not is_url(parsed_url):
            if self.domain.endswith(self.url_separator):
                parsed_url = self.domain + parsed_url
            else:
                parsed_url = f'{self.domain}{self.url_separator}{parsed_url}'

        if not is_url(parsed_url):
            self.logger.log(t('ERRORS.INVALID_CHAPTER_URL', {
                'chapter_url': parsed_url
            }))
            return None

        return parsed_url

    def parse_image(self, image: Tag, index: int) -> Image:
        parsed = self.requester.parse_img(image)
        transformed = Image(
            url_separator=self.url_separator,
            logger=self.logger,
            index=index,
            url=parsed,
            chapter=self,
            extension=self.album.configuration['FILE_EXTENSION'],
            requester=self.requester,
        )

        return transformed

    def scrape(self, images_limit: int = EVERYTHING) -> None:
        """"""
        parsed_url = self.get_parsed_chapter_url()
        if not parsed_url:
            return

        self.logger.log(t('CHAPTERS.CHAPTER_DOWNLOAD_STARTS', {
            'chapter_url': parsed_url
        }))

        soup = self.requester.get_parsed(parsed_url)

        img_tags = soup.select(self.chapter_img_query)
        if images_limit != EVERYTHING:
            img_tags = img_tags[:images_limit]

        check_folder_or_create(self.get_folder_name())

        self.images = [self.parse_image(img, index)
                       for index, img in enumerate(img_tags)]

        return self.images

    def get_images(self) -> List[Image]:
        """"""
        pass

    def check_health(self) -> Union[bool, List[str]]:
        """"""
        pass

    def get_title_name(self, should_rename: bool = False) -> str:
        if self.title:
            return self.title

        title = self.url
        for substring in [self.base_url, self.extra_title, self.url_separator]:
            title = title.replace(substring, '')

        if should_rename:
            title = f'{pad(self.index + 1)}-{title}'

        return title

    def get_folder_name(self) -> str:
        """"""
        if self.folder_name:
            return self.folder_name

        return join(self.base_dir, self.chapters_folder_name, self.get_title_name())

    pass
