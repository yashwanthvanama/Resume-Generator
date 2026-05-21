---
name: tailor-resume
description: Tailor templates/yashwanth_vanama_resume_software_engineer.tex to a given job description by rewriting the Professional Summary, Work Experience bullets, and Skills sections while preserving the file's LaTeX structure and formatting. Trigger when the user asks to tailor/customize/update the software engineer resume for a job (posting, JD, role).
---

# Tailor Software Engineer Resume

Rewrite three sections of `templates/yashwanth_vanama_resume_software_engineer.tex` so the resume aligns with a specific job description, without touching any other part of the file.

**Never edit `templates/yashwanth_resume_software_engineer.tex`** — that is the untouched base resume. All tailoring edits go into `yashwanth_vanama_resume_software_engineer.tex`. If that file is missing or has drifted from the base, recreate it by copying the base: `cp templates/yashwanth_resume_software_engineer.tex templates/yashwanth_vanama_resume_software_engineer.tex`. If the user wants to start a fresh tailoring on top of the base, confirm, then recopy before editing.

## Input

The job description may arrive as:
- Pasted text in the user's message
- A path to a file (e.g. under `job_postings/`)
- A URL — if so, fetch it first with `uv run python -m src.scrape_job_posting "<url>"` and use the stdout markdown as the JD

If no JD is provided, ask the user for one before editing.

## Target file and allowed scope

**File:** `templates/yashwanth_vanama_resume_software_engineer.tex` (the tailored copy — never the base `yashwanth_resume_software_engineer.tex`)

**Edit ONLY these three sections:**
1. `\section*{Professional Summary}` — the paragraph immediately after
2. `\section*{Work Experience}` — only the `\item` lines inside each `\begin{itemize} … \end{itemize}` block. Do **not** change the `\subsection{…}` headings (job title / company / dates) or the number of roles.
3. `\section*{Skills}` — the four `\textbf{…:}` lines

**Do not modify:** preamble, packages, `\titleformat`/`\titlespacing` directives, header (name/contact line), Projects section, Education section, or the `\subsection` role headings in Work Experience. Do not add or remove sections.

## Editing rules

- Use the `Edit` tool with precise `old_string`/`new_string` replacements, one section at a time. Do not rewrite the whole file with `Write`.
- Preserve the LaTeX idioms already in the file:
  - `\section*{…}`, `\subsection{…}`, `\begin{itemize} … \end{itemize}`, `\item`
  - `\textbf{…}`, `\href{…}{…}`
  - Escape `%`, `&`, `$`, `#`, `_` as `\%`, `\&`, `\$`, `\#`, `\_` (e.g. `$2.4M` stays `\$2.4M`; `60%` stays `60\%`).
  - Use straight ASCII quotes and hyphens; keep en-dash `–` only where it already appears (role date ranges).
  - No trailing whitespace, no blank line inside an `itemize`.
- Keep the current **bullet count per role** (currently 4 bullets for each of the three roles). Keep the Skills section at exactly 4 lines with the existing category labels (`Languages \& Scripting`, `Frameworks \& Libraries`, `Tools \& Platforms`, `Methodologies \& Concepts`).
- Keep each bullet a single sentence on one line, similar length to the originals (roughly 25–40 words), and keep a concrete metric/impact where the original had one — carry the spirit forward rather than fabricating new numbers. If a metric no longer fits the reworded bullet, reuse the original metric or drop it; do not invent new figures.
- **Adding JD technologies to the resume:** When the JD lists technologies, languages, tools, or methodologies that are not currently in the resume, add them to the most appropriate Skills line and, where it fits naturally, weave them into a relevant bullet. Do not fabricate entire new projects or outcomes — but adding a tool to a bullet where it plausibly co-existed with the work described (e.g. adding "bash scripting" to a Jenkins CI/CD bullet, or adding a standard/methodology to Methodologies) is expected and encouraged. The goal is the strongest honest match, not strict conservatism.
- **Professional Summary:** 1–2 sentences, echo the job's title and top 2–3 required skills, keep the "3+ years" framing unless the JD clearly calls for a different seniority level (then adjust only within what the work history supports).
- **Skills:** reorder and swap items within each category so the JD's must-haves appear first. Add JD-required technologies that are missing from the current Skills lines — place them near the front of the relevant category. You may also replace less-relevant items to keep lines from becoming too long. Keep `\\` line endings between the four lines, matching the existing pattern.
- **Truthfulness boundary:** Add technologies/tools/standards the candidate plausibly knows or used (commonly co-occurring with their stack, or listed by the JD as requirements). Do not claim specific project outcomes, companies, or domain expertise that have no basis in the work history.

## Workflow

1. Confirm `templates/yashwanth_vanama_resume_software_engineer.tex` exists; if not, copy it from `templates/yashwanth_resume_software_engineer.tex`.
2. Read the current `templates/yashwanth_vanama_resume_software_engineer.tex` to anchor exact strings for `Edit`.
3. Extract from the JD: target title, must-have technologies, domain keywords, seniority cues.
4. Identify JD technologies/tools/standards missing from the current resume and plan where to add them: Skills lines (always) and relevant bullets (where plausible).
5. Draft the three rewritten sections in your head (or in a short plan message to the user if ambiguous), then apply them with `Edit` calls on the tailored file only.
6. After editing, verify by compiling: `uv run python src/compile_resume.py yashwanth_vanama_resume_software_engineer`. If `xelatex` isn't available locally, note that to the user instead of failing the task.
7. Report what changed at a high level (summary tone, top keywords added, new technologies inserted, skills reordered) — do not dump the full new file.

## Example invocation

> "Tailor my SWE resume for this JD: <pasted text>"
> → Read tex file → Edit Professional Summary → Edit each Work Experience itemize block → Edit Skills → run compile-resume → report.
