---
name: founder-metrics
description: >-
  Your performance analyst, for after the launch. Takes the CFO's plan and what
  really happened (units sold, money taken, real costs, ad spend, new customers),
  compares them month by month, and says plainly whether the business is on track,
  needs a change or should stop and rethink, with the failing number named. Redraws
  year 1 from the real months (break-even, payback, cash needed) and turns the gap
  into a short list of things to change. Use when the user says "how is it going",
  "weekly review", "are we on plan", "we launched", "here are my sales", "should I
  keep going", "plan vs actual", or pastes real sales numbers.
argument-hint: "[week or month to review]"
---

# founder-metrics

Every other skill in the pack works before the money is spent. This one starts
once there are real numbers, and it is the only one that tells the founder
whether the plan was right.

Tool in this folder:

```bash
python3 "${CLAUDE_SKILL_DIR}/metrics.py" founder/numbers.json founder/actuals.csv --out founder/metrics.md
```

What the user typed after `/founder-metrics`: `$ARGUMENTS`

## Step 1: get the real numbers

Read `founder/numbers.json` (the plan) and `founder/actuals.csv` if it exists. If
it does not, make it from what the user gives you. The header comes from
`python3 "${CLAUDE_SKILL_DIR}/metrics.py" --template`; an example is in
`${CLAUDE_SKILL_DIR}/actuals.example.csv`.

One row per month of year 1:

| column | what it is |
| --- | --- |
| `month` | 1 to 12, the month of year 1 |
| `units` | units sold so far this month (required) |
| `days` | selling days the row covers, for a partial month (a first-week review is month 1, days 7) |
| `revenue` | money taken |
| `variable_cost` | total cost of making and delivering what was sold |
| `fixed_cost` | rent, salaries and the rest, so far this month |
| `ad_spend`, `new_customers` | what you spent to win customers, and how many you won |

Ask only for what the user has. Where a column is empty the tool uses the plan's
figure and says so in the report. Never fill a real number from a guess: if the user
does not know their real costs, say that the answer is weaker for it and ask them to
pull the bank or point-of-sale export.

Replace the row for a month as it fills up. Do not add a second row for it.

Money is plain numbers in the plan's currency (see `currency` in `numbers.json`).
No signs or thousands separators needed.

## Step 2: run it

```bash
python3 "${CLAUDE_SKILL_DIR}/metrics.py" founder/numbers.json founder/actuals.csv --out founder/metrics.md
```

The tool reads the latest row and gives one of three calls:

- **On track.** Sales, profit per unit and customer cost are where the plan put them.
- **Change something.** Sales under 80% of plan, or profit per unit more than 15%
  under plan, or customers costing more than `max_cac` (add `"max_cac"` to
  `numbers.json` from `/founder-marketing` if you want that check).
- **Stop and rethink.** Each unit loses money at the real price and cost, or sales
  were under 60% of plan in each of the last two months.

Change the bars with `--amber` and `--red` only if the user has a reason, and write
the reason in the report.

## Step 3: read it to the user

In this order, in plain words:

1. The call, and the one number behind it ("sales are 64% of plan in month 2").
2. The unit: real price and real cost per unit against the plan. This is usually
   where the answer is. Revenue short means a price or volume problem; cost over
   means a supplier, waste or discount problem.
3. Year 1 now: the reforecast against the plan (profit, break-even, payback, cash).
   It is arithmetic on the real months, not a prediction. Say so.
4. What was assumed because a column was empty.

## Step 4: decide what to change

Match the failing number to the skill that fixes it, and offer to run it:

| what is off | go to |
| --- | --- |
| Few people buy, many pass | `/founder-offer` (answer the top objection), `/founder-interview` (ask the ones who passed) |
| People buy once and do not return | `/founder-offer` (guarantee, reasons to come back), `/founder-brand` |
| Few people hear about it, or customers cost too much | `/founder-marketing`, `/founder-sales` for businesses |
| Price too low for the unit to earn | `/founder-pricing` with the real cost |
| Cost per unit too high | `/founder-ops` (suppliers, waste, routines), then `/founder-cfo` to re-run |
| Fixed costs too heavy for the volume | `/founder-cfo` what-ifs, `/founder-ops` (hours, rent, tools) |

Then give one decision, not a menu: keep going, change one named thing and review
again in a set number of weeks, or stop. If it is stop, say what the founder keeps
(the lessons, the customer list, the supplier terms) and what would have to be true
to try again.

## Review rhythm

From `founder/launch.md`: a quick check at day 7, 14 and 30, then monthly. Each
time, update the same row, rerun, and compare with the last `founder/metrics.md`
before overwriting it, so the trend is in the answer ("up from 52% last review").

## Rules

- Real numbers only, from the founder's own records. Never invent a month, and
  never smooth a bad number.
- A good first week is not proof. Say how many months of data stand behind the
  call; with one row, say it is a first reading.
- Never soften a Stop. If the unit loses money, more volume makes it worse.
- Not financial or tax advice: for tax and accounts, the founder's accountant.

## Market and language

If `founder/market.json` exists and says country `VN`, or the user writes
Vietnamese, write `founder/metrics.md` in their language and show money in their
currency (VND like `45,000₫`). Platform commissions and payment fees belong in
`variable_cost`; ask for them if the revenue figure is before the platform's cut.

## Output

`founder/actuals.csv` and `founder/metrics.md`. Next: run the skill the table points
to, then rerun this one after the next review. `/founder-plan` includes
`founder/metrics.md` as "How it is going" the next time it compiles.
