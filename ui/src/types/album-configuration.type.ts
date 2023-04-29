import { LoggingLevel } from "./logging.type";

/** All the necessary configuration for an album */
export type AlbumConfiguration = {
  // album
  /** [Internal] album's download path, automatically generated */
  albumPath: string;
  /** CSS query to get the chapters links */
  chapterLinkQuery: string;
  /** Wether it will check a correct health within the local files */
  shouldCheckHealth: boolean;
  /** Will it check for non-downloaded chapters? */
  shouldDetectUpdates: boolean;
  /** The directory to download the album in, if it doesn't exist, it will create it */
  downloadDir: string;
  /** Will it download those non-downloaded chapters? */
  shouldDownloadUpdates: boolean;
  /** Extracts the link from the chapter tag */
  getLinkFromTag?: () => void;
  /** Does it show first the latest chapters? If so, it's in reverse order */
  isReverseOrder: boolean;
  /** Desired logging level */
  loggingLevel: LoggingLevel;
  /** Wether it will attempt to scrape or not */
  shouldScrape: boolean;
  /** Filepath slug for the album */
  slug: string;
  /** Base starting index for an image */
  startingHealthCheckImageIndex: number;
  /** Base starting index for a chapter */
  startingHealthCheckChapterIndex: number;
  /** Base url from which to scrape the chapters links */
  startingUrl: string;
  /** When generating the download path, will it use the slug */
  useSlugOnDownloadPath: boolean;
  /** Manual chapter indices to scrape */
  chapterIndices: number[];

  // chapters
  /** Last chapter to scrape, it should be the desired end chapter */
  chapterEnd: number;
  /** Length of the index in the filepath, e.g. 4 would be 0000-chapter-name */
  chapterIndexLen: number;
  /** Start chapter to scrape */
  chapterStart: number;
  /** Custom function for the chapter index extraction */
  getChapterIndex?: (url: string, index: number) => void;
  /** Function to extrapolate the chapter's name from the url */
  getChapterName: (url: string) => string;
  /** Maximum amount of concurrent threads for the chapter extraction */
  maxChapterWorkers: number;
  /** Maximum amount of retries per chapter, when scraping image links */
  maxRetryAttemptsPerChapter: number;
  /** Should it even retry at all? */
  shouldRetryChapters: boolean;

  // images
  /** Gets the source link, usually from an image tag */
  getSourceFromTag?: (element: HTMLElement) => string;
  /** Length of the index in the filepath, e.g. 3 would be chapter-name/000.jpg */
  imageIndexLen: number;
  /** CSS Query to retrieve all the images tags */
  imageSourceQuery: string;
  /** Maximum amount of processes to download the images */
  maxImageProcesses: number;
  /** Maximum amount of retries per image, when downloading an image */
  maxRetryAttemptsPerImage: number;
  /** Should it even retry at all? */
  shouldRetryImages: boolean;
};
