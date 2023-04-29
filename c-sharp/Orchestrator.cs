using System;
using Album;

public class Orchestrator
{
    private AlbumConfig albumConfig;
    private Album album;

    public Orchestrator(AlbumConfig albumConfig)
    {
        this.albumConfig = albumConfig;
    }

    public void prepare()
    {
        this.album = new Album(albumConfig);

    }

    public void scrapeChapters()
    {
        this.album.scrape();
    }

    public void detectUpdates(bool shouldDownloadUpdates)
    {
        this.album.getUpdates();

        if (shouldDownloadUpdates)
        {
            this.downloadUpdates();
        }
    }

    public void downloadUpdates()
    {
        this.album.saveUpdates();
    }

    public bool checkHealth()
    {
        bool isHealthy = this.album.isHealthy();
    }

    public void start(
        bool shouldScrapeChapters = true,
        bool shouldCheckHealth = false, // not implemented
        bool shouldDetectUpdates = false, // not implemented
        bool shouldDownloadUpdates = false // not implemented
    )
    {
        this.prepare();

        if (shouldDownloadUpdates && !shouldDetectUpdates)
        {
            System.Console.WriteLine("No updates will be downloaded if they're not detected first");

        }

        if (shouldScrapeChapters)
        {
            this.scrapeChapters();

        }

        if (shouldDetectUpdates)
        {
            this.detectUpdates(shouldDownloadUpdates);

        }

        if (shouldCheckHealth)
        {
            this.checkHealth();
        }
    }
}