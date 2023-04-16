"""Example"""

from album_config import AlbumConfig
from common_utilities import get_chapter_name

album_config = AlbumConfig(
    slug="example",
    chapter_link_query=".chapters li a",
    starting_url="https://favorite-album.com/album/",
    is_reverse_order=True,
    get_chapter_name=get_chapter_name,
    image_source_query=".chapter_content img.chapter_img"
)
