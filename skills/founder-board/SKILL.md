---
name: founder-board
description: >-
  Your board of directors. Puts a business idea in front of a board of up to five,
  each a sub-agent reading the idea through one published framework. Three seats
  are always filled: the Offers lens (from Alex Hormozi's $100M Offers), the
  Monopoly lens (from Peter Thiel's Zero to One) and the Product lens (from Walter
  Isaacson's biography of Steve Jobs). The chair adds two guest seats that fit the
  business: Lean, Moat, Customer, Operator or Calm, drawn from the pack's framework
  library. Each member scores the idea, names the risks that would kill it and
  votes fund, fund with conditions, or pass. Use when the user says "test my
  business idea", "would this work", "pressure-test this", "what would a board
  say", "is this a good business", or starts the founder pack on a new idea.
argument-hint: "<the business idea, or leave blank to use the conversation> [--core | --seats lean,moat]"
---

# founder-board

The first meeting. Before anyone builds a website or signs a lease, a board of
three to five members tears the idea apart, each from a different angle, and votes.

What the user typed after `/founder-board`: `$ARGUMENTS`. If that is blank, take
the idea from the conversation.

## The rule about the names

The lenses are summaries of **published frameworks**, nothing more. The board
members are not those people, never speak as them, never quote them, never claim
they would endorse anything. Write "the Offers lens", never "Alex Hormozi says".
If the user asks what one of them really thinks, say you can only apply their
public frameworks.

## Step 0: the idea file

Everything in the founder pack reads `founder/idea.md` in the user's project. If
it does not exist, write it now from the conversation:

```markdown
# <business name, or a working name>

- What it is: one sentence.
- Who it is for: the target customer, as specific as the user can make it.
- What it sells, at what price: the core product and its price.
- Where and how: city or online, how customers find it, how it is delivered.
- Budget and constraints: money, time, skills, anything already decided.
```

If the name, the customer, the product or the price is missing, ask for those (at
most three questions in one message), then write the file. Do not invent a
budget, a market size or a competitor.

## Step 1: brief the board

Write `founder/board/brief.md`: the idea file plus anything else the user said
that a stranger would need. **Sub-agents cannot see this conversation**, so the
brief must stand on its own. Do not add your own opinion of the idea to it.

## Step 2: choose the seats, then convene

Three seats are always filled: the Offers, Monopoly and Product lenses. Up to two
guest seats come from the other lenses in `lenses.md` (Lean, Moat, Customer,
Operator, Calm). The chair picks the two that fit this business and says why, one
line each:

| the business looks like | guest seats |
| --- | --- |
| demand is unproven, or the product is new to the world | Lean, Customer |
| a shop, cafe or anything with a lease and staff | Operator, Moat |
| big money up front, or thin margins | Moat, Calm |
| an online product, a subscription or a solo service | Calm, Lean |
| it sells to other businesses | Customer, Lean |

`--core` seats only the three core lenses. `--seats lean,moat` seats those guests
instead of the chair's pick (two at most).

Launch one sub-agent per seat in ONE message (Agent tool, `subagent_type:
general-purpose`), each told: `Read founder/board/brief.md and founder-board's
lenses.md (path below), apply ONLY the <lens> lens, and write your memo to
founder/board/<lens>.md.` A guest seat is also told to read the framework files
named under "Depth" in its lens, in the founder-playbook skill's `frameworks/`
folder (`${CLAUDE_SKILL_DIR}/../founder-playbook/frameworks/<slug>.md`). The lens
file is `lenses.md` in this skill's folder (`${CLAUDE_SKILL_DIR}/lenses.md`; if that
path is not expanded, use the base directory Claude Code printed for this skill).

Each memo, in this shape:

```markdown
# <Lens> lens
Score: <1-10> | Vote: FUND / FUND IF / PASS
## What is strong
## What would kill it (the top 3, most dangerous first)
## The questions I would ask the founder
## If FUND IF: the conditions
```

## Step 3: the chair's summary

Read the memos (they are short) and write `founder/board.md`:

1. The vote, e.g. "3 fund if, 1 pass, 1 fund", and the average score. Name the
   seats, so the reader sees which lenses were at the table.
2. The risks more than one member raised: these go first.
3. Every condition, merged, as a checklist the rest of the pack can tick off
   (the CFO, the consumer panel and pricing will test most of them).
4. One paragraph: the strongest version of this business the board can see.
   It may differ from what the user pitched; say so plainly.

Keep the members' disagreements. A board that agrees on everything was not doing
its job.

## Rules

- Score the business, not the founder.
- No made-up facts. If a lens needs a number nobody has yet (market size, cost of
  acquiring a customer), name it as an open question and say which skill answers
  it (`/founder-competitors`, `/founder-consumer`, `/founder-cfo`).
- A PASS is a result, not a failure. Say it plainly.

## Market and language

If `founder/market.json` exists and says country `VN`, or the user is clearly in Vietnam or writes
Vietnamese, also read `${CLAUDE_SKILL_DIR}/locale-vn.md`. Write every file in the user's language
(Vietnamese when they write Vietnamese) and use the currency from `founder/market.json`
(VND is shown like `45,000₫`). Treat the Vietnam notes as prompts to check, not as sourced rules.

## Frameworks that apply

The guest lenses are built on these library files (their "Depth" in `lenses.md`).
A guest member reads the ones named in its lens before writing its memo. Read any
of them with `python3 "${CLAUDE_SKILL_DIR}/../founder-playbook/playbook.py" show <slug>`.

- `lean-startup`: Lean Startup
- `customer-development`: Customer Development
- `graham-do-things-that-dont-scale`: Do Things that Don't Scale
- `moat-circle-of-competence`: Circle of Competence, Moat and Margin of Safety
- `five-forces`: Five Forces
- `inversion`: Inversion and the Pre-Mortem
- `bezos-working-backwards`: Working Backwards
- `jobs-to-be-done`: Jobs to Be Done
- `e-myth`: The E-Myth
- `high-output-okrs`: High Output Management and OKRs
- `walton-ten-rules`: Walton's Ten Rules for Building a Business
- `graham-default-alive`: Default Alive or Default Dead, and Ramen Profitable
- `calm-company`: The Calm Company
- `profit-first`: Profit First

## Output

`founder/idea.md`, `founder/board/` (brief and the memos), `founder/board.md`.
Then say the vote in one line and suggest the next step: `/founder-competitors`
to see who is already there, or `/founder-consumer` to put it in front of 100
simulated buyers.

## Where the pack goes next

```
board -> competitors -> consumer -> pricing -> offer -> cfo -> marketing -> brand -> ops -> launch -> plan
```

Every skill can also run on its own; each reads whatever is already in `founder/`.
