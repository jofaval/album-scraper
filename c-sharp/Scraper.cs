using System;
using System.Net.Http;
using Fizzler;

public class Scraper
{
    private static (bool, TReturnType) withRetries<TReturnType>(Func<(bool, TReturnType)> execute, int retries = 3)
    {
        int retryAttempt = 0;

        do
        {
            retryAttempt++;

            try
            {
                (bool, TReturnType) success, output = execute();
                if (!success)
                {
                    continue;
                }

                return (true, output);
            }
            catch (System.Exception)
            {
                continue;
            }
        } while (retryAttempt < retries);

        return (false, null);
    }

    // TODO: properly type and download the Fizzler
    public static HtmlDocument scrape(string url, int retries)
    {
        (bool, string) success, content = withRetries<HtmlDocument>(execute: () =>
        {
            string content = await new HttpClient().GetStringAsync(url);
            if (!content)
            {
                return (false, null);
            }

            HtmlDocument html = new HtmlDocument();
            html.LoadHtml(content);
            return (true, html.DocumentNode);
        }, retries);

        if (!success)
        {
            throw new Exception(message: $"{url} could not be downloaded after {retries} retries");
        }

        return content;
    }
}