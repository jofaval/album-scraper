// @refresh reload
import { Suspense } from "solid-js";
import {
  Body,
  ErrorBoundary,
  FileRoutes,
  Head,
  Html,
  Meta,
  Routes,
  Scripts,
  Title,
} from "solid-start";
import "./root.css";

export default function Root() {
  return (
    <Html lang="en" class="">
      <Head>
        <Title>Album Scraper</Title>
        <Meta charset="utf-8" />
        <Meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>
      <Body class="bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 flex items-center p-5">
        <main class="text-center mx-auto text-gray-700 bg-slate-200 rounded drop-shadow-2xl w-full h-full">
          <h1 class="max-6-xs text-6xl font-bold text-sky-700 font-thin uppercase my-16">
            Album scraper
          </h1>

          <Suspense>
            <ErrorBoundary>
              <Routes>
                <FileRoutes />
              </Routes>
            </ErrorBoundary>
          </Suspense>
        </main>

        <Scripts />
      </Body>
    </Html>
  );
}
