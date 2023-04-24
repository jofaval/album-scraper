import { mount, StartClient } from "solid-start/entry-client";

// TODO: multi-lang options?
// TODO: implement a slug for index retrieval from the URL, no function should be passed there (eval should be avoided)
// so maybe it would be a viable solution to parse a string like /album-chapter-{index}-...

mount(() => <StartClient />, document);
