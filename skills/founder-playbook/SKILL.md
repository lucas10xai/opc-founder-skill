---
name: founder-playbook
description: >-
  Your mentor. A library of business and startup frameworks from well-known
  founders, investors and thinkers (Paul Graham, Eric Ries, Steve Blank, Clayton
  Christensen, Michael Porter, Jeff Bezos, Warren Buffett and Charlie Munger,
  Andy Grove, Jason Fried and others), each summarised in our own words. Picks the
  two or three that fit the user's stage and kind of business, applies them to the
  facts in founder/ (never to invented ones), and says what each one shows, what
  it misses and which pack skill acts on it. Use when the user says "what would a
  good founder do", "give me a framework", "how do I think about this", "mentor
  me", "I am stuck", "should I grow fast", "is this a good market", or asks about
  lean startup, jobs to be done, moats, pivots or product-market fit.
argument-hint: "[a question, or the situation you are stuck on]"
---

# founder-playbook

The rest of the pack runs a method. This skill is the reading list behind it: what
experienced founders and investors have published about the exact decision in front
of the user, applied to the user's own numbers instead of quoted at them.

Tool in this folder:

```bash
python3 "${CLAUDE_SKILL_DIR}/playbook.py" suggest --stage validate --fits consumer
```

The library is `${CLAUDE_SKILL_DIR}/frameworks/`, one markdown file per framework.
What the user typed after `/founder-playbook`: `$ARGUMENTS`

## The rule about the names

Every framework is a **published idea**, summarised in our words. The people named
in it are the source of the idea, not members of the conversation. Never write "X
would say", never put words in their mouth, never imply that anyone endorses the
user's business or this project. Write "the Lean Startup framework asks...", and
cite the book or essay from the file's `source` line. If the user asks what a
person really thinks, say you can only apply what they have published.

## Step 1: find the stage and the kind of business

Read what exists in `founder/`: `idea.md`, `market.json`, `board.md`, the panel and
interview results, `numbers.json`, `launch.md`, `metrics.md`. From them, set:

| stage | when |
| --- | --- |
| `idea` | nothing tested yet |
| `validate` | testing demand: panel, interviews, competitors |
| `price` | deciding price, offer and the numbers |
| `launch` | preparing to open, or running the first test |
| `operate` | open, with real sales and routines |
| `grow` | working, and deciding how much to scale and how fast |

and the kind of business, one of `consumer`, `business`, `online`, `service`,
`physical`. If you cannot tell the stage or the kind, ask one short question. Do
not guess a stage to make a framework fit.

If the user asked about one pack skill's job (pricing, launch, operations), add
`--skill founder-pricing` and so on to narrow the list.

## Step 2: pick two or three

```bash
python3 "${CLAUDE_SKILL_DIR}/playbook.py" suggest --stage launch --fits physical --skill founder-launch
python3 "${CLAUDE_SKILL_DIR}/playbook.py" list              # the whole library
python3 "${CLAUDE_SKILL_DIR}/playbook.py" show lean-startup # read one in full
```

Choose at most three, and prefer ones that disagree with each other where the
decision is genuinely open (see "When frameworks disagree"). Never apply every
framework that matches; a long list is the same as no advice. Read each chosen file
completely with `show` before you use it.

## Step 3: apply it to this business

Each file's "How the pack uses it" section is the procedure for applying it at a
named pack step. When the user's question is about that step's job, follow it, and
write the result where the section says.

For each chosen framework, in this order:

1. **What it says**, three sentences in plain words, from the file, not from memory.
2. **The questions** from the file's "Questions to put to the founder", answered
   from the user's own files. Name the file for each answer ("from
   `founder/panel/results.md`"). Where the answer is not in the files, say it is
   unknown and ask the user or name the pack skill that finds out.
3. **The red flags** from the file that this business shows, with the evidence.
4. **What to do next**: one specific action and the pack skill that does it.
5. **What it misses**, from the file's "Limits", so the user knows where the
   framework could mislead here.

## When frameworks disagree

They will, and that is useful. Show both sides and pick one for this user's
situation with a reason:

- **Speed against profit.** A growth-first framework (blitzscaling) against a
  profit-first one (default alive, the calm company, profit first). For almost any
  business funded by its founder, profit and cash come first; growth-first only fits
  a winner-take-most market with outside money.
- **Test first against plan first.** The lean approach (cheapest test, learn) against
  working backwards (write the finished product description first). They combine:
  write the one-page description, then test the riskiest sentence in it.
- **Focus against exploring.** A narrow position against looking for a new market.
  Early on, narrow wins; once the position is secure, explore.

Do not average them into mush. Say which fits and why, and what evidence would change
the choice.

## Step 4: write it down

Write `founder/playbook.md`:

```markdown
# Playbook: <the question or situation>
Stage: <stage> | Kind: <kind>

## <Framework name> (<source>)
What it says: ...
What it shows about this business: ... (with the files it is from)
Red flags present: ...
Next action: ... (/founder-xxx)
Where it could mislead here: ...
```

End with one decision: what to do this week, and which one thing is still unknown.
Append to the file if it exists; one section per framework applied, dated by
session if there are several.

## Rules

- Facts come from `founder/` or from the user. No invented market sizes, customers,
  competitors or results; no "studies show".
- Never quote the source. Short framework names are fine. Everything else is in
  your words, or the library's.
- Frameworks are lenses, not laws. Most were written from a few famous cases; say
  so when the user treats one as a guarantee.
- A framework never overrides the numbers. If the CFO says each unit loses money,
  no framework makes that acceptable.
- Not financial, legal or tax advice.

## Adding to the library

A new framework is one file in `${CLAUDE_SKILL_DIR}/frameworks/` with the header and
sections of the others: `slug`, `name`, `source`, `people`, `stage`, `fits`, `feeds`,
then the sections The idea, When to use it, Questions to put to the founder, Red
flags, How the pack uses it, Limits, Sources. Own words, verified against the
source, no quotations. Then:

```bash
python3 "${CLAUDE_SKILL_DIR}/playbook.py" check
```

It reports every malformed file and exits 1 if there is one.

## Market and language

If `founder/market.json` exists and says country `VN`, or the user writes
Vietnamese, write `founder/playbook.md` in their language, keep framework names in
their original form with a short gloss, and cite sources by author, title and year.
Examples should use the user's market and currency (VND like `45,000₫`).

## Output

`founder/playbook.md`. Next: the pack skill each framework pointed to, then
`/founder-plan` once the numbers are in.
