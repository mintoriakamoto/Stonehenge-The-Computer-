# TEAM_MEMORY.md

Shared team memory for the Verdict quality gate workflow.
Each Quality Gate entry is a dated, structured block appended under `## Quality Gate`.
The format is designed for both human readability and machine parsing (pattern extraction).

---

## Brand

**Voice constraints for "voice match" scoring:**

_(Define brand archetype, tone, and register here. Examples: "Professional but approachable. No jargon without explanation. First-person plural preferred. Emoji-free."_

**Key constraints:**
- _(Edit this list to match your brand)_

---

## Quality Gate

### Entry format

Each gate decision appends one entry in this exact structure so it can be parsed
for recurring failure pattern analysis:

```
---
date: YYYY-MM-DD
piece: <brief name or ID>
audience: <target audience / distribution surface>
decision: returned | shipped
average_score: <float, e.g. 6.5>
scores:
  hook_strength: <1-10>
  clarity: <1-10>
  emotional_pull: <1-10>
  differentiation: <1-10>
  value_density: <1-10>
  voice_match: <1-10>
  shareability: <1-10>
  platform_fit: <1-10>
binding_constraints:
  - <lowest-dimension>: <score>  # typically the 2 lowest scores
flags:
  - category: ai-mush | vague-claims | clickbait-without-payoff | drag | missing-or-buried-cta
    issue: <one-line description>
the_one_edit: <the single edit that would lift the piece furthest>
edit_dimension: <which dimension the edit lifts>
rationale: <one-line rationale for the gate decision>
---
```

### Example entry

```
---
date: 2026-10-14
piece: "homepage-hero-v3"
audience: "homepage hero banner, B2B SaaS visitors"
decision: returned
average_score: 5.3
scores:
  hook_strength: 3
  clarity: 6
  emotional_pull: 4
  differentiation: 3
  value_density: 5
  voice_match: 8
  shareability: 4
  platform_fit: 8
binding_constraints:
  - hook_strength: 3
  - differentiation: 3
flags:
  - category: clickbait-without-payoff
    issue: "Claim '10x faster' not substantiated in body"
  - category: vague-claims
    issue: "ROI improvement cited without metric or source"
  - category: drag
    issue: "Paragraph 3 explains generic cloud benefits irrelevant to hero"
the_one_edit: "Replace the unsupported '10x faster' claim with a specific, measurable benefit backed by a customer metric"
edit_dimension: hook_strength
rationale: "Hook makes an unsubstantiated 10x claim that undermines credibility; no evidence in the body to cash it"
---
```

### Entries

_(New entries are appended below this heading in date order.)_

---
