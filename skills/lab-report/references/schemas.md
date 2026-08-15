# Lab Report Schemas

Shared data contracts for `lab-report`. The orchestrator, scripts, and agents should use
these structures consistently.

## `profile.json`

Stored outside the repository:

```text
~/.auto-college/lab-report/profile.json
```

```json
{
  "student_name": "王小明",
  "student_id": "2024000000",
  "class": "计科 1 班",
  "course": "计算机系统实验",
  "instructor": "李老师",
  "institution": "某某大学"
}
```

Rules:
- Profile fields are reusable defaults, not experiment results.
- Empty strings mean unknown.
- Use cached values silently unless the user asks to update them or current materials
  explicitly conflict with them.

## `report_context.json`

Created in every output directory by `scripts/init_output_dir.py`.

```json
{
  "experiment_name": "cuda-vector-add",
  "report_type": "standard-executable",
  "run_mode": "auto",
  "created_at": "2026-04-30T12:00:00",
  "profile_path": "C:/Users/name/.auto-college/lab-report/profile.json",
  "profile_complete": true,
  "source_files": [
    "C:/path/to/manual.pdf"
  ],
  "source_manifest_path": "C:/path/to/source_manifest.json",
  "language": "zh",
  "screenshot_preference": "key",
  "delivery_formats": ["md", "docx", "pdf"],
  "course_template_id": "computer-network",
  "failure_policy": "auto-skip",
  "notes": ""
}
```

Allowed values:
- `report_type`: `standard-executable`, `data-provided`, `paper-only`
- `run_mode`: `manual`, `auto`
- `language`: `zh`, `en`, or empty when not inferred yet
- `screenshot_preference`: `key`, `all`, `none`
- `delivery_formats`: any of `md`, `docx`, `pdf`
- `failure_policy`: `auto-skip`, `manual-pause`

Rules:
- `report_context.json` records the current run's control decisions.
- Do not put personal profile fields here except profile status/path.
- Agents should read this file when they need run mode, report type, source files, or
  screenshot preference.
- In auto mode, `failure_policy` defaults to `auto-skip`; in manual mode it defaults to
  `manual-pause`.

## `source_manifest.json`

Produced by `scripts/index_source_files.py` when the user provides files or a material
directory.

```json
{
  "created_at": "2026-04-30T12:00:00",
  "input_paths": ["C:/course/lab3"],
  "files": [
    {
      "path": "C:/course/lab3/manual.pdf",
      "name": "manual.pdf",
      "extension": ".pdf",
      "category": "manual",
      "size_bytes": 123456
    }
  ],
  "counts": {
    "manual": 1,
    "slides": 0,
    "data": 1,
    "image": 2,
    "log": 0,
    "code": 3,
    "other": 0
  }
}
```

Categories:
- `manual`: lab instructions or prose source material
- `slides`: presentation decks
- `data`: result tables, measurements, structured data, JSON exports
- `image`: screenshots, photos, scanned pages
- `log`: terminal or program logs
- `code`: experiment source code or scripts
- `other`: files that should be reviewed only if needed

Rules:
- The manifest is an index, not extracted content.
- `experiment-summarizer` decides which files are evidence-bearing after reading them.
- Missing paths are warnings during indexing; unreadable required files become blocking
  material issues during summarization.

## `experiment_info.json`

Created during initialization and updated by `experiment-summarizer`.

```json
{
  "experiment_name": "cuda-vector-add",
  "title": "CUDA Vector Addition",
  "course": "并行计算实验",
  "student_name": "王小明",
  "student_id": "2024000000",
  "class": "计科 1 班",
  "date": "2026-04-30",
  "instructor": "李老师",
  "institution": "某某大学"
}
```

Rules:
- This file contains report-facing metadata only.
- Do not store `run_mode` or `report_type` here; those belong in `report_context.json`.
- `date` defaults to today's date and may be overridden if the source materials specify an
  experiment date.

## `procedure_summary.md`

Markdown structure produced by `experiment-summarizer`.

