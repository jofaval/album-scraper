"""
Album model

Contains Chapters
"""

# system
from os.path import join
# multiprocessing
from multiprocessing import Pool, cpu_count
# types
from typing import Generator, List
from pydantic import BaseModel
from ..logger import Logger
from ..utils import Requester
from .album_types import ChapterScraperThread, ImageDownloadThread
# constants
from ..constants import END_OF_LINE, EVERYTHING
# custom
from ..config.type import ConfigType
# models
from .chapter import Chapter
from .image import Image
# translator
from ..lang import t
# utils
from ..utils.system import check_folder_or_create, cls


class Album(BaseModel):
    """An instance of an Album"""
    chapters: List[Chapter]
    images: List[Image]
    configuration: ConfigType
    logger: Logger
    requester: Requester
    base_url: str
    chapters_query: str
    url_separator: str
    processes: int = cpu_count() - 1

    def scrape_all_chapters(self, start_at: int, is_reversed: bool = True) -> List[str]:
        """Get a list of all the chapters"""
        self.logger.log(t('CHAPTERS.GET_ALL', {'start_at': start_at}))
        soup = self.requester.get_parsed(self.base_url)

        chapter_a_tags = soup.select(self.chapters_query)
        # reverse the order, first becomes last, and so on and so forth
        if is_reversed:
            chapter_a_tags = chapter_a_tags[::-1]
        chapter_links = [a['href'] for a in chapter_a_tags[(start_at - 1):]]

        return chapter_links

    def prepare(self) -> None:
        """Initializes the Album configuration"""
        cls()

        check_folder_or_create(self.configuration['BASE_DIR'])
        check_folder_or_create(
            join(self.configuration['BASE_DIR'],
                 self.configuration['CHAPTERS_FOLDER'])
        )

        # TODO: 21:22 29/11/2022 complete
        # self.logger = Logger()
        # self.requester = Requester()

    def parse_chapter(self, url: str) -> Chapter:
        """Creates a chapter instance from a given URL"""
        # TODO: implement parsing

    def get_chapter_links(
        self, chapter_links: List[str],
        start_at: int,
        is_reversed: bool,
        limit_chapters: int,
    ) -> List[str]:
        """Discriminates the chapters links source"""
        if chapter_links is None:
            chapter_links = self.scrape_all_chapters(start_at, is_reversed)
        if limit_chapters != EVERYTHING:
            chapter_links = chapter_links[:limit_chapters]

        return chapter_links

    def get_all_chapters_images(self) -> List[Image]:
        """Gets all the images from all the chapters (locally)"""
        images = []

        for chapter in self.chapters:
            images.extend(chapter.get_images())

        return images

    def start_scraping(
        self,
        start_at: int,
        is_reversed: bool = True,
        chapter_links: List[str] = None,
        limit_chapters: int = EVERYTHING,
        detect_corrupt: bool = True
    ) -> None:
        """Main entrypoint of the album flow"""
        self.prepare()

        chapter_links = self.get_chapter_links(
            chapter_links, start_at, is_reversed, limit_chapters
        )
        self.chapters = [self.parse_chapter(
            chapter) for chapter in chapter_links]

        self.logger.log(t('CHAPTERS.TOTAL_CHAPTERS_RETRIEVED', {
            'chapter_links': len(chapter_links)
        }))

        self.scrape_chapters()

        images = self.get_all_chapters_images()

        self.scrape_images(images)

        if detect_corrupt:
            incomplete_chapters = self.check_health()
            self.logger.log(t('CHAPTERS.TOTAL_CORRUPTED_CHAPTERS', {
                'total_incomplete_chapters': len(incomplete_chapters),
                'incomplete_chapters': END_OF_LINE.join(incomplete_chapters)
            }))

    def check_health(self) -> List[str]:
        """Checks the health of a given album"""
        return []

    def detect_updates(self) -> None:
        """Detects a desynchronization between the album and the downloads"""

    def thread_scrape_chapter(self, props: ChapterScraperThread) -> None:
        """Thread logic for a chapter scrape"""
        props['chapter'].scrape(props['imgs_per_chapter'])

    def scrape_chapters(self, imgs_per_chapter: int = EVERYTHING) -> None:
        """Scrapes all the chapters"""
        if not self.chapters:
            return

        with Pool(processes=self.processes) as pooler:
            pooler.map(self.thread_scrape_chapter, [
                {'chapter': chapter, 'imgs_per_chapter': imgs_per_chapter}
                for chapter in self.chapters
            ])

    def thread_download_image(self, props: ImageDownloadThread) -> None:
        """Thread logic for an image download"""
        percentage = '{0:.2%}'.format(
            (props['index'] + 1) / props['total_imgs']
        )

        img_name = props['image'].get_filename()
        success = props['image'].scrape()

        if not success:
            self.logger.log(
                t('ERRORS.IMAGE_DIDNT_DOWNLOAD', {'img': img_name})
            )
            props['not_downloaded'].append(img_name)

        if success and props['show_progress']:
            t('CHAPTERS.PROGRESS_PERCENTAGE', {
                'title': props['image'].chapter.get_title_name(),
                'percentage': percentage,
                'index': props['index'],
                'url_separator': self.url_separator,
                'total_imgs': props['total_imgs']
            })

    def parallelize_images_download(self, show_progress: bool, images: List[Image]) -> List[str]:
        """Parallelizes the bulk download of images"""
        not_downloaded = []

        parallelization_args: Generator[ImageDownloadThread] = (
            {'show_progress': show_progress,
             'image': image,
             'index': index,
             'total_imgs': len(images),
             'not_downloaded': not_downloaded, }
            for index, image in enumerate(images)
        )

        # TODO: 20:06 29/11/2022 threadify inside each processor?
        with Pool(processes=self.processes) as pooler:
            pooler.map(self.thread_download_image, parallelization_args)

        return not_downloaded

    def scrape_images(self, images: List[Image], show_progress: bool = True) -> None:
        """Scrapes all of the chapter's images"""
        total_imgs = len(images)
        self.logger.log(t('IMAGES.FOUND_TOTAL_IMAGES', {
            'total_imgs': total_imgs
        }))

        not_downloaded = self.parallelize_images_download(
            show_progress=show_progress,
            images=images,
        )

        self.logger.log(t('IMAGES.IMAGES_DOWNLOADED'))

        if not_downloaded:
            self.logger.log('IMAGES.NOT_DOWNLOADED', {
                'not_downloaded': len(not_downloaded)
            })
