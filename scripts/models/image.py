# system
from shutil import copyfileobj
from os.path import join
# types
from typing import Any
from pydantic import BaseModel
from ..utils import Requester
from ..logger import Logger
# constants
from ..constants import DEFAULT_IMG_DOWNLOAD_RETRIES
# models
from .chapter import Chapter
# translator
from ..lang import t
# utils
from ..utils import pad

SINGLE_RETRY = 1


class Image(BaseModel):
    """An instance of a Chapter's Image"""
    chapter: Chapter
    url: str
    index: int
    should_be_renamed: bool
    logger: Logger
    requester: Requester
    extension: str

    def __init__(self, url_separator, logger, chapter, url, index, requester, extension, should_be_renamed=False):
        self.url_separator = url_separator
        self.logger = logger
        self.chapter = chapter
        self.url = url
        self.index = index
        self.should_be_renamed = should_be_renamed
        self.requester = requester
        self.extension = extension
        pass

    def scrape(self, retries: int = DEFAULT_IMG_DOWNLOAD_RETRIES) -> None:
        """"""
        success = False

        if retries > SINGLE_RETRY:
            success = self.download()
        else:
            success = self.download_with_retries(retries)

        return success

    def download(self) -> bool:
        """"""
        content = self.requester.get_img(self.url)

        if content == False:
            self.logger.log(
                t('ERRORS.INVALID_URL', {
                  'filename': self.get_filename(), 'url': self.url
                  }))
            return False

        return self.save(content)

    def download_with_retries(self, max_retries: int) -> bool:
        """"""
        for attempt in range(max_retries):
            self.logger.log(
                t('IMAGES.IMAGE_ATTEMPT', {'attempt': attempt + 1, 'max_retries': max_retries, 'url': self.url}))

            success = self.download()
            if success:
                return True

        return False

    def get_filename(self, should_rename: bool = True) -> str:
        """"""
        if self.url_separator not in self.url:
            return self.url

        start_at = self.url.rfind(self.url_separator) + 1
        filename = self.url[start_at:]

        if not should_rename:
            return filename

        return f'{pad(self.index + 1)}{self.extension}'

    def save(self, content: Any) -> bool:
        """"""
        try:
            with open(join(self.chapter.get_folder_name(), self.get_filename()), "wb") as img_file:
                copyfileobj(content.raw, img_file)

            self.logger.log(t('IMAGES.IMAGE_SUCCESS', {
                            'filename': self.get_filename()}))
            return True
        except:
            return False

    def is_healthy(self) -> bool:
        """"""
        pass

    pass
