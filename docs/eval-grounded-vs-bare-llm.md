# Eval: BOM Guardian (You.com-grounded) vs. Bare Frontier LLM

**Method (2026-07-24):** A fresh Claude agent with no tools and no conversation
context answered lifecycle questions from training knowledge only (cutoff:
January 2026), committing to a verdict + confidence per part. BOM Guardian
answered the same questions through its live You.com pipeline. Ground truth
from manufacturer documents.

## Head-to-head results

| Case | Ground truth | Bare LLM (no web) | BOM Guardian (You.com) | Winner |
|------|-------------|-------------------|------------------------|--------|
| **Vishay SiP32508** — EOL announced **2026-03-24**, after training cutoff | EOL (PTN-SIL-000401-2026) | **ACTIVE** (low conf, "no EOL date known"); suggested SiP32509 as fallback — **which is on the same EOL notice** | **EOL**, cites the exact PTN PDF + date; flags that a distributor still shows "Active" and explains why the PDN wins | **BOM Guardian — decisive** |
| H1-2026 PDN landscape | Multiple (MCC 2026-01-27, Vishay 2026-03-24, ...) | "UNKNOWN — cannot name specific PDNs without fabricating" (self-admitted) | Surfaces dated PDN documents with links | **BOM Guardian — structural** |
| Current STM32H7 lead times (July 2026) | live market data | "Extrapolation, low confidence" (self-admitted) | Freshness-filtered live signals | **BOM Guardian — structural** |
| MPU-6050 (famous EOL) | EOL | EOL ✓ (high conf, no sources) | EOL ✓ + distributor/TDK citations + TDK's recommended successor | Tie on verdict; **BOM Guardian on evidence** |
| Raspberry Pi 4 guarantee | ≥ Jan 2034 | 2034 ✓ ("risk I'm conflating with another Pi model") | 2034 ✓, cites current commitment, notes it superseded the old Jan 2026 date | Tie on verdict; **BOM Guardian on evidence** |
| Cyclone II EP2C5T144C8N | contested | **EOL**, "LTB circa 2017, last ship ~2018" — specific dates, zero sources, self-flagged fuzzy | **NRND**: found no formal PDN, current distributor listings, Intel statement extending Cyclone supply to 2040 — all cited | **Auditability**: one asserts from memory, one shows receipts |
| STM32H743 / NE555 / DS3231 (stable actives) | ACTIVE | ACTIVE ✓ | ACTIVE/LOW ✓ | Tie |

## Honest conclusions (use these on stage)

1. **On famous, pre-cutoff history, a frontier LLM is decent.** We do not claim
   otherwise — the baseline knew the MPU-6050 EOL and the Pi's 2034 date.
2. **On anything after its cutoff, it is structurally blind — and dangerously
   polite about it.** For SiP32508 it committed to ACTIVE and offered a
   replacement that is dying on the same document. In a real BOM review, that
   error ships a product on two discontinued parts.
3. **On current market state (lead times, allocation), it can only extrapolate.**
   It said so itself.
4. **Citations are the difference between an answer and a decision.** Both
   systems can say "EOL"; only the grounded one hands the engineer the PDN PDF
   to forward to procurement.

One-liner: *"The model knows how the world was. You.com tells our agents how it
is — and hands you the document to prove it."*

Cost of the grounded run: ~$0.02/part.
