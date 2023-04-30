using System;

public class AlbumConfiguration
{
    // TODO: create index-finder slug for a serializable configuration

    // album
    /// <summary>
    /// [Internal] album's download path, automatically generated
    /// </summary>
    public string albumPath;
    /// <summary>
    /// CSS query to get the chapters links
    /// </summary>
    public string chapterLinksQuery;
    /// <summary>
    /// Wether it will check a correct health within the local files
    /// </summary>
    public bool shouldCheckHealth;
    /// <summary>
    /// Will it check for non-downloaded chapters?
    /// </summary>
    public bool shouldDetectUpdates;
    /// <summary>
    /// The directory to download the album in, if it doesn't exist, it will create it
    /// </summary>
    public string downloadDir;
    /// <summary>
    /// Will it download those non-downloaded chapters?
    /// </summary>
    public bool shouldDownloadUpdates;
    /// <summary>
    /// Extracts the link from the chapter tag
    /// </summary>
    public Func<HTMLNode, Nullable> getLinkFromTag;
    /// <summary>
    /// Does it show first the latest chapters? If so, it's in reverse order
    /// </summary>
    public bool isReverseOrder;
    /// <summary>
    /// Desired logging level
    /// </summary>
    public int loggingLevel;
    /// <summary>
    /// Wether it will attempt to scrape or not
    /// </summary>
    public bool shouldScrape;
    /// <summary>
    /// Filepath slug for the album
    /// </summary>
    public string slug;
    /// <summary>
    /// Base starting index for an image
    /// </summary>
    public int startingHealthCheckImageIndex;
    /// <summary>
    /// Base starting index for a chapter
    /// </summary>
    public int startingHealthCheckChapterIndex;
    /// <summary>
    /// Base url from which to scrape the chapters links
    /// </summary>
    public string startingUrl;
    /// <summary>
    /// When generating the download path, will it use the slug
    /// </summary>
    public bool useSlugOnDownloadPath;
    /// <summary>
    /// Manual chapter indices to scrape
    /// </summary>
    public List<int> chapterIndices;

    // chapters
    /// <summary>
    /// Last chapter to scrape, it should be the desired end chapter
    /// </summary>
    public int chapterEnd;
    /// <summary>
    /// Length of the index in the filepath, e.g. 4 would be 0000-chapter-name
    /// </summary>
    public int chapterIndexLen;
    /// <summary>
    /// Start chapter to scrape
    /// </summary>
    public int chapterStart;
    /// <summary>
    /// Custom function for the chapter index extraction
    /// </summary>
    public Func<(string, int), int> getChapterIndex;
    /// <summary>
    /// Function to extrapolate the chapter's name from the url
    /// </summary>
    public Func<string, string> getChapterName;
    /// <summary>
    /// Maximum amount of concurrent threads for the chapter extraction
    /// </summary>
    public int maxChapterWorkers;
    /// <summary>
    /// Maximum amount of retries per chapter, when scraping image links
    /// </summary>
    public int maxRetryAttemptsPerChapter;
    /// <summary>
    /// Should it even retry at all?
    /// </summary>
    public bool shouldRetryChapters;

    // images
    /// <summary>
    /// Gets the source link, usually from an image tag
    /// </summary>
    public Func<HTMLNode, Nullable> getSourceFromTag;
    /// <summary>
    /// Length of the index in the filepath, e.g. 3 would be chapter-name/000.jpg
    /// </summary>
    public int imageIndexLen;
    /// <summary>
    /// CSS Query to retrieve all the images tags
    /// </summary>
    public string chapterImagesQuery;
    /// <summary>
    /// Maximum amount of processes to download the images
    /// </summary>
    public int maxImageProcesses;
    /// <summary>
    /// Maximum amount of retries per image, when downloading an image
    /// </summary>
    public int maxRetryAttemptsPerImage;
    /// <summary>
    /// Should it even retry at all?
    /// </summary>
    public bool shouldRetryImages;

    public AlbumConfiguration(string albumPath, string chapterLinksQuery, bool shouldCheckHealth, bool shouldDetectUpdates, string downloadDir, bool shouldDownloadUpdates, Func<HTMLNode, Nullable> getLinkFromTag, bool isReverseOrder, int loggingLevel, bool shouldScrape, string slug, int startingHealthCheckImageIndex, int startingHealthCheckChapterIndex, string startingUrl, bool useSlugOnDownloadPath, List<int> chapterIndices, int chapterEnd, int chapterIndexLen, int chapterStart, Func<(string, int), int> getChapterIndex, Func<string, string> getChapterName, int maxChapterWorkers, int maxRetryAttemptsPerChapter, bool shouldRetryChapters, Func<HTMLNode, Nullable> getSourceFromTag, int imageIndexLen, string chapterImagesQuery, int maxImageProcesses, int maxRetryAttemptsPerImage, bool shouldRetryImages)
    {
        this.albumPath = albumPath;
        this.chapterLinksQuery = chapterLinksQuery;
        this.shouldCheckHealth = shouldCheckHealth;
        this.shouldDetectUpdates = shouldDetectUpdates;
        this.downloadDir = downloadDir;
        this.shouldDownloadUpdates = shouldDownloadUpdates;
        this.getLinkFromTag = getLinkFromTag;
        this.isReverseOrder = isReverseOrder;
        this.loggingLevel = loggingLevel;
        this.shouldScrape = shouldScrape;
        this.slug = slug;
        this.startingHealthCheckImageIndex = startingHealthCheckImageIndex;
        this.startingHealthCheckChapterIndex = startingHealthCheckChapterIndex;
        this.startingUrl = startingUrl;
        this.useSlugOnDownloadPath = useSlugOnDownloadPath;
        this.chapterIndices = chapterIndices;
        this.chapterEnd = chapterEnd;
        this.chapterIndexLen = chapterIndexLen;
        this.chapterStart = chapterStart;
        this.getChapterIndex = getChapterIndex;
        this.getChapterName = getChapterName;
        this.maxChapterWorkers = maxChapterWorkers;
        this.maxRetryAttemptsPerChapter = maxRetryAttemptsPerChapter;
        this.shouldRetryChapters = shouldRetryChapters;
        this.getSourceFromTag = getSourceFromTag;
        this.imageIndexLen = imageIndexLen;
        this.chapterImagesQuery = chapterImagesQuery;
        this.maxImageProcesses = maxImageProcesses;
        this.maxRetryAttemptsPerImage = maxRetryAttemptsPerImage;
        this.shouldRetryImages = shouldRetryImages;
    }
}