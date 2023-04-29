import { ChapterConfiguration } from "./chapter-configuration.type";

/** All the necessary configuration for an image */
export type ImageConfiguration = {
  /** Image's index */
  index: number;
  /** Image's url */
  url: string;
  /** Chapter's configuration */
  chapter: ChapterConfiguration;
};
