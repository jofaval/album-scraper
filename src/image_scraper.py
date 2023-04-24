"""Image Scraper"""

import logging
import os
import shutil
# from multiprocessing import Pool
from typing import Union

import cchardet
from requests import Response, get

from src.image_config import ImageConfig


class ImageScraper():
    """Scrapes an image and properly retrieves it's metadata"""

    def save(self, content: str, image_path: str) -> None:
        """Writes the image into a file"""
        image_path_dir = os.path.dirname(image_path)
        if not os.path.exists(image_path_dir):
            try:
                os.makedirs(image_path_dir)
            except FileExistsError:
                logging.warning("Attempted to recreate dir %s", image_path_dir)

        try:
            if os.path.exists(image_path):
                os.remove(image_path)

            with open(image_path, 'wb') as writer:
                shutil.copyfileobj(content, writer)
        except Exception as error:
            logging.exception(
                "Could not save image %s, error: %s",
                image_path,
                error
            )

    def get_image_extension(self, img_format: str) -> str:
        """Parses the image format into an extension"""
        if img_format == "image/jpeg":
            return "jpg"
        if img_format == "image/png":
            return "png"

        return "jpg"

    def get_image_path(self, meta_image_name: str, config: ImageConfig, img_format: str) -> str:
        """Generates the image's final path"""
        image_index = str(config.index).zfill(
            config.chapter.album.image_index_len
        )

        extension = self.get_image_extension(img_format)
        # return f'{chapter_index}-{config.chapter.name}/{image_index}-{meta_image_name}'

        return os.path.join(config.chapter.generate_chapter_path(), f"{image_index}.{extension}")

    def get_image_content(self, config: ImageConfig) -> Union[Response, None]:
        """Downloads the image with retries"""
        # -1 implements a pseudo do-while
        max_retry = config.chapter.album.max_retry_attempts_per_image if config.chapter.album.should_retry_images else -1
        retry_attempt = 0

        while True:
            logging.info("Attempting image download for %s", config.url)
            if retry_attempt > 0:
                logging.info("Attempt number %d", retry_attempt)

            try:
                response = get(config.url, stream=True, timeout=30)
                if not response.ok:
                    logging.warning(
                        "%s failed download, might retry",
                        config.url
                    )
                    raise Exception(
                        "%s failed download, might retry",
                        config.url
                    )

                if not response.content:
                    raise Exception(
                        "No content was detected for %s",
                        config.url
                    )

                return response
            except Exception as error:
                logging.exception(error)
            finally:
                retry_attempt += 1
                if retry_attempt >= max_retry:
                    return None

    def scrape(self, config: ImageConfig) -> None:
        """Scrapes an image and writes it with metadata"""
        logging.info("Start scraper for image: %s", config.url)
        response = self.get_image_content(config)
        if not response or not response.ok:
            logging.warning("%s could not be downloaded", config.url)
            return None

        image_path = self.get_image_path(
            # TODO: properly detect the image name, or content-disposition
            # meta_image_name=config.url.split("/")[-1],
            meta_image_name="",
            config=config,
            img_format=response.headers.get("Content-Type")
        )

        logging.info("Attempting to save image %s %s", image_path, config.url)
        try:
            # TODO: implement base path
            self.save(response.raw, image_path)
            # TODO: implement proper threading with file as tuple space
        except Exception as error:
            logging.exception(
                "Image could not be saved %s %s, %s", image_path, config.url, error
            )
            return None

        logging.info("Image saved %s %s!!", image_path, config.url)
        return None
