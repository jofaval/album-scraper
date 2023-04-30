using System;
using System.Collections.Generic;

public class Album
{
    private AlbumConfiguration albumConfiguration;
    private List<string> chapterLinks = new List<string>();

    public Album(AlbumConfiguration albumConfiguration)
    {
        this.albumConfiguration = albumConfiguration;
    }

    private List<string> scrapeChapterLinks(bool force)
    {
        if (!force && this.chapterLinks.Count > 0)
        {
            return this.chapterLinks;
        }

        chapterLinks = new List<string>();
        string content = Scraper.scrape(url: albumConfiguration.startingUrl);

        var chapterLinkNodes = content.QuerySelectorAll(albumConfiguration.chapterLinksQuery);
        if (chapterLinkNodes == null)
        {
            throw new Exception(message: "No chapter links were found!!");
        }

        foreach (HtmlNode chapterLinkNode in chapterLinkNodes)
        {
            chapterLinks.Add(item: chapterLinkNode.GetAttributeValue("href", null));
        }

        return chapterLinks;
    }

    private List<string> scrapeChapterImageSources(ChapterConfiguration chapterConfiguration)
    {
        List<string> chapterImageSources = new List<string>();
        string content = Scraper.scrape(url: chapterConfiguration.url);

        var chapterImageSources = content.QuerySelectorAll(albumConfiguration.chapterImagesQuery);
        if (chapterImageSources == null)
        {
            throw new Exception(message: "No chapter images were found!!");
        }

        foreach (HtmlNode chapterImageNode in chapterImageNodes)
        {
            chapterImageSources.Add(item: chapterImageNode.GetAttributeValue("src", null));
        }

        return chapterImageSources;
    }

    private void scrapeChapterImages(List<ImageConfiguration> imageConfigurations)
    {
        foreach (ImageConfiguration imageConfiguration in imageConfigurations)
        {
            ChapterImageScraper.scrapeImage(imageConfiguration);
        }
    }

    private List<ImageConfiguration> generateImageConfigurations(List<ChapterConfiguration> chapterConfigurations)
    {
        List<ImageConfiguration> imageConfigurations = new List<ImageConfiguration>();
        for (int index = 0; index < chapterConfigurations.Count; index++)
        {
            generateImageConfigurationsFromChapter(imageConfigurations, index, chapterConfiguration: chapterConfigurations[index]);
        }

        return imageConfigurations;
    }

    private void generateImageConfigurationsFromChapter(List<ImageConfiguration> imageConfigurations, int index, ChapterConfiguration chapterConfiguration)
    {
        List<string> imageLinks = scrapeChapterImageSources(chapterConfiguration);
        for (int imageIndex = 0; imageIndex < imageLinks.Count; imageIndex++)
        {
            string imageLink = imageLinks[index: imageIndex];
            imageConfigurations.Add(item: new ImageConfiguration(chapterConfiguration, url: imageLink, index));
        }
    }

    private List<ChapterConfiguration> generateChapterConfigurations(List<string> chapterLinks)
    {
        List<ChapterConfiguration> chapterConfigurations = new List<ChapterConfiguration>();

        for (int chapterLinkIndex = 0; chapterLinkIndex < chapterLinks.Count; chapterLinkIndex++)
        {
            string chapterLink = chapterLinks[index: chapterLinkIndex];
            chapterConfigurations.Add(item: new ChapterConfiguration(albumConfiguration, url: chapterLink, index));
        }

        return chapterConfigurations;
    }

    public void scrape(bool forceScrape = false)
    {
        List<string> chapterLinks = scrapeChapterLinks(force: forceScrape);
        List<ChapterConfiguration> chapterConfigurations = generateChapterConfigurations(chapterLinks);
        // TODO: reverse order option
        List<ImageConfiguration> imageConfigurations = generateImageConfigurations(chapterConfigurations);
        // TODO: filter repeated URLs?! maybe not, but cache the image URL download?

        scrapeChapterImages(imageConfigurations);
    }

    public void getUpdates()
    {
        throw new NotImplementedException(message: "getUpdates not implemented");
    }

    public void saveUpdates()
    {
        throw new NotImplementedException(message: "saveUpdates not implemented");
    }

    public bool isHealthy()
    {
        bool isHealthy = true;

        throw new NotImplementedException(message: "isHealthy not implemented");

        return isHealthy;
    }
}