"""
Main entrypoint and workflow for the scraper
"""


from src.album import Album
from src.configs import album_config
from src.logger import get_logger

# TODO: refactor into generators as much as possible for an efficient memory usage
# TODO: implement a detect updates, new chapters not found locally
# TODO: implement a health checker, missing images? missing values in a sorted list of ints
# TODO: implement a sanitizer, download those missing images
# TODO: implement a modular system with folders and configuration files
# TODO: log to file
# TODO: implement a multilingual logging utility
# TODO: implement avoid/ignore slug
# TODO: write to (physical) log or simply store in memory, failed/corrupt chapters/images per chapter
# TODO: implement a single chapter download mode, with human number input? even better, a flag for human number input
# TODO: human number flag, wether an index starts at 0 or not (would start at 1)
# TODO: fix after a health checker error detection, requires a granular image download
# TODO: implement a manual image download per chapters?
# TODO: implement c-sharp solution at the root, in another source file, maybe called c-sharp, for maximum multithreading and resources profit


def start() -> None:
    """
    Starts all the processes

    Serves as the orchestrator for the scraping
    """

    try:
        album = Album(album_config)
        album.start()
    except Exception as error:
        get_logger().exception("error %s", error)


if __name__ == "__main__":
    raise UserWarning(
        "Incorrect usage: please, execute at the root of the project, `python .`"
    )
