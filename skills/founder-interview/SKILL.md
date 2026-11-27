---
name: founder-interview
description: >-
  Your customer-discovery coach. The consumer panel is simulated, so this skill
  makes you check it against 5 to 10 real people. It writes a screener and a Mom
  Test style interview script from your idea and the panel's top objections,
  tells you where to find people without breaking any site's rules, files each
  interview as a record, and tallies real commitment against the panel's buy
  rate with a plain recommendation. Use when the user says "customer interviews",
  "talk to customers", "validate with real people", "interview script", "mom
  test", or "did the panel get it right".
argument-hint: "[script | add | tally]"
---

# founder-interview

The simulated panel is a fast first read. It is not a customer. This skill sends
you to talk to real people, keeps a clean record of what they said, and compares
it with the panel. Real conversations are never invented or filled in by the
agent: the agent only writes what you report, in your words.

## Step 1: read what exists

Read `founder/idea.md`, `founder/customer.json` and `founder/panel/results.md`
if they exist. If `founder/market.json` exists, write the script in its language
and use its currency. If there is no idea yet, stop and send the user to
`/founder-idea`. Note the panel's top objections: each one becomes a probe in the
script, a thing to listen for, never a thing to suggest to the person.

## Step 2: write the screener

Write 3 to 5 questions that decide who qualifies, taken from `customer.json`:

- Do they have the problem now (not "would you ever")?
- When did it last happen?
- Do they already pay for something to solve it, and how much?
- Who decides and who pays?
- The disqualifier: someone who has never had the problem is a polite chat, not data.

Say who qualifies in one sentence, and who to politely skip.

## Step 3: write the interview script

Use the Mom Test rules: ask about their life and past behaviour, not your idea.
Never pitch the idea first, and never ask "would you buy this?", because people
lie politely about the future.

1. Warm-up: their role and a normal day (2 minutes).
2. The last time: "Tell me about the last time you ..." Then what they did, what
   it cost, what they tried, what they use now.
3. Real spending: "What do you pay today? When did you last pay? What would make
   you stop?" Past money is a fact, future money is a wish.
4. Probes from the panel: one open question per top objection, phrased about the
   past ("Has price ever stopped you buying something like this?").
5. Only now, one sentence on the idea, then listen. Ask for the price they expect
   before you say yours.
6. The commitment ask, picked to fit the business:
   - waitlist: leave a name and contact (a soft yes)
   - pre-order with money: pay a deposit or the full price now (a real yes)
   - paid pilot: three weeks at the real price (the strongest yes)
   A person who will not give time, a contact or money has told you the answer.
7. Close: "Who else should I talk to?"

Add a recording section: write notes straight after the call, keep the exact
words they used (quote), and note the commitment level, the price they said, the
objection and the reason.

## Step 4: where to find people

Name 3 to 5 places that fit this business, with a plain first message for each:

- Your existing customers or an email list, if any.
- Communities where the target customer already talks (forums, groups, clubs),
  following each group's rules. Ask first, never spam.
- Cold outreach by hand, one person at a time, to people who clearly have the
  problem. A short honest message: who you are, that you are researching and not
  selling, 15 minutes.
- Markets, shop floors and queues where the buyer is physically present.
- Do not scrape sites, buy lists, or break a platform's terms.

Warn the user: friends and family say yes to be kind. Their interviews are
filed but never counted. Aim for 5 to 10 strangers or real customers.

## Step 5: file each interview

After every call, the founder reports what happened and you file it, one record
per person:

```
python3 ${CLAUDE_SKILL_DIR}/interview.py add --id I04 --commitment preorder --source stranger --price-said 6.5 --objection "too far from work" --quote "I would pay today"
```

`--commitment` is one of `none`, `interest`, `waitlist`, `preorder`, `paid`.
`--source` is `stranger`, `customer`, `friend` or `colleague`. Use only what the
founder said. If a field is unknown, leave it out. Run
`python3 ${CLAUDE_SKILL_DIR}/interview.py check` to list broken or duplicate
records, and `python3 ${CLAUDE_SKILL_DIR}/interview.py template` for a blank one.

## Step 6: tally and read it

```
python3 ${CLAUDE_SKILL_DIR}/interview.py tally
```

Read `founder/interviews/results.md` aloud in plain words:

- The real commitment rate (preorder or paid) against the panel's buy rate.
- The objections that repeated, and whether the panel had predicted them.
- The prices people said, against the price in `founder/pricing.md`.
- The recommendation. Under 5 counted interviews: too few to trust, do more. If
  real people fall well short of the panel, go back to `/founder-offer` or
  `/founder-pricing`. Always trust real buyers over the panel.

State the limits: a small sample, only people you could reach, money committed
counts, a smile does not.

## Output

`founder/interviews/script.md` (screener, interview script, where to find
people), `founder/interviews/I01.json` onward (one record per person), and
`founder/interviews/results.md` plus `results.json` from the tally. Next:
`/founder-offer` or `/founder-pricing` if real people fall short, otherwise
`/founder-launch` to run a real-world test.
