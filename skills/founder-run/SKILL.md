---
name: founder-run
description: >-
  Your chief of staff for the whole founder pack. Sets the market once (country,
  currency, language), checks what is already in the founder/ folder, and runs the
  next skill in the right order: board, competitors, consumer panel, pricing, offer,
  CFO, compliance, marketing, brand, operations, launch, then the business plan.
  Picks up where the founder left off if the session was interrupted, and says which
  steps are optional (real interviews, sales for businesses, metrics after launch,
  a pitch). Use when the user says "run the whole pack", "start from the beginning",
  "what's next", "where am I", "continue", "do everything", or "test my business
  idea end to end".
argument-hint: "[the idea in one or two sentences]"
---

# founder-run

The pack has eighteen skills and an order. This one keeps track of both, so the
founder does not have to remember which skill comes next.

Tool in this folder:

```bash
python3 "${CLAUDE_SKILL_DIR}/status.py"
```

What the user typed after `/founder-run`: `$ARGUMENTS`

## Step 1: see where things stand

```bash
python3 "${CLAUDE_SKILL_DIR}/status.py" --dir founder
```

It lists every skill, marks the ones whose file already exists in `founder/`, and
names the next one. It only reads. If the folder is empty, this is a fresh start.
If some steps are done, tell the user which, and continue from the next one rather
than redoing them. Offer to redo a step only if the user asks, or if something
earlier changed (a new price means `/founder-cfo` and `/founder-plan` must run
again).

## Step 2: set the market, once

If `founder/market.json` does not exist, ask three short questions together: which
country the business will sell in, which currency to count in, and which language
the user wants the files written in. Then write it:

```bash
python3 "${CLAUDE_SKILL_DIR}/status.py" market --country VN
python3 "${CLAUDE_SKILL_DIR}/status.py" market --country CA --currency CAD --language English
```

Vietnam fills in VND and Vietnamese by default. Every other skill reads this file:
it decides the currency in `numbers.json` and `customer.json`, whether the Vietnam
notes in each skill are read, and the language of everything written. If the user
is writing to you in Vietnamese, ask in Vietnamese and default to Vietnamese.

## Step 3: the idea

If `founder/idea.md` does not exist, `/founder-board` writes it from what the user
says. If the user gave an idea in `$ARGUMENTS`, hand it over as is. Do not improve
it and do not fill gaps; the board asks for what is missing.

## Step 4: run the next skill

Run the skills in this order, one at a time, by reading each `SKILL.md` and
following it as if the user had typed its command:

```
board -> competitors -> consumer -> pricing -> offer -> cfo -> compliance
      -> marketing -> brand -> ops -> launch -> plan
```

After each one, say in two lines what it found and what it changes for the rest,
then run `status.py` again to confirm the file landed and to see what is next. Ask
before continuing only when the next step costs real effort or money: the
100-buyer panel is 100 sub-agent calls, so offer `--quick` first.

Things that change the order:

- **Real people.** `/founder-interview` takes days, because it needs real
  conversations. Run it right after the panel, give the founder the script, and
  carry on with the rest. The plan's verdict will include the real result once
  the interviews are tallied.
- **Selling to businesses.** If the customers are companies, run `/founder-sales`
  after marketing, and set `"kind": "business"` in `founder/customer.json` before
  the panel.
- **A step fails its own check.** If `/founder-cfo` shows each unit losing money
  or the panel buys under the bar, stop. Say which skill fixes it
  (`/founder-pricing`, `/founder-offer`) and rerun from there. Do not carry on to
  marketing a business that loses money on every sale.
- **Raising money.** Only if the user says so, `/founder-pitch` after the plan.
- **Already launched.** Go straight to `/founder-metrics` with real numbers.
- **Stuck on a decision.** At any point, `/founder-playbook` picks the two or three
  published frameworks that fit the stage and applies them to the files in
  `founder/`. Use it when the user asks how to think about something, not to skip a
  step.

## Step 5: the end

When `/founder-plan` has run, read the verdict to the user in one line, the one
thing to do this week, and what is still open (interviews not done, licences to
confirm). Offer the exports: `compile.py --html` for a printable copy, and
`compile.py --vault <folder>` for an Obsidian vault or a Notion markdown import.

## Rules

- One skill at a time, in order, with the evidence the earlier ones wrote. Never
  skip ahead and never invent a file a skill should have written.
- Never overwrite a finished step without asking.
- Say plainly what is simulated (the panel), what is projected (the numbers) and
  what is real (interviews, a pre-sale, actuals). Not financial, legal or tax advice.

## Output

`founder/market.json` when it was missing, and every file the skills write along
the way. Next: the skill `status.py` names, or `/founder-metrics` after launch.
