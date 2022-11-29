"""
Types for the album model
"""

# types
from dataclasses import dataclass
from typing import List, TypedDict
from .chapter import Chapter
from .image import Image


class ChapterScraperThread(TypedDict):
    """Props for the chapter scraping thread"""

    chapter: Chapter
    imgs_per_chapter: int


class ImageDownloadThread(TypedDict):
    """Props for the image download thread"""

    show_progress: bool
    image: Image
    index: int
    total_imgs: int
    not_downloaded: List[str]


@dataclass
class ScrapeProps(TypedDict):
    """Scrape initialization props"""

    start_at: int
    """The (human) index it will start looking for at, starts at 1"""

    limit_chapters: int
    """How many chapters to download? Every single one by default"""

    imgs_per_chapter: int
    """Is there a limit of imgs to download per chapter? Every single one by default"""

    chapter_links: List[str]
    """An array of the links from where to scrape, it won't search for chapters if any given"""

    detect_corrupt: bool
    """Should it do a sanity check after downloading it? It will by default"""
