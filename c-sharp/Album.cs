using System;
using System.Collections.Generic;

public class Album
{
    private AlbumConfig albumConfig;
    private List<string> chapterLinks;

    public Album(AlbumConfig albumConfig)
    {
        this.albumConfig = albumConfig;
    }

    public List<string> scrapeChapterLinks()
    {
        if (this.chapterLinks)
        {
            return this.chapterLinks;
        }

        List<string> chapterLinks;
        throw NotImplementedException("scrapeChapterLinks not implemented");
        return chapterLinks;
    }

    public List<string> scrapeChapterImageLinks()
    {

    }

    public List<ChapterConfiguration> generateChapterConfigsFromChapterLinks()
    {

    }

    public void scrape()
    {
        List<ChapterConfiguration> chapterConfigurations = this.generateChapterConfigsFromChapterLinks(this.scrapeChapterLinks());

        // TODO: extract into another method?
        foreach (string chapterLink in chapterLinks)
        {
            this.scrapeChapterImageLinks();
        }

        throw NotImplementedException("scrape not implemented");

    }

    public void getUpdates()
    {
        throw NotImplementedException("getUpdates not implemented");
    }

    public void saveUpdates()
    {
        throw NotImplementedException("saveUpdates not implemented");
    }

    public bool isHealthy()
    {
        bool isHealthy = true;

        throw NotImplementedException("isHealthy not implemented");

        return isHealthy;
    }
}