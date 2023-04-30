using System;
using System.Collections.Generic;

public class ChapterConfiguration : IComparable<ChapterConfiguration>
{
    public AlbumConfiguration albumConfiguration;
    public string url;
    public int index;
    public string name;
    public string path;

    public ChapterConfiguration(AlbumConfiguration albumConfiguration, string url, int index, string name)
    {
        this.albumConfiguration = albumConfiguration;
        this.url = url;
        this.index = index;
        this.name = name;
    }

    public override bool Equals(object obj)
    {
        return obj is ChapterConfiguration configuration && url == configuration.url;
    }

    public string GetChapterPath()
    {
        if (!this.path)
        {
            string chapterIndex = this.index.ToString(format: $"{new string(0, this.albumConfiguration.chapterIndexLen)}");
            this.path = System.IO.Path.Join(this.albumConfiguration.albumPath, $"{chapterIndex}-{this.name}");
        }

        return this.path;
    }

    public override int GetHashCode()
    {
        return HashCode.Combine(albumConfiguration, url, index, name, path);
    }

    public int CompareTo(object obj)
    {
        if (obj == null) return 1;

        ChapterConfiguration otherChapter = obj as ChapterConfiguration;
        if (otherChapter != null)
            return this.index.CompareTo(value: otherChapter.index);
        else
            throw new ArgumentException(message: "Object is not a Chapter");
    }
}