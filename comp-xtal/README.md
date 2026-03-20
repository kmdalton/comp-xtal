# CCTBX.XFEL handbook (static site)

This folder is a **plain static site** generated from Markdown in [`content/`](content/). There is no JavaScript framework—just HTML, CSS, a small search script, and a Python build step.

## Requirements

- **Python 3.10+** (3.12 recommended)

## Local installation

From this directory (`comp-xtal/comp-xtal/`):

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Build

Regenerate `index.html` from the Markdown sources:

```bash
.venv/bin/python build_handbook.py build
```

## Preview locally

Static sites need to be served over HTTP (not `file://`) so scripts behave consistently. From this directory:

```bash
python3 -m http.server 8080
```

Then open [http://localhost:8080](http://localhost:8080).

## Editing workflow

1. Change files under [`content/`](content/) (see [`content/README.md`](content/README.md) for format and manifest rules).
2. Run `build_handbook.py build`.
3. Commit **both** the Markdown changes and the updated `index.html` *or* rely on CI to build on push (see below).
4. If the handbook includes screenshots, commit the `images/` folder as well (see below).

### Figures and screenshots (from the PDF)

The first PDF → Markdown import (`import-pdf`) only captured **text**. Embedded screenshots live as separate image objects in the PDF.

To pull them out and attach them to each chapter (by PDF page / section mapping):

1. Put the handbook PDF at `../material/comp-xtal_stable_handbook.pdf`.
2. Run:

   ```bash
   .venv/bin/python build_handbook.py import-pdf-images
   .venv/bin/python build_handbook.py build
   ```

This **clears and repopulates** `images/`, then adds or replaces a `<!-- handbook-pdf-figures-begin -->` … `end` block at the bottom of each `content/*.md`. You can move or delete images in Markdown by hand afterward.

**Limits:** only **embedded raster** images are extracted. Anything drawn as pure vector/annotations in the PDF may not appear; for those, add PNGs manually under `images/` and reference them in Markdown.

---

## Hosting recommendations

| Approach | Best for |
|----------|-----------|
| **GitHub Pages** | Public handbook, zero hosting cost, integrates with Git PRs. **Recommended** for your use case. |
| **Netlify / Cloudflare Pages** | Same static output; connect the repo and set build command if you build in CI or on their runners. |
| **Internal web server** | Copy `index.html`, `styles.css`, and `search.js` to any static file host behind your org firewall. |

The site has **no server-side code**: deploy `index.html`, `styles.css`, `search.js`, and the `images/` directory when present (the GitHub Action copies them into `_site/`).

### GitHub Pages

Yes—you can host this on **GitHub Pages**.

1. Push this repository to GitHub (if it is not already).
2. In the repo: **Settings → Pages → Build and deployment → Source**: choose **GitHub Actions** (not “Deploy from a branch”).
3. Ensure the workflow file [`.github/workflows/handbook-pages.yml`](../../.github/workflows/handbook-pages.yml) exists at the **repository root** (as in this layout).
4. Push to `main`; the “Deploy handbook to GitHub Pages” workflow builds the HTML and publishes it.

Your site URL will look like:

`https://<user-or-org>.github.io/<repository>/`

**Repository layout note:** The workflow assumes the handbook project lives at `comp-xtal/comp-xtal/` inside the repo (matching this workspace). If you move the site to the repository root, edit the workflow paths and the `cp` step so they point at your `build_handbook.py` and copy `index.html`, `styles.css`, `search.js`, and optionally `images/` from the correct directory.

**First-time GitHub Pages:** After the first successful run, open **Settings → Pages** to confirm the published URL. If the workflow fails, check the Actions tab for logs (common issues: Pages not enabled, or workflow permissions).

### Optional: build only in CI

If you prefer **not** to commit `index.html`, you can stop tracking it and deploy **only** the artifact from GitHub Actions. That requires always using the workflow to publish (local preview would still run `build` locally). The workflow in this repo already builds on each push, so the published site stays aligned with `content/` even if you sometimes forget to run `build` before committing Markdown.

---

## One-time import from PDF

If you place a PDF at `../material/comp-xtal_stable_handbook.pdf` (relative to this folder), you can regenerate Markdown from it:

```bash
.venv/bin/python build_handbook.py import-pdf
```

This overwrites files under `content/` and `manifest.txt`. Use only when you intentionally want to reset editorial Markdown from PDF text.

To extract **images** from the same PDF without resetting the text, use `import-pdf-images` (see “Figures and screenshots” above).
