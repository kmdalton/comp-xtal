#!/usr/bin/env python3
"""Build static handbook from Markdown in content/. Optional one-time PDF import."""
from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

import markdown
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
MANIFEST = CONTENT / "manifest.txt"
OUT_HTML = ROOT / "index.html"
PDF = ROOT.parent / "material" / "comp-xtal_stable_handbook.pdf"

# Same anchors as the original PDF split (import only)
SECTIONS: list[tuple[str, str, str | None]] = [
    ("intro", "About this handbook", None),
    ("references", "Helpful references", "Helpful references"),
    (
        "preparation-remote-gui",
        "Preparation: Remote access to GUI",
        "✅Preparation: Remote access to GUI",
    ),
    (
        "basic-initial-gui",
        "Basic: Initial GUI configuration for an experiment",
        "✅Basic: Initial GUI configuration for an experiment",
    ),
    (
        "basic-programs-tasks",
        "Basic: CCTBX.XFEL Programs and Tasks",
        "✅ Basic: CCTBX.XFEL Programs and Tasks",
    ),
    (
        "intermediate-realtime-s3df",
        "Intermediate: Prepare for real-time usage during beamtime (S3DF)",
        "Intermediate: Prepare for real-time usage during \nbeamtime (S3DF) \nBefore the beamtime",
    ),
    (
        "intermediate-geometry-refinement",
        "Intermediate: Geometry Refinement",
        "✅ Intermediate: Geometry Refinement \ncctbx/dials understands",
    ),
    (
        "intermediate-mask",
        "Intermediate: How to make a mask",
        "✅ Intermediate: How to make a mask \nThis chapter assumes",
    ),
    (
        "intermediate-indexing",
        "Intermediate: Indexing result improvement",
        "Intermediate: Indexing result improvement \nDiagnostics",
    ),
    (
        "intermediate-photon-energy",
        "Intermediate: Photon energy calibration",
        "Intermediate: Photon energy calibration \nCorrect energy",
    ),
    (
        "advanced-event-code",
        "Advanced: Event code handling",
        "✅ Advanced: Event code handling \nHelpful past experiments",
    ),
    (
        "appendix-programs",
        "Appendix: relevant programs and parameters",
        "Appendix: relevant programs and parameters \nWhen tweaking PHIL",
    ),
    ("debugging-tips", "Debugging tips", "Debugging tips \nReview all the red warning"),
]

ORDERED_SLUGS = [s[0] for s in SECTIONS]
SLUG_TO_TITLE = {s[0]: s[1] for s in SECTIONS}

IMAGES_DIR = ROOT / "images"
FIG_BEGIN = "<!-- handbook-pdf-figures-begin -->"
FIG_END = "<!-- handbook-pdf-figures-end -->"
MIN_IMAGE_SIDE = 48


def soften_linebreaks(text: str) -> str:
    text = re.sub(r"-[ \t]*\n[ \t]*(?=[a-z])", "", text)
    text = re.sub(r"(?<=[a-z,)\]])[ \t]*\n[ \t]*(?=[a-z])", " ", text)
    text = re.sub(r"(?<=[,;])[ \t]*\n[ \t]*(?=\S)", " ", text)
    return text


def load_full_pdf_text() -> str:
    r = PdfReader(str(PDF))
    return "\n\n".join(page.extract_text() or "" for page in r.pages)


def split_pdf_sections(full: str) -> list[tuple[str, str, str]]:
    intro_end = full.find("Helpful references")
    if intro_end < 0:
        raise SystemExit("Could not find start of references section in PDF.")
    out: list[tuple[str, str, str]] = []
    out.append(("intro", SECTIONS[0][1], full[:intro_end]))

    positions: list[tuple[str, str, int]] = []
    for sid, title, anchor in SECTIONS[1:]:
        if anchor is None:
            continue
        pos = full.find(anchor)
        if pos < 0:
            raise SystemExit(f"Missing anchor for section {sid!r} in PDF.")
        positions.append((sid, title, pos))

    for i, (sid, title, start) in enumerate(positions):
        end = positions[i + 1][2] if i + 1 < len(positions) else len(full)
        out.append((sid, title, full[start:end]))
    return out


def strip_leading_title(body: str, title: str) -> str:
    body = body.lstrip()
    if not body:
        return body
    first_line = body.split("\n", 1)[0].strip()
    first_norm = re.sub(r"^✅\s*", "", first_line)
    if first_norm == title or first_norm.replace("  ", " ") == title:
        rest = body.split("\n", 1)[1] if "\n" in body else ""
        return rest.lstrip("\n")
    return body


def section_body_to_markdown(body: str, title: str) -> str:
    body = strip_leading_title(body, title)
    body = soften_linebreaks(body).strip()
    if not body:
        return ""
    chunks = re.split(r"\n\s*\n+", body)
    return "\n\n".join(c.strip() for c in chunks if c.strip())


