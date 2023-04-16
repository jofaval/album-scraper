"""
Main entrypoint and workflow for the scraper
"""

import logging

from album import Album

from .configs import album_config

# TODO: refactor into generators as much as possible for an efficient memory usage
# TODO: implement a detect updates, new chapters not found locally
# TODO: implement a health checker, missing images? missing values in a sorted list of ints
# TODO: implement a sanitizer, download those missing images
# TODO: implement a modular system with folders and configuration files
# TODO: log to file with dates
# TODO: implement a multilingual logging utility


def start() -> None:
    """
    Starts all the processes

    Serves as the orchestrator for the scraping
    """

    try:
        album = Album(album_config)
        album.scrape_chapters()
    except Exception as error:
        logging.exception("error %s", error)


if __name__ == "__main__":
    start()
