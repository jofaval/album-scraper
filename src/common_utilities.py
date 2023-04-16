"""Common utilities"""


def get_chapter_name(chapter_url: str) -> str:
    """Gets the chapter url"""
    if not chapter_url:
        return ""

    if chapter_url.endswith("/"):
        chapter_url = chapter_url[:-1]

    return chapter_url.split("/")[-1]
