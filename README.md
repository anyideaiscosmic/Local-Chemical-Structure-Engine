# Local-Chemical-Structure-Engine
A cross-platform tool that generates a 2D chemical structure image from a user-provided name (IUPAC or trivial). Name-to-structure conversion runs through a local backend (OPSIN for parsing, RDKit for 2D rendering) — no web search, no downloading images from the internet. Using architecture of single REST API backend and thin frontends per platform.

Deployment order: web first, then Windows/Mac desktop (Electron wrapping the web frontend), then mobile (PWA or native client hitting the same API).

Input: one chemical name per request.

Output: 2D structure image (format — PNG or SVG — still undecided).

Open items unresolved: batch input support, exact output format, handling of trivial/non-systematic names, online-hosted API vs fully offline bundled runtime.

On Progress
