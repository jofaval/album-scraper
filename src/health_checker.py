"""Health checker"""

import logging
import os
from os import listdir
from os.path import isfile, join
from typing import Any, Generator, List

from src.album_config import AlbumConfig
from src.chapter_config import ChapterConfig


def log_health_details_list(label: str, details: List[Any]) -> None:
    """Custom logging formatter for the Health checker"""
    logging.warning(
        "%s:\n%s",
        label,
        '\n'.join((str(detail) for detail in details))
    )


class HealthChecker():
    """Checks the health of a given album"""
    config: AlbumConfig

    def __init__(self, config: AlbumConfig) -> None:
        self.config = config

    def check_number_series(self, chapter_images: List[str]) -> List[int]:
        """Checks inconsistency in the number series and returns if there's inconsistency"""
        invalid_images: List[int] = []

        for index, image in enumerate(chapter_images):
            image_basename: str = os.path.basename(image)
            image_index = image_basename.split(".")[0].split("-")[0]
            actual_image_index = (index+len(invalid_images)) + \
                self.config.starting_health_check_image_index

            if not image_index.isnumeric() or int(image_index) != actual_image_index:
                invalid_images.append(actual_image_index)

        return invalid_images

    def check_images_size(self, chapter_images: List[str]) -> List[str]:
        """Checks that the images have an adequate size"""
        corrupt_images = [
            chapter_image
            for chapter_image in chapter_images
            if not os.path.exists(chapter_image) or os.path.getsize(chapter_image) <= 0
        ]

        return corrupt_images

    def get_chapter_images(self, chapter_config: ChapterConfig) -> List[str]:
        """Gets all the images from the given chapter"""
        chapter_path = chapter_config.generate_chapter_path()
        return [
            join(chapter_path, image_file)
            for image_file in listdir(chapter_path)
            if isfile(join(chapter_path, image_file))
        ]

    def check_health_of_chapter(self, chapter_config: ChapterConfig) -> bool:
        """Check the health of the given chapter"""
        images = self.get_chapter_images(chapter_config)

        # TODO: print anywhere else the number of missing images, or store it
        corrupt_number_series = self.check_number_series(images)
        if corrupt_number_series:
            logging.warning(
                "Chapter \"%s\" has an incomplete number of images, %d missing images",
                chapter_config.chapter_path,
                len(corrupt_number_series)
            )
            # TODO: use info logging
            logging.warning(corrupt_number_series)
            log_health_details_list("Missing images", corrupt_number_series)

        # TODO: print anywhere else the number of corrupt images, or store it
        corrupt_images = self.check_images_size(images)
        if corrupt_images:
            logging.warning(
                "Chapter \"%s\" has %d corrupt images",
                chapter_config.chapter_path,
                len(corrupt_images)
            )
            # TODO: use info logging
            log_health_details_list("Corrupt images", corrupt_images)

        is_healthy = not corrupt_number_series and not corrupt_images

        if not is_healthy:
            logging.warning("\n")

        return is_healthy

    def get_chapters_folders(self) -> Generator[str, None, None]:
        """Retrieves all of the chapter folders (locally)"""
        return (
            join(self.config.album_path, chapter_folder)
            for chapter_folder in listdir(self.config.album_path)
        )

    def get_chapters_configs(self) -> Generator[ChapterConfig, None, None]:
        """Retrieves all of the chapter folders (locally)"""
        chapters_folders = self.get_chapters_folders()

        return (
            ChapterConfig(
                album=self.config,
                index=index,
                name="",
                url="",
                chapter_path=chapter_folder
            )
            for index, chapter_folder in enumerate(chapters_folders)
        )

    def check(self) -> bool:
        """Checks the health of the given album"""
        chapters_configs = self.get_chapters_configs()

        unhealthy_chapters: List[ChapterConfig] = []
        # TODO: convert to set and check for non-repeated missing series, more error proof
        missing_chapters: List[int] = []

        for index, chapter_config in enumerate(chapters_configs):
            chapter_basename: str = os.path.basename(
                chapter_config.chapter_path
            )
            chapter_index = int(chapter_basename.split(
                "-")[0]) + self.config.starting_health_check_image_index

            if len(missing_chapters) + index != chapter_index:
                missing_chapters.append(len(missing_chapters) + index)

            is_chapter_healthy = self.check_health_of_chapter(chapter_config)
            if not is_chapter_healthy:
                unhealthy_chapters.append(chapter_config)

        logging.warning(
            "%d unhealthy chapter(s) were detected",
            len(unhealthy_chapters)
        )
        if unhealthy_chapters:
            # TODO: use info logging
            log_health_details_list(
                "Unhealthy chapters",
                (chapter.chapter_path for chapter in unhealthy_chapters)
            )
            return False

        logging.warning(
            "%d missing chapter(s) were detected",
            len(missing_chapters)
        )
        if missing_chapters:
            # TODO: use info logging
            log_health_details_list("Missing chapters", missing_chapters)

        return not unhealthy_chapters
