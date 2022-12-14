## CHANGELOG

The log of changes on the project/repository.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## 2022-12-14

### Fixed

- Reduced the number of cyclical imports

## 2022-11-30

### Added

- Add the pylint extension and styleguide

### Modified

- Implemented some rules over the codebase to satisfy Pylint's warnings

## 2022-11-29

### Added

- Translate the logger into a class with shared state
- Implement a Requested (name suggestable to changes)
- Images will now download in bulk after scraping them from the chapters
- Finally "finished" an example, a quick one at that
- Use Pool executor now instead of a manual Thread "queue"

### Modified

- Move a ton of logic into models
- Cleaned up the code

## 2022-11-27

### Added

- Base CLI concept
- Started the class component translation

### Modified

- The multilang imports and usage

## 2022-11-26

### Achieved

- Project started and repository initialized

### Added

- Base modularization scripts
- Translation utilities
- Config types
- Debug mode
- Logging
- Base UI scaffolding, solidjs
- Docs (readme and images), LICENSING and CHANGELOG
- Github Actions ci/cd workflow pipeline

## 2022-11-25

### Started

- Base modularization concept design

## 2022-11-20

### Modified

- Cleaned the code a little bit

## _[...]_

### _Iterations_

## 2022-11-5

## Achieved

- Started the project

## Added

- Webscraping per chapter system
- Bulk image downloading
- "Manual" Threading, without pool or queue
