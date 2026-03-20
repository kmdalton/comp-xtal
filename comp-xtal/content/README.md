# Handbook content (source of truth)

The HTML site is **generated** from the Markdown files in this folder. Edit these files (not `index.html`) and rebuild.

## Workflow

1. Edit one or more `NN-slug.md` files (see `manifest.txt` for order).
2. From the handbook directory (`comp-xtal/` at the repo root—the parent of this `content/` folder) run:
   ```bash
   python3 -m venv .venv          # first time only
   .venv/bin/pip install -r requirements.txt
   .venv/bin/python build_handbook.py build
   ```
3. Open `index.html` via a local server (e.g. `python3 -m http.server`) and refresh.

## File format

Each chapter is a Markdown file with YAML frontmatter:

```yaml
---
id: my-section-id
title: Human-readable section title
---

Your **Markdown** body here. Use normal paragraphs, lists, links, and fenced code blocks as needed.
```

- **id** — stable fragment for URLs (`#my-section-id`). Prefer kebab-case; keep it stable if others link to it.
- **title** — shown in the table of contents and as the section heading.

## Order

`manifest.txt` lists filenames **top to bottom**. To add a section:

1. Create `13-new-topic.md` (next number in sequence).
2. Append its filename to `manifest.txt`.
3. Run `build` again.

## Optional: re-import from a PDF

If you ever obtain a replacement PDF and want to **overwrite** generated Markdown from it, place it at `../material/comp-xtal_stable_handbook.pdf` and run:

```bash
.venv/bin/python build_handbook.py import-pdf
```

That will replace files under `content/` and `manifest.txt`. Use only when you intend to reset editorial Markdown from PDF text.

## Figures from the PDF

Screenshots are **not** included in `import-pdf` (text only). From the handbook directory (`comp-xtal/` at repo root), with the PDF in `../material/comp-xtal_stable_handbook.pdf`:

```bash
.venv/bin/python build_handbook.py import-pdf-images
.venv/bin/python build_handbook.py build
```

That fills `../images/` and appends a block delimited by `<!-- handbook-pdf-figures-begin -->` and `<!-- handbook-pdf-figures-end -->` in each chapter. You may edit captions, reorder, or remove images inside that block.

To add your own screenshots, put files under `../images/` and use `![](images/yourfile.png)` in the Markdown (paths are relative to the built `index.html`).
