import { AlbumConfiguration } from "./album-configuration.type";

/** All the necessary configuration for a chapter */
export type ChapterConfiguration = {
  /** Album's configuration */
  album: AlbumConfiguration;
  /** Chapter's index */
  index: number;
  /** Chapter's url */
  url: string;
  /** Chapter's name */
  name: string;
  /** [Internal] chapter's download path, automatically generated */
  chapterPath?: string;
  // TODO: refactor into a common function that a chapter configuration could be passed to
  generateChapterPath: () => string;
};
