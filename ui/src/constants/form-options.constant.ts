import { FormSectionConfiguration } from "~/types/form.type";

export const FORM_OPTIONS: Record<
  FormSectionConfiguration["slug"],
  FormSectionConfiguration
> = {
  required: {
    title: "Base configuration",
    slug: "required",
    inputs: [
      // { slug: "albumPath", type: "text" },
      { slug: "chapterEnd", type: "numeric" },
      { slug: "chapterIndexLen", type: "numeric" },
      { slug: "chapterLinkQuery", type: "text" },
      { slug: "imageSourceQuery", type: "text" },
      { slug: "isReverseOrder", type: "check", checked: true },
      { slug: "slug", type: "text" },
      { slug: "startingUrl", type: "text" },
    ],
  },
  advanced: {
    title: "Advanced settings",
    slug: "advanced",
    inputs: [
      { slug: "chapterIndices", type: "text" },
      { slug: "chapterStart", type: "numeric" },
      { slug: "downloadDir", type: "text" },
      { slug: "getChapterIndex", type: "text" },
      { slug: "getChapterName", type: "text" },
      { slug: "getLinkFromTag", type: "text" },
      { slug: "getSourceFromTag", type: "text" },
      { slug: "imageIndexLen", type: "numeric" },
      {
        slug: "loggingLevel",
        type: "select",
        options: [{ id: "", value: "" }],
      },
      { slug: "maxChapterWorkers", type: "numeric" },
      { slug: "maxImageProcesses", type: "numeric" },
      { slug: "maxRetryAttemptsPerChapter", type: "numeric" },
      { slug: "maxRetryAttemptsPerImage", type: "numeric" },
      { slug: "shouldCheckHealth", type: "check", checked: true },
      { slug: "shouldDetectUpdates", type: "check", checked: true },
      { slug: "shouldDownloadUpdates", type: "check", checked: true },
      { slug: "shouldRetryChapters", type: "check", checked: true },
      { slug: "shouldRetryImages", type: "check", checked: true },
      { slug: "shouldScrape", type: "check", checked: true },
      { slug: "startingHealthCheckChapterIndex", type: "numeric" },
      { slug: "startingHealthCheckImageIndex", type: "numeric" },
      { slug: "useSlugOnDownloadPath", type: "check", checked: true },
    ],
  },
};
