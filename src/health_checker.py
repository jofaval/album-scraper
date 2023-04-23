"""Health checker"""

import logging
import os
from typing import Generator, List

from src.album_config import AlbumConfig
from src.chapter_config import ChapterConfig


class HealthChecker():
    """Checks the health of a given album"""
    config: AlbumConfig

    def __init__(self, config: AlbumConfig) -> None:
        self.config = config

    def check_number_series(self, chapter_images: List[str]) -> bool:
        """Checks inconsistency in the number series and returns if there's inconsistency"""
        invalid_images: List[str] = []

        for index, image in enumerate(chapter_images):
            image_basename: str = os.path.basename(image)
            image_index = image_basename.split(".")[0].split("-")[0]
            actual_image_index = index + self.config.starting_health_check_image_index

            if not image_index.isnumeric() or int(image_index) != actual_image_index:
                invalid_images.append(image)

        return not invalid_images

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
        chapter_images: List[str] = []

        raise NotImplementedError("get_chapter_folders not implemented")

        return chapter_images

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

    def get_chapters_folders(self) -> List[str]:
        """Retrieves all of the chapter folders (locally)"""
        chapters_folders: List[str] = []

        raise NotImplementedError("get_chapter_folders not implemented")

        return chapters_folders

    def get_chapters_configs(self) -> Generator[ChapterConfig, None, None]:
        """Retrieves all of the chapter folders (locally)"""
        chapters_folders: List[str] = self.get_chapters_folders()

        raise NotImplementedError("get_chapters_configs not implemented")

        return (
            ChapterConfig()
            for chapter_folder in chapters_folders
        )

    def check(self) -> bool:
        """Checks the health of the given album"""
        chapters_configs = self.get_chapters_configs()
        unhealthy_chapters: List[ChapterConfig] = []

        for chapter_config in chapters_configs:
            is_chapter_healthy = self.check_health_of_chapter(chapter_config)
            if not is_chapter_healthy:
                unhealthy_chapters.append(chapter_config)

        return not unhealthy_chapters
