# ANZCA Final Companion (PWA)

Offline-first study app. Opens in any browser and installs to the home screen. Progress, written answers and recordings are stored on the device (IndexedDB). Study content lives in `content/`.

## Adding or updating a set
1. Put the set in `content/set-N.json`. Copy the shape of `content/set-11.json`: `{num, title, note, items:[{id,type,...}]}`.
   Item types: `learn` (title, priority, los, body), `retrieve` (title, priority, los, topics, q, a), `speak` (title, sub, eyebrow, priority, los, target, q, a), `saq`, `viva`, `los` (groups), `trials` (body), `refs` (body), `docs` (body, shows under Professional Documents).
   Markdown subset: `##`/`###` headings, `- ` bullets, `> ` callouts, pipe tables, `**bold**`, links.
2. Run `python3 tools/build_index.py`. It checks the set, refreshes counts and rebuilds `content/index.json`.
3. In `sw.js` change `VERSION` (for example `v2`) so devices pick up the new files.
4. Commit and push. The site updates; devices get the new set the next time they open the app online.

## Run locally
`python3 -m http.server 8123` then open http://localhost:8123

## Not built yet
Cross-device sync (planned: Firebase, local-first, last-write-wins per item). Until then use Data, Back up progress, to move progress between devices.
