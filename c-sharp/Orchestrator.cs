using System;

public class Orchestrator
{
    private AlbumConfiguration albumConfiguration;
    private Album album;

    private void Prepare(string configurationPath)
    {
        albumConfiguration = new AlbumConfiguration();
        // TODO: parse configuration
        album = new Album(albumConfiguration);
    }

    private void ScrapeChapters()
    {
        this.album.Scrape();
    }

    private void DetectUpdates(bool shouldDownloadUpdates)
    {
        this.album.GetUpdates();

        if (shouldDownloadUpdates)
        {
            this.downloadUpdates();
        }
    }

    private void DownloadUpdates()
    {
        this.album.SaveUpdates();
    }

    private bool CheckHealth()
    {
        bool isHealthy = this.album.IsHealthy();
    }

    public void Start(
        string configurationPath = "", // not implemented
        bool shouldScrapeChapters = true,
        bool shouldCheckHealth = false, // not implemented
        bool shouldDetectUpdates = false, // not implemented
        bool shouldDownloadUpdates = false // not implemented
    )
    {
        this.Prepare(configurationPath);

        if (shouldDownloadUpdates && !shouldDetectUpdates)
        {
            throw new Exception(message: "No updates will be downloaded if they're not detected first... please,"
            + "enable the updates detection, or disable the updates downloads");
        }

        if (shouldScrapeChapters)
        {
            this.ScrapeChapters();
        }

        if (shouldDetectUpdates)
        {
            this.DetectUpdates(shouldDownloadUpdates);
        }

        if (shouldCheckHealth)
        {
            this.CheckHealth();
        }
    }
}