```markdown
# <Experiment Title>

## Report Type
standard-executable

## Objective
...

## Equipment / Environment
| Equipment/Software | Model/Version | Notes |
|--------------------|---------------|-------|

## Theory
...

## Procedure
### Step 1: <Step Name>
**Type:** executable
**Description:** ...
**Command:** `...`
**Expected outcome:** ...
**Data to collect:** ...

## Provided Data
| Source | Description | How to use |
|--------|-------------|------------|

## Writing Outline
1. ...

## Safety Notes
- ...
```

Path-specific expectations:
- `standard-executable`: include concrete executable steps with commands whenever possible.
- `data-provided`: include `Provided Data`; procedure may describe how the data was obtained
  rather than commands to run.
- `paper-only`: include `Writing Outline`; do not invent executable steps.

## `run_log.md`

Produced only for `standard-executable` when commands are run.

```markdown
# Run Log — <Experiment Title>

**Date:** <YYYY-MM-DD HH:MM>
**Environment:** <OS, shell, key tools>
**Run mode:** auto

---

### Step 1: <Step Name>
- **Command:** `<command>`
- **Status:** success | failed | skipped
- **Failure class:** none | blocking | non-blocking
- **Key output:** ...
- **Screenshot:** `screenshots/step1.png` | none | unavailable (no tool)
- **Raw output:** `raw_outputs/step1.txt`
- **Notes:** ...
```

Rules:
- Record exactly what happened.
- Do not rewrite command output to make it look successful.
- If a failure is `blocking` and `failure_policy` is `manual-pause`, stop and ask the user how
  to proceed.
- If a failure is `blocking` and `failure_policy` is `auto-skip`, record failed/skipped status,
  continue independent later steps, and surface the issue in `delivery_manifest.json`.

## `evidence_map.md`

Produced incrementally by `experiment-summarizer`, `experiment-runner`, and `report-writer`.

```markdown
# Evidence Map — <Experiment Title>

| Report section | Claim or content | Evidence source | Confidence | Notes |
|----------------|------------------|-----------------|------------|-------|
| Objective | ... | manual.pdf page 1 | high | extracted from lab manual |
| Results | ... | raw_outputs/step2.txt | medium | command succeeded |
| Analysis | ... | data.csv + run_log.md | high | calculated from provided data |
```

Rules:
- Every important result, conclusion, table, and screenshot should have a source.
- Use `low` confidence for partial, inferred, or failed-step evidence.
- Do not cite nonexistent files or unsupported claims.

## `report_draft.md`

Produced by `report-writer` template mode.

Rules:
- May contain `[TO BE FILLED]` placeholders for unknown result data.
- Should not contain fabricated results.
- For `paper-only`, avoid execution/screenshot placeholders unless the user provided
  supporting images.

## `final_report.md`

Produced by `report-writer` fill-in mode.

Rules:
- Must not contain unresolved `[TO BE FILLED]` or `[SCREENSHOT: ...]` markers.
- Must only use evidence from source materials, provided data, run logs, raw outputs, or user
  corrections.
- If key evidence is missing, stop and ask instead of inventing it.

## `course_templates.json`

Stored outside the repository:

```text
~/.auto-college/lab-report/course_templates.json
```

```json
{
  "templates": [
    {
      "id": "computer-network",
      "course": "计算机网络",
      "aliases": ["计网"],
      "template_path": "C:/templates/network-lab.md",
      "updated_at": "2026-04-30T12:00:00"
    }
  ]
}
```

Rules:
- `course_templates.json` stores reusable report-structure preferences only.
- Course templates must not store experiment results.
- `report-writer` should prefer the matched course template, then a user-provided one-time
  template, then the built-in default template.

## `delivery_manifest.json`

Produced at final delivery.

```json
{
  "created_at": "2026-04-30T12:00:00",
  "requested_formats": ["md", "docx", "pdf"],
  "delivered_files": [
    "final_report.md",
    "final_report.docx",
    "final_report.pdf"
  ],
  "warnings": [
    "Step 3 failed and was skipped in auto mode."
  ],
  "unresolved_items": [],
  "evidence_map": "evidence_map.md"
}
```

Rules:
- Include every generated deliverable path.
- Summarize skipped commands, missing optional screenshots, unsupported files, and export
  failures.
- `unresolved_items` must be empty only when the final report has no unresolved required data.
