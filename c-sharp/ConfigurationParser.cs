using System;
using System.Globalization;
using System.IO;

public class ConfigurationParser<ConfigurationType>
{
    private static ConfigurationType parseXml(string content)
    {
        throw new NotImplementedException(message: "parseXml not implemented");
    }

    private static ConfigurationType parseYaml(string content)
    {
        throw new NotImplementedException(message: "parseYaml not implemented");
    }

    private static ConfigurationType parseJson(string content)
    {
        throw new NotImplementedException(message: "parseJson not implemented");
    }

    private static string readFileContents(string filename)
    {
        string content = "";
        throw new NotImplementedException(message: "readFileContents");
        return content;
    }

    public static string getFileExtension(string filename)
    {
        return System.IO.Path.GetExtension(path: filename).ToLower();
    }

    private static Func getParserFromExtension(string extension)
    {
        if (extension == "yaml")
        {
            extension = "yml";
        }

        var parser = extension switch
        {
            "yml" => parseYaml,
            "xml" => parseXml,
            "json" => parseJson,
        };

        if (!parser)
        {
            throw new Exception($"Extension \"{extension}\" is not valid for a configuration");
        }

        return parser;
    }

    public static ConfigurationType parseConfiguration(string filename)
    {
        if (!System.IO.Path.Exists(path: filename))
        {
            throw new FileNotFoundException($"{filename} was not found");
        }

        string extension = getFileExtension(filename);
        Func parser = getParserFromExtension(extension);

        string content = readFileContents(filename);

        return parser(content);
    }
}