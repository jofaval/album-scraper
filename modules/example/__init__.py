"""
Example module scrape entrypoint
"""

# types
from scripts.models.album_types import ScrapeProps
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
        # 'limit_chapters': 1,
        'detect_corrupt': True,
    }
    start(CONFIG, scrape_props)


if __name__ == '__main__':
    init()
