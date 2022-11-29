from typing import Dict


STRINGS: Dict[str, str] = {
    'ERRORS': {
        'GET_PAGE': 'Could not retrieve content for page: {{url}}',
        'GET_IMG': 'Could not retrieve content for image: {{url}}',
        'INVALID_URL': 'Url for image "{{filename}}" not found or invalid, URL: {{url}}',
        'IMAGE_DIDNT_DOWNLOAD': 'Failed to download image {{img}}',
        'PARSE_ERROR': 'parse error',
        'CORRPUT_IMAGE_FOUND': 'Corrupt or missing image found {{chapter}} {{index}}{{extension}} {{filesize}})',
        'INVALID_CHAPTER_URL': 'The chapter URL "{{chapter_url}}" was not detected as valid, make sure it starts with http[s]://',
    },
    'CHAPTERS': {
        'GET_ALL': 'Attempts to retrieve all chapters, starting from: {{start_at}}',
        'CHAPTER_DOWNLOAD_STARTS': 'Chapter content {{chapter_url}} will be downloaded',
        # 'TOTAL_CHAPTERS_RETRIEVED': 'A total of {{total_chapter_links}} links have been retrieveds'
        'TOTAL_CHAPTERS_RETRIEVED': 'A total of {{chapter_links}} chapter(s) have been retrieved',
        'TOTAL_CORRUPTED_CHAPTERS': 'Incomplete or corrupt chapters {{total_incomplete_chapters}} chapter(s)\n {{incomplete_chapters}}',
        'CORRUPT_CHAPTERS_DETECTION':
        "|----------------------------------|\n"
            + "| Detección de capítulos corruptos |\n"
            + "|----------------------------------|\n",
        'PROGRESS_PERCENTAGE': 'Chapter download percentage ({{title}}), {{percentage}} ({{index}}{{URL_SEPARATOR}}{{total_imgs}})',
    },
    'IMAGES': {
        'IMAGE_SUCCESS': 'Downloaded image {{filename}}',
        'FOUND_TOTAL_IMAGES': 'Found {{total_imgs}} image(s)',
        'IMAGES_DOWNLOADED': 'All the images of the chapter have already been downloaded',
        'NOT_DOWNLOADED': 'Failed to download {{not_downloaded}} image(s)',
        'ANALYZING_IMAGES': 'Analyzing the images of the chapter {{chapter}}',
    },
    'THREADS': {
        'WAIT_ALL': 'Wait for the rest of the threads to finish',
    },
    'UPDATES': {
        'NEWS': "What\'s new is {{updates}}",
        'DOWNLOAD_PROMPT': "Download what's new? Yes=y:",
        'CHOSEN_OPTION': 'Option {{option}} chosen',
        'NOT_DOWNLOADING_NEWS': '\nNews will not be downloaded\n',
        'NEWS_DOWNLOADED': '\nThe news has been downloaded\n',
    }
}
