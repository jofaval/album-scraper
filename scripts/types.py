from dataclasses import dataclass
from typing import List, TypedDict


@dataclass
class ScrapeProps(TypedDict):
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
