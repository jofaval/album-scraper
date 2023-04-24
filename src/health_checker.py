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
    logging.info(
        "%s:\n%s",
        label,
        '\n'.join((str(detail) for detail in details))
    )


class HealthChecker():
    """Checks the health of a given album"""
    config: AlbumConfig

    def __init__(self, config: AlbumConfig) -> None:
        self.config = config

    def get_missing_images(self, chapter_images: List[str]) -> List[int]:
        """Checks inconsistency in the number series and returns if there's inconsistency"""
        raw_images_indices = map(
            lambda x: os.path.basename(x).split(".")[0].split("-")[0],
            chapter_images
        )
        only_numeric_images_indices = filter(
            lambda chapter_raw_index: chapter_raw_index.isnumeric(),
            raw_images_indices
        )
        set_of_images_indices = set(map(int, only_numeric_images_indices))
        list_of_images_indices = list(set_of_images_indices)

        actual_range_of_images = set(range(
            self.config.starting_health_check_image_index,
            list_of_images_indices[-1] + 1
        ))
        del list_of_images_indices

        missing_images = list(
            set_of_images_indices.difference(actual_range_of_images)
        )

        return missing_images

    def get_corrupt_image_sizes(self, chapter_images: List[str]) -> List[str]:
        """Checks that the images have an adequate size"""
        return list(filter(
            lambda chapter_image: os.path.getsize(chapter_image) <= 0,
            chapter_images
        ))

    def get_chapter_images(self, chapter_config: ChapterConfig) -> List[str]:
        """Gets all the images from the given chapter"""
        chapter_path = chapter_config.generate_chapter_path()
        return [
            join(chapter_path, image_file)
            for image_file in listdir(chapter_path)
            if isfile(join(chapter_path, image_file))
        ]

    def is_chapter_healthy(self, chapter_config: ChapterConfig) -> bool:
        """Check the health of the given chapter"""
        images = self.get_chapter_images(chapter_config)

        # TODO: print anywhere else the number of missing images, or store it
        corrupt_number_series = self.get_missing_images(images)
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
        corrupt_images = self.get_corrupt_image_sizes(images)
        if corrupt_images:
            logging.warning(
                "Chapter \"%s\" has %d corrupt images",
                chapter_config.chapter_path,
                len(corrupt_images)
            )
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

    def get_chapters_configs(self) -> List[ChapterConfig]:
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

    def get_missing_chapters(self) -> List[int]:
        """Returns the missing chapters of the album"""
        set_of_chapter_indices = set((
            int(os.path.basename(chapter_config.chapter_path).split("-")[0])
            for chapter_config in self.get_chapters_configs()
        ))
        list_of_chapter_indices = list(set_of_chapter_indices)

        actual_range_of_chapters = set(range(
            self.config.starting_health_check_chapter_index,
            list_of_chapter_indices[-1] + 1
        ))
        del list_of_chapter_indices

        missing_chapters = list(
            set_of_chapter_indices.difference(actual_range_of_chapters)
        )
        return missing_chapters

    def are_there_unhealthy_chapters(self) -> List[ChapterConfig]:
        """Get all of the unhealthy chapters"""
        unhealthy_chapters = [
            chapter_config
            for chapter_config in self.get_chapters_configs()
            if not self.is_chapter_healthy(chapter_config)
        ]

        logging.warning(
            "%d unhealthy chapter(s) were detected",
            len(unhealthy_chapters)
        )
        if unhealthy_chapters:
            log_health_details_list(
                "Unhealthy chapters",
                (chapter.chapter_path for chapter in unhealthy_chapters)
            )

        return bool(unhealthy_chapters)

    def are_there_missing_chapters(self) -> List[int]:
        """Check if there are any missing chapters"""
        missing_chapters = self.get_missing_chapters()

        logging.warning(
            "%d missing chapter(s) were detected",
            len(missing_chapters)
        )
        if missing_chapters:
            log_health_details_list("Missing chapters", missing_chapters)

        return bool(missing_chapters)

    def is_album_healthy(self) -> bool:
        """Checks the health of the given album"""
        missing_chapters = self.are_there_missing_chapters()
        unhealthy_chapters = self.are_there_unhealthy_chapters()

        return not missing_chapters and not unhealthy_chapters
