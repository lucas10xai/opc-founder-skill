---
name: founder-sales
description: >-
  Your sales lead for selling to businesses or by direct outreach (agencies,
  SaaS, services, wholesale). Defines the ideal customer profile, writes the
  one-line offer and the cheapest paid pilot, drafts the first message, follow
  ups, call script and objection answers in the customer's language, sets up the
  pipeline and works out how many conversations a week it takes to hit the target,
  with CAC and payback checked against the CFO's numbers. Use when the user says
  "B2B", "sell to businesses", "find clients", "outreach", "cold email", "sales
  pipeline", "how many calls do I need", or "direct sales".
argument-hint: "[who you sell to]"
---

# founder-sales

Most of this pack leans toward consumers. If your customers are companies, or you
win them one conversation at a time, this skill fills the gap. It produces a
customer profile, a script, a pipeline and a funnel calculation. It does not
promise any result: every conversion rate here is your guess until real
conversations replace it.

Read `founder/idea.md`, `founder/numbers.json`, `founder/offer.md`,
`founder/pricing.md` and `founder/market.json` if they exist. When `market.json`
exists, write everything the customer will read in its language and use its
currency.

## Step 1: the ideal customer profile

Ask only for what the files do not already answer. Then write down:

- Company type and size (a range, for example 5 to 50 staff), and the sectors to
  start with. Prefer one sector first.
- The role that buys (signs and pays) and the role that uses (lives with it daily).
  They are often different people, and each needs a different message.
- The trigger event: the moment a company starts looking (a new hire, a deadline, a
  complaint, a new regulation, a funding round, a busy season).
- Where they can be found, by hand and within the terms of each site: public
  directories and trade association member lists, LinkedIn-style search done by
  hand, industry communities and events, and for Vietnam also Zalo and Facebook
  groups. No scraping against a site's terms, no bought lists of private data.
- Who is not a fit, so you can say no early.

Save as `founder/icp.md`.

## Step 2: the offer and the cheapest paid pilot

Write the offer as one sentence a buyer can say yes to: who it is for, the result
they get, by when, at what price. Then design the cheapest paid pilot: a small,
fixed scope, a fixed price and a fixed end date, that lets a buyer try it without a
long contract. A paid pilot is better evidence than a free trial, because a company
that pays has decided something. State the price, what is included and what happens
at the end.

## Step 3: outreach

Write each piece in the customer's language, short and specific to the profile:

- First message (email, LinkedIn-style note or Zalo message): who you are in one
  line, the trigger you noticed, the one result you offer, one easy question.
  Under 100 words.
- Two follow ups, a few days apart, each adding something new rather than "just
  checking in".
- A call script of 15 to 20 minutes: opening, discovery questions (what they do
  today, what it costs them, who else decides, what happened last time they tried
  to fix it, what a good result looks like, by when), the pilot offer, and the
  agreed next step.
- Objection answers. If `founder/panel/results.md` and `founder/competitors.md`
  exist, draw the objections and the competitor comparisons from them and cite
  which file each came from. If they do not exist, write the common ones (price,
  timing, "we already have a supplier", "send me an email") and mark them as
  untested.

Never invent a client, a testimonial, a number or a competitor claim. Use only what
the files and real conversations support.

## Step 4: the pipeline and the funnel numbers

Define the stages a deal passes through (for example contacted, replied,
discovery call, proposal, signed), and for each: what moves a deal forward, what
stalls it, and when to drop it.

Then write `founder/funnel.json` (see `${CLAUDE_SKILL_DIR}/funnel.example.json`):
the monthly customer target, first-month deal value, contribution per customer per
month and expected lifetime in months (take contribution from `founder/numbers.json`,
do not guess it), the stage conversions, the sales cycle in days, how many first
contacts one person can make a day, and monthly ad or tool spend if any.

Run:

```
python3 ${CLAUDE_SKILL_DIR}/funnel.py founder/funnel.json --out founder/sales-funnel.md
```

The tool works backwards from the target to the first contacts needed per month
and per selling day, says whether your daily capacity is enough, and gives CAC,
LTV to CAC and payback in months. It flags LTV:CAC under 3 and payback over 12
months, and it refuses a stage conversion of 0 or above 1. Copy its numbers into
`founder/sales.md` exactly. Conversion rates are guesses until the first 30
conversations; say so and re-run the tool with real ones.

CAC here counts only spend you give it. Your own time is not counted, so state
what your hours are worth next to it.

## Step 5: the weekly sales review

End `founder/sales.md` with a review to run every week, with the answers written
down: how many new conversations started against the number the funnel needs, how
many replies, calls, proposals and signatures, what the real conversion of each
stage was, which deals are stuck and why, which objection came up most, what
changed in the message as a result, and the funnel numbers re-run with real rates.

## Running /founder-consumer for businesses

The buyer panel also works for companies. In `founder/customer.json` set:

- `"kind": "business"` (the values are `consumer` or `business`).
- `"income_line"`: a sentence with an `{amount}` placeholder, for example
  `"Your team spends about {amount} a year on tools like this."`. For a business
  panel, a segment's `income` means that yearly spend.

Make the segments company types, the behaviours buying styles (champion-led,
procurement-led, trial-first), and the objections the procurement ones (security
review, switching cost, budget cycle). The panel is still simulated buyers, not
customers: confirm with real conversations.

## Entering a B2B business in /founder-cfo

In `founder/numbers.json` set `"volume_period": "month"`. Then `plan_per_day` and
`ramp_per_day` mean units per month (the field names stay the same). Use a unit
such as `client-month`, so one unit is one client for one month. Put the monthly
fee as the price and the cost of serving one client for a month as the variable
cost.

## Output

`founder/icp.md`, `founder/sales.md` and `founder/funnel.json` (the input to the
tool), plus `founder/sales-funnel.md` from the tool. Next: `/founder-plan`.
