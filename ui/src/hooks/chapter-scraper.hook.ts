import { createSignal } from "solid-js";

export const [chapterUrls] = createSignal(new Set<string>());

function addChapterUrl(url: string): void {
  chapterUrls().add(url);
}

function getChapterUrls(): string[] {
  return Array.from(chapterUrls().values());
}

export type ChapterScraperHookResponse = {
  addChapterUrl: typeof addChapterUrl;
  getChapterUrls: typeof getChapterUrls;
};

export function useChapterScraper(): ChapterScraperHookResponse {
  return { addChapterUrl, getChapterUrls };
}
