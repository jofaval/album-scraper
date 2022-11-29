# system
from os.path import join
# types
from pydantic import BaseModel

# constants
from ..constants import ENCODING, END_OF_LINE
from .constants import DEFAULT_EXTENSION, DEFAULT_FOLDER_NAME, DEFAULT_LOG_DATE_FORMAT, WRITE_MODE
# utils
from ..utils import check_folder_or_create, get_now_as_str


class Logger(BaseModel):
    current: str
    """Current instance of now (Date) in str"""

    joiner: str = '§'
    """The joiner character"""

    def __init__(
        self,
        base_dir: str,
        folder_name: str = DEFAULT_FOLDER_NAME,
        debug: bool = True,
        extension: str = DEFAULT_EXTENSION,
        log_date_format: str = DEFAULT_LOG_DATE_FORMAT,
        should_log: bool = True,
    ) -> None:
        self.current = None
        self.base_dir = base_dir
        self.folder_name = folder_name
        self.debug = debug
        self.extension = extension
        self.log_date_format = log_date_format
        self.should_log = should_log
        pass

    def get_log_path(self) -> str:
        if self.logs_path:
            return self.logs_path

        self.logs_path = join(self.base_dir, self.folder_name)
        check_folder_or_create(self.logs_path)
        return self.logs_path

    def get_filename(self) -> str:
        return join(self.get_log_path(), f'{self.current}{self.extension}')

    def parse_log_content(self, args) -> str:
        parsed_args = self.joiner.join(args)
        parsed_args = END_OF_LINE.join([
            f'[{get_now_as_str(self.log_date_format)}] - {line}'
            for line in parsed_args.split(END_OF_LINE)
        ])

        return parsed_args + END_OF_LINE

    def store(self, *args) -> None:
        with open(self.get_filename(), WRITE_MODE, encoding=ENCODING) as fw:
            fw.write(self.parse_log_content(args))

    def log(self, *args, display: bool = True) -> bool:
        """Logs information if we're in debug mode"""
        success = False

        if not self.should_log:
            return success

        if not self.current:
            self.current = get_now_as_str(self.log_date_format)

        try:
            self.store(*args)
            success = True
        except Exception as ex:
            self.store(str(ex))

        if self.debug and display:
            print(*args)

        return success

    pass