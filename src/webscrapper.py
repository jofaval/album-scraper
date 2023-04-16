"""
Main entrypoint and workflow for the scraper
"""

import logging
import os

from album import Album
from album_config import AlbumConfig

# TODO: refactor into generators as much as possible for an efficient memory usage
# TODO: implement a detect updates, new chapters not found locally
# TODO: implement a health checker, missing images? missing values in a sorted list of ints
# TODO: implement a sanitizer, download those missing images
# TODO: implement a modular system with folders and configuration files


def start() -> None:
    """
    Starts all the processes

    Serves as the orchestrator for the scraping
    """
    def get_chapter_name(chapter_url: str) -> str:
        """Gets the chapter url"""
        if not chapter_url:
            return ""

        if chapter_url.endswith("/"):
            chapter_url = chapter_url[:-1]

        return chapter_url.split("/")[-1]

    # Example config
    album_config = AlbumConfig(
        slug="example",
        chapter_link_query=".chapters li a",
        starting_url="https://favorite-album.com/album/",
        is_reverse_order=True,
        get_chapter_name=get_chapter_name,
        image_source_query=".chapter_content img.chapter_img"
    )

    album = Album(album_config)

    try:
        album.scrape_chapters()
    except Exception as error:
        logging.exception("error %s", error)


if __name__ == "__main__":
    start()
