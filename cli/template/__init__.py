"""
Example init
"""

# types
from scripts.types import ScrapeProps
# constants
from scripts.constants import EVERYTHING
# scraper
from scripts.webscrapper import start
# config
from .config import CONFIG


def init() -> None:
    """Start the download"""
    scrape_props: ScrapeProps = {
        'start_at': 1,
        'limit_chapters': EVERYTHING,
        'detect_corrupt': True,
    }
    start(CONFIG, scrape_props)


if __name__ == '__main__':
    init()
