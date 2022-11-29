"""
Image model
"""

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
    should_be_renamed: bool = False
    logger: Logger
    requester: Requester
    extension: str

    def scrape(self, retries: int = DEFAULT_IMG_DOWNLOAD_RETRIES) -> None:
        """Scrape an image, wrapper for a download"""
        success = False

        if retries > SINGLE_RETRY:
            success = self.download()
        else:
            success = self.download_with_retries(retries)

        return success

    def download(self) -> bool:
        """Simple download functionality"""
        content = self.requester.get_img(self.url)

        if content is False:
            self.logger.log(
                t('ERRORS.INVALID_URL', {
                  'filename': self.get_filename(), 'url': self.url
                  }))
            return False

        return self.save(content)

    def download_with_retries(self, max_retries: int) -> bool:
        """Downloads with a fallback"""
        for attempt in range(max_retries):
            self.logger.log(t('IMAGES.IMAGE_ATTEMPT', {
                'attempt': attempt + 1,
                'max_retries': max_retries,
                'url': self.url,
            }))

            success = self.download()
            if success:
                return True

        return False

    def get_filename(self, should_rename: bool = True) -> str:
        """Gets the image's name"""
        if self.chapter.url_separator not in self.url:
            return self.url

        start_at = self.url.rfind(self.chapter.url_separator) + 1
        filename = self.url[start_at:]

        if not should_rename:
            return filename

        return f'{pad(self.index + 1)}{self.extension}'

    def save(self, content: Any) -> bool:
        """Saves the image physically"""
        try:
            with open(join(self.chapter.get_folder_name(), self.get_filename()), "wb") as img_file:
                copyfileobj(content.raw, img_file)

            self.logger.log(t('IMAGES.IMAGE_SUCCESS', {
                            'filename': self.get_filename()}))
            return True
        except Exception as ex:
            return False

    def is_healthy(self) -> bool:
        """Checks the image's health"""
