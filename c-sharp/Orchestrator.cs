using System;
using Album;

public class Orchestrator
{
    private AlbumConfiguration albumConfiguration;
    private Album album;

    public void prepare(string configurationPath)
    {
        albumConfiguration = new AlbumConfiguration();
        // TODO: parse
        album = new Album(albumConfiguration);
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
        string configurationPath = "", // not implemented
        bool shouldScrapeChapters = true,
        bool shouldCheckHealth = false, // not implemented
        bool shouldDetectUpdates = false, // not implemented
        bool shouldDownloadUpdates = false // not implemented
    )
    {
        this.prepare(configurationPath);

        if (shouldDownloadUpdates && !shouldDetectUpdates)
        {
            throw new Exception(message: "No updates will be downloaded if they're not detected first... please,"
            + "enable the updates detection, or disable the updates downloads");
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