# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Dependencies are managed with `uv` (see `uv.lock`, `pyproject.toml`). Python >= 3.11.

```bash
# Install / sync dependencies
uv sync

# Compile a resume (interactive picker if no arg)
uv run compile-resume                       # or: uv run python src/compile_resume.py
uv run compile-resume yashwanth_resume_software_engineer

# Auto-recompile on .tex save (watches templates/)
uv run python watch_templates.py

# Scrape a job posting via Firecrawl (prints markdown to stdout)
uv run python -m src.scrape_job_posting "https://example.com/jobs/123"
uv run scrape-job "https://example.com/jobs/123" --only-main-content
```

`FIRECRAWL_API_KEY` must be set (via `.env` at project root or exported) for the scraper.

LaTeX compilation requires `xelatex` on PATH. On macOS: `brew install --cask basictex` (then `sudo tlmgr install enumitem titlesec hyperref xcolor fontspec`) or `mactex`.

## Architecture

Three independent entry points, loosely coupled:

1. **`src/compile_resume.py`** — LaTeX → PDF pipeline. Runs `xelatex` twice (for references/formatting) from the template's directory, moves the PDF to `output/`, and cleans aux files (`.aux .log .out .toc .fls .fdb_latexmk`). Templates are discovered by globbing `templates/*.tex`; the CLI arg is the template stem (`.tex` auto-appended).

2. **`watch_templates.py`** — `watchdog` observer on `templates/`. On `.tex` modify events it shells out to `compile_resume.py` as a subprocess (not an import). Has a 1s per-file debounce plus a 0.1s post-save delay to let editors finish writing.

3. **`src/scrape_job_posting.py` + `src/firecrawl_client.py`** — CLI wrapper around a minimal Firecrawl REST client (`POST /v1/scrape`). `FirecrawlClient` handles auth, retries 429/5xx with exponential backoff, and `extract_content_fields` normalizes response shapes (`data.markdown|html` vs top-level vs `content`/`text` fallback). Note: `scrape_job_posting.py` imports `firecrawl_client` as a top-level module, so it must be run as `python -m src.scrape_job_posting` (or via the `scrape-job` script entry) with `src/` resolvable on `sys.path`.

Path convention: both scripts resolve `project_root = Path(__file__).parent.parent`, so `src/` can be moved but the `templates/` and `output/` siblings must stay put.

## Directory layout notes

- `templates/` — source `.tex` files (tracked dir, individual `.tex` files are gitignored except `.gitkeep`).
- `output/` — generated PDFs (gitignored).
- `original_resume/` — reference PDFs (not consumed by code).
- `job_postings/` — scratch dir for scraped content (not auto-written by scraper; scraper prints to stdout).
- `venv/` and `.venv/` both exist; `.venv/` is the uv-managed one. `activate_env.sh` predates the uv migration.
