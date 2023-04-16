"""Health checker"""

import os
from typing import List

from album_config import AlbumConfig
from chapter_config import ChapterConfig


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

    def get_chapter_images(self, chapter_config: ChapterConfig) -> List[str]:
        """Gets all the images from the given chapter"""
        return []

    def check_health_of_chapter(self, chapter_config: ChapterConfig) -> bool:
        """Check the health of the given chapter"""
        images = self.get_chapter_images(chapter_config)
        return self.check_number_series(images)

    # TODO: check for inconsistency in chapters: 0001, 0002, 0003, 0005
