# BOM Guardian

**Live, citation-backed risk radar for your bill of materials.**

🌐 **[Live app](https://bom-guardian.onrender.com)** (Render) ·
[![Run on Replit](https://replit.com/badge/github/jules-jo/bom-guardian)](https://replit.com/new/github/jules-jo/bom-guardian)

Component obsolescence tracking is still a manual, error-prone chore: EOL notices
hide in PCN PDFs, errata sheets get published quietly, and supply shocks show up
in trade news before they show up in your distributor portal. BOM Guardian points
a team of AI agents at the live web and turns a raw BOM CSV into a ranked,
cited risk report in minutes.

Built at the You.com Agentic Hackathon (SF, July 2026).

## How it works

For every component, three agents fan out in parallel:

| Agent | You.com API | What it finds |
|-------|-------------|---------------|
| Lifecycle | Research | ACTIVE / NRND / EOL verdict, PCN & EOL notices, drop-in alternates — with citations |
| Errata | Search | Published errata sheets, device limitations, advisories |
| Availability | Search (freshness-filtered) | Recent shortage / allocation / lead-time signals |

Search hits only count if they actually mention the part (normalized
part-number prefix match, so packaging suffixes don't break it) — otherwise a
random STM32 errata PDF would flag your Altera FPGA. Findings are scored
(EOL → HIGH; NRND or multiple independent signals escalate) and rendered as a
report with every claim linked to its source, downloadable as Markdown.

```
BOM CSV -> parser -> [lifecycle | errata | availability] x N components -> risk score -> report
                          (async fan-out, bounded concurrency)
```

## Quickstart

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
cp .env.example .env   # paste your key from https://you.com/platform
.venv/bin/streamlit run app.py
```

CLI (no UI):

```bash
.venv/bin/python -m bom_guardian.cli --mpn STM32H743ZIT6
.venv/bin/python -m bom_guardian.cli --bom data/demo_bom.csv
```

Tests:

```bash
.venv/bin/pytest
```

## Tech

Python 3.13, httpx (async), Streamlit. You.com Search, Contents, and Research
APIs. No component database — everything is discovered live from the web at
query time, which is exactly the point.
