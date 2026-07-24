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

## Cost: You.com API vs. LLM + vendor web-search tool

Could this pipeline be rebuilt on a frontier LLM's built-in web-search tool
(Anthropic/OpenAI/Gemini)? Yes — nothing here is categorically impossible
elsewhere. The differences are cost shape and architecture.

**BOM Guardian per-part cost (measured):**

| Agent | Call | Cost | LLM tokens |
|-------|------|------|-----------|
| Lifecycle | 1 Research call | $0.012 | none billed to us (bundled) |
| Errata | 1 Search | $0.005 | zero — deterministic Python filter |
| Availability | 1 Search | $0.005 | zero — deterministic Python filter |
| **Total** | | **~$0.022** | |

**Same pipeline on a frontier LLM + its web-search tool (estimated):**
the lifecycle agent becomes an agentic loop — 3–6 searches at ~$10/1k
(~$0.03–0.06) plus 20–50k tokens of read-and-reconcile on a Sonnet-class
model (~$0.10–0.20). The errata/availability agents can no longer be LLM-free
(the search tool only exists inside an LLM call): ~$0.03–0.06 each.
**Realistic total: $0.15–0.30/part — roughly 5–10x more.**

At demo scale the difference is irrelevant (cents either way). At product
scale it decides viability: a 1,000-part BOM re-checked monthly is ~$22/mo
on this pipeline vs. ~$150–300/mo rebuilt on vendor search tools; across the
~50 BOMs a mid-size hardware company manages, ~$1.1k/mo vs. ~$10k/mo.

Honest caveats:
1. The gap is mostly Research-API-vs-hand-rolled-loop. A cheap search API
   (e.g. Tavily) + small model could narrow it to 2–3x.
2. Assumes quality parity, verified here only by spot checks (which included
   the hard cases above).
3. Ignores engineering cost of building/maintaining the agentic loop — which
   favors the managed API further.

Architectural corollary: because retrieval is a standalone API rather than a
tool inside one vendor's chat loop, two of the three agents run with **no LLM
at all** (deterministic, unit-tested, token-free), freshness windows are API
parameters rather than prompt suggestions, and the data layer is
model-vendor-independent.
