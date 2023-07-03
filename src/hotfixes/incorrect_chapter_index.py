"""
Ad hoc hotfix for a folder renaming,
incorrect index retrieval
"""

import os
import shutil
from os.path import basename, dirname
from typing import List

from config import FILE_DIRECTORY, ZERO_FILL


def get_chapter_index(url: str, index: str) -> int:
    """Returns the chapter index"""
    raw_chapter_index = url.split("-")[-1]

    if raw_chapter_index.endswith("/"):
        raw_chapter_index = raw_chapter_index[:-1]

    try:
        return int(raw_chapter_index)
    except Exception:
        return index


def main():
    """Main flow of action"""
    chapters: List[str] = list(os.walk(FILE_DIRECTORY))[1:]

    for chapter in chapters:
        fullpath = chapter[0]

        chapter_name = "-".join(basename(fullpath).split("-")[1:])
        index = str(get_chapter_index(fullpath, None)).zfill(ZERO_FILL)
        new_name = f"{index}-{chapter_name}"

        new_fullpath = os.path.join(dirname(fullpath), new_name)

        print(fullpath, "->", new_fullpath)
        os.rename(fullpath, new_fullpath)


if __name__ == "__main__":
    main()
