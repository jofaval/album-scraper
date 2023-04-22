"""Health checker"""

import logging
import os
from typing import List

from src.album_config import AlbumConfig
from src.chapter_config import ChapterConfig


# TODO: instantiate as a configuration inside the album?
class HealthChecker():
    """Checks the health of a given album"""
    config: AlbumConfig

    def __init__(self, config: AlbumConfig) -> None:
        self.config = config

    def check_number_series(self, chapter_images: List[str]) -> bool:
        """Checks inconsistency in the number series and returns if there's inconsistency"""
        for index, image in enumerate(chapter_images):
            image_basename: str = os.path.basename(image)
            # TODO: there may be different image names, such as 000-zdmhqcmir.jpg
            image_index = image_basename.split(".")[0].split("-")[0]
            # TODO: starting index may differ from album to album, it should be a configuration

            try:
                if int(image_index) != index:
                    return True
            except SyntaxError:
                return True

        return False

    def check_images_size(self, chapter_images: List[str]) -> bool:
        """Checks that the images have an adequate size"""
        corrupt_images = [
            chapter_image
            for chapter_image in chapter_images
            if not os.path.exists(chapter_image) or os.path.getsize(chapter_image) <= 0
        ]

        return not corrupt_images

    def get_chapter_images(self, chapter_config: ChapterConfig) -> List[str]:
        """Gets all the images from the given chapter"""
        return []

    def check_health_of_chapter(self, chapter_config: ChapterConfig) -> bool:
        """Check the health of the given chapter"""
        images = self.get_chapter_images(chapter_config)

        if not self.check_number_series(images):
            logging.warning("Chapter %s has an incomplete number of images")
            # TODO: print anywhere else the number of missing images, or store it
            return False

        if not self.check_images_size(images):
            logging.warning("Chapter %s has a corrupt images")
            # TODO: print anywhere else the number of corrupt images, or store it
            return False

        return True

    # TODO: check for inconsistency in chapters: 0001, 0002, 0003, 0005
