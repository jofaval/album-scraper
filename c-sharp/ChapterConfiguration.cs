public class ChapterConfiguration
{
    private AlbumConfiguration albumConfiguration;
    private string url;
    private int index;

    public ChapterConfiguration(AlbumConfiguration albumConfiguration, string url, int index)
    {
        this.albumConfiguration = albumConfiguration;
        this.url = url;
        this.index = index;
    }
}