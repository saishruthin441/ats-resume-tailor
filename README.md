# ATS Resume Tailor

> Python CLI that scores your resume against any job description, identifies keyword gaps, and suggests rewrites — zero external AI API required.

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://python.org)
[![CLI](https://img.shields.io/badge/CLI-Typer-009688)](https://typer.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## How It Works

```
Your Resume (PDF/DOCX)          Job Description (txt)
         │                               │
         ▼                               ▼
    extract_text()              extract_text()
         │                               │
         └──────────┬────────────────────┘
                    ▼
           TF-IDF Keyword Extraction
                    │
                    ▼
          Cosine Coverage Score (0-100)
                    │
           ┌────────┴────────┐
           ▼                 ▼
      Gap Report       Recommendations
   (Missing Skills)   (Bullet Rewrites)
```

## Installation

```bash
git clone https://github.com/saishruthin441/ats-resume-tailor.git
cd ats-resume-tailor
pip install -r requirements.txt
```

## Usage

```bash
# Quick ATS score
python -m ats_tailor.cli score --resume resume.pdf --job job.txt

# Full analysis with keyword gaps and recommendations
python -m ats_tailor.cli analyze-cmd --resume resume.pdf --job job.txt
```

### Example Output

```
╭──────────────────╮
│    ATS Score     │
│   82.5 / 100     │
╰──────────────────╯

Keyword Analysis
┌──────────┬──────────────┐
│ Status   │ Keyword      │
├──────────┼──────────────┤
│ ✅ Present │ python      │
│ ✅ Present │ fastapi     │
│ ❌ Missing │ kubernetes  │
│ ❌ Missing │ docker      │
└──────────┴──────────────┘

💡 Recommendations:
  • Add 'kubernetes' — appears 4 time(s) in the job description
  • Add 'docker' — appears 3 time(s) in the job description
```

## Running Tests

```bash
pytest tests/ -v
```

## License

MIT © 2026 saishruthin441