def slug_to_filename(slug: str) -> str:
    idx = ORDERED_SLUGS.index(slug) + 1
    return f"{idx:02d}-{slug}.md"


def char_offset_to_page(page_texts: list[str], idx: int) -> int:
    """Map a character index in ``"\\n\\n".join(page_texts)`` to a 0-based page index."""
    sep = 2
    pos = 0
    for i, t in enumerate(page_texts):
        if idx < pos + len(t):
            return i
        pos += len(t)
        if i < len(page_texts) - 1:
            pos += sep
    return len(page_texts) - 1


def section_start_pages(page_texts: list[str]) -> dict[str, int]:
    """First PDF page index where each section anchor appears (pypdf text, same as import-pdf)."""
    full = "\n\n".join(page_texts)
    starts: dict[str, int] = {"intro": 0}
    search_from = 0
    for sid, _title, anchor in SECTIONS[1:]:
        if anchor is None:
            continue
        found = full.find(anchor, search_from)
        if found < 0:
            found = full.find(anchor.replace("\n", " "), search_from)
        if found < 0:
            raise SystemExit(f"import-pdf-images: anchor not found for section {sid!r}")
        starts[sid] = char_offset_to_page(page_texts, found)
        search_from = found + 1
    return starts


def page_section_for_index(page_num: int, starts: dict[str, int]) -> str:
    best_sid = "intro"
    best_p = -1
    for sid in ORDERED_SLUGS:
        sp = starts.get(sid)
        if sp is None:
            continue
        if sp <= page_num and sp >= best_p:
            best_sid = sid
            best_p = sp
    return best_sid


def inject_figures_markdown(md_path: Path, image_md_lines: list[str]) -> None:
    raw = md_path.read_text(encoding="utf-8")
    if not raw.startswith("---\n"):
        raise SystemExit(f"{md_path}: expected YAML frontmatter")
    end_fm = raw.find("\n---\n", 4)
    if end_fm < 0:
        raise SystemExit(f"{md_path}: unterminated frontmatter")
    head = raw[: end_fm + 5]
    body = raw[end_fm + 5 :]
    body = re.sub(
        r"\n*<!-- handbook-pdf-figures-begin -->.*?<!-- handbook-pdf-figures-end -->\s*",
        "\n\n",
        body,
        flags=re.DOTALL,
    )
    body = body.rstrip()
    if image_md_lines:
        body = (
            body
            + f"\n\n{FIG_BEGIN}\n\n### Figures (from PDF)\n\n"
            + "\n\n".join(image_md_lines)
            + f"\n\n{FIG_END}\n"
        )
    md_path.write_text(head + "\n" + body.lstrip("\n") + "\n", encoding="utf-8")


def cmd_import_pdf_images() -> None:
    """Extract embedded raster images from the PDF into images/ and inject Markdown figures."""
    try:
        import fitz  # PyMuPDF
    except ImportError as e:
        raise SystemExit("import-pdf-images requires pymupdf: pip install pymupdf") from e

    if not PDF.is_file():
        raise SystemExit(
            f"PDF not found: {PDF}\n"
            "Place comp-xtal_stable_handbook.pdf there, then run this command again."
        )

    r = PdfReader(str(PDF))
    page_texts = [(p.extract_text() or "") for p in r.pages]
    starts = section_start_pages(page_texts)

    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    for f in IMAGES_DIR.iterdir():
        if f.is_file():
            f.unlink()

    doc = fitz.open(str(PDF))
    try:
        if doc.page_count != len(page_texts):
            raise SystemExit("Page count mismatch between PyMuPDF and pypdf.")

        figure_lines: dict[str, list[str]] = {sid: [] for sid in ORDERED_SLUGS}
        per_section_count: dict[str, int] = {sid: 0 for sid in ORDERED_SLUGS}
        seen_page_xref: set[tuple[int, int]] = set()
        total = 0

        for page_index in range(doc.page_count):
            page = doc.load_page(page_index)
            sid = page_section_for_index(page_index, starts)
            for img in page.get_images(full=True):
                xref = img[0]
                w, h = img[2], img[3]
                if w < MIN_IMAGE_SIDE or h < MIN_IMAGE_SIDE:
                    continue
                key = (page_index, xref)
                if key in seen_page_xref:
                    continue
                seen_page_xref.add(key)
                try:
                    info = doc.extract_image(xref)
                except (ValueError, RuntimeError):
                    continue
                raw_bytes = info["image"]
                ext = info.get("ext", "png")
                if ext == "jpeg":
                    ext = "jpg"
                per_section_count[sid] += 1
                n = per_section_count[sid]
                fname = f"{sid}_p{page_index + 1:02d}_{n:02d}.{ext}"
                (IMAGES_DIR / fname).write_bytes(raw_bytes)
                alt = f"PDF p.{page_index + 1} fig.{n}"
                figure_lines[sid].append(f"![{alt}](images/{fname})")
                total += 1
    finally:
        doc.close()

    for sid in ORDERED_SLUGS:
        inject_figures_markdown(CONTENT / slug_to_filename(sid), figure_lines[sid])

    print(f"Wrote {total} image(s) under {IMAGES_DIR}/ and updated Markdown figure blocks.")


