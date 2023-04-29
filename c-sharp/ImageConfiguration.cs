public class ImageConfiguration
{
    private ChapterConfiguration chapterConfiguration;
    private string url;
    private int index;

    public ImageConfiguration(ChapterConfiguration chapterConfiguration, string url, int index)
    {
        this.chapterConfiguration = chapterConfiguration;
        this.url = url;
        this.index = index;
    }
}