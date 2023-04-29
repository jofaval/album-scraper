export const LoggingLevelEnum = {
  ALL: "all",
  DEBUG: "debug",
  INFO: "info",
  WARNING: "warning",
  ERROR: "error",
  CRITICAL: "critical",
} as const;

export type ObjectValues<T> = T[keyof T];

export type LoggingLevel = ObjectValues<typeof LoggingLevelEnum>;