def cmd_import_pdf() -> None:
    if not PDF.is_file():
        raise SystemExit(f"PDF not found: {PDF}")
    CONTENT.mkdir(parents=True, exist_ok=True)
    full = load_full_pdf_text()
    sections = split_pdf_sections(full)
    lines: list[str] = []
    for sid, title, body in sections:
        fn = slug_to_filename(sid)
        lines.append(fn)
        md_body = section_body_to_markdown(body, title)
        text = f"---\nid: {sid}\ntitle: {title}\n---\n\n{md_body}\n"
        (CONTENT / fn).write_text(text, encoding="utf-8")
    MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(lines)} files under {CONTENT}/")


def parse_frontmatter(raw: str) -> tuple[dict[str, str], str]:
    if not raw.startswith("---\n"):
        return {}, raw
    end = raw.find("\n---\n", 4)
    if end < 0:
        return {}, raw
    block = raw[4:end]
    body = raw[end + 5 :]
    meta: dict[str, str] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, body


def load_manifest_files() -> list[Path]:
    if not MANIFEST.is_file():
        raise SystemExit(f"Missing {MANIFEST}. Run: python build_handbook.py import-pdf (once) or create manifest.")
    names = [ln.strip() for ln in MANIFEST.read_text(encoding="utf-8").splitlines() if ln.strip()]
    paths: list[Path] = []
    for name in names:
        p = CONTENT / name
        if not p.is_file():
            raise SystemExit(f"Manifest lists missing file: {p}")
        paths.append(p)
    return paths


MD_EXTENSIONS = ["extra", "sane_lists", "smarty"]


def md_to_html_fragment(source: str) -> str:
    return markdown.markdown(source, extensions=MD_EXTENSIONS)


def cmd_build() -> None:
    paths = load_manifest_files()
    sections: list[tuple[str, str, str]] = []
    for path in paths:
        raw = path.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(raw)
        sid = meta.get("id", "")
        title = meta.get("title", "")
        m = re.match(r"^(\d+)-(.+)\.md$", path.name)
        if not sid and m:
            sid = m.group(2)
        if not title and sid in SLUG_TO_TITLE:
            title = SLUG_TO_TITLE[sid]
        if not sid or not title:
            raise SystemExit(f"{path}: frontmatter must include id and title (or use known slug in filename).")
        body_html = md_to_html_fragment(body.strip())
        sections.append((sid, title, body_html))

    nav_items = "".join(
        f'        <li><a href="#{html.escape(sid, quote=True)}">{html.escape(title)}</a></li>\n'
        for sid, title, _ in sections
    )
    articles = []
    for sid, title, body_html in sections:
        articles.append(
            f'    <article id="{html.escape(sid, quote=True)}" class="section" '
            f'data-title="{html.escape(title, quote=True)}">\n'
            f"      <h2>{html.escape(title)}</h2>\n"
            f'      <div class="section-body">\n{body_html}\n      </div>\n'
            f"    </article>\n"
        )
    articles_html = "\n".join(articles)

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>CCTBX.XFEL handbook</title>
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <header class="top">
    <div class="top-inner">
      <h1 class="site-title">CCTBX.XFEL handbook</h1>
      <p class="site-sub">Source: Markdown files in <code>content/</code>. After editing, run
        <code>python build_handbook.py build</code> and refresh.</p>
      <div class="search-wrap">
        <label class="sr-only" for="search">Search handbook</label>
        <input type="search" id="search" placeholder="Search…" autocomplete="off" />
        <span class="search-meta" id="search-meta" aria-live="polite"></span>
      </div>
    </div>
  </header>
  <div class="layout">
    <nav class="toc" aria-label="Sections">
      <p class="toc-title">Sections</p>
      <ul>
{nav_items}      </ul>
    </nav>
    <main id="main">
{articles_html}    </main>
  </div>
  <script src="search.js"></script>
</body>
</html>
"""
    OUT_HTML.write_text(page, encoding="utf-8")
    print(f"Wrote {OUT_HTML} ({len(sections)} sections)")


def main() -> None:
    ap = argparse.ArgumentParser(description="Handbook build (Markdown → HTML)")
    ap.add_argument(
        "command",
        nargs="?",
        default="build",
        choices=("build", "import-pdf", "import-pdf-images"),
        help="build | import-pdf (text→Markdown) | import-pdf-images (figures→images/ + MD)",
    )
    args = ap.parse_args()
    if args.command == "import-pdf":
        cmd_import_pdf()
    elif args.command == "import-pdf-images":
        cmd_import_pdf_images()
    else:
        cmd_build()


if __name__ == "__main__":
    main()
