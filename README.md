# maxsancheez.github.io

Source for my portfolio site: **https://maxsancheez.github.io**

Everything is generated from `projects.json` (Python standard library only):

```bash
python3 art.py     # draw tab banners and experience images into images/ (they use the page colors)
python3 build.py   # write index.html
```

- Tabs: About, Experience, Research, Tools, Contact. Links like `/#research` open a tab directly.
- Each card and experience row opens a detail panel. Mark one project per section with `"featured": true` to show it as the wide card on top.
- Add a project in `projects.json`; put its cover in `covers/<repo>.svg` (otherwise it gets a text tile).
- Set `"photo"` in `projects.json` (e.g. `images/headshot.jpg`) to replace the MS monogram.
- `qr.svg` / `qr.png` point to https://maxsancheez.github.io (for the CV).
