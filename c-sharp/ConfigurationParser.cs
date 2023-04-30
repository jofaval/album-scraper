using System;
using System.Globalization;
using System.IO;

public class ConfigurationParser<ConfigurationType>
{
    private static ConfigurationType ParseXml(string content)
    {
        throw new NotImplementedException(message: "parseXml not implemented");
    }

    private static ConfigurationType ParseYaml(string content)
    {
        throw new NotImplementedException(message: "parseYaml not implemented");
    }

    private static ConfigurationType ParseJson(string content)
    {
        throw new NotImplementedException(message: "parseJson not implemented");
    }

    private static string ReadFileContents(string filename)
    {
        string content = "";
        throw new NotImplementedException(message: "readFileContents");
        return content;
    }

    private static string GetFileExtension(string filename)
    {
        return System.IO.Path.GetExtension(path: filename).ToLower();
    }

    private static Func GetParserFromExtension(string extension)
    {
        if (extension == "yaml")
        {
            extension = "yml";
        }

        var parser = extension switch
        {
            "yml" => ParseYaml,
            "xml" => ParseXml,
            "json" => ParseJson,
        };

        if (!parser)
        {
            throw new Exception(message: $"Extension \"{extension}\" is not valid for a configuration");
        }

        return parser;
    }

    public static ConfigurationType Parse(string filename)
    {
        if (!System.IO.Path.Exists(path: filename))
        {
            throw new FileNotFoundException(message: $"{filename} was not found");
        }

        string extension = GetFileExtension(filename);
        Func parser = GetParserFromExtension(extension);

        string content = ReadFileContents(filename);

        return parser(content);
    }
}