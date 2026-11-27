---
name: founder-pitch
description: >-
  Your pitch writer, for founders who are raising money or asking a lender or
  partner. Optional: a profitable one-person company may never need it. Turns the
  business plan, one-pager and CFO numbers into a 10 slide story with speaker
  notes, a markdown deck outline, and the 15 hardest questions an investor or
  lender will ask with honest answers. Refuses to pitch an Incomplete verdict, and
  leads with what has to change on a Not yet. Use when the user says "pitch deck",
  "investor pitch", "raise money", "ask a lender", "loan application", "pitch Q&A",
  or "what will investors ask".
argument-hint: "[investor, lender or partner]"
---

# founder-pitch

This skill is only for founders who are raising money or asking a lender or a
partner for something. It is optional. A one-person company that is profitable may
never need it, and you should not build a deck just because the pack offers one.
Nothing here is legal, financial or tax advice.

## Step 0: check what you are allowed to pitch

Read `founder/business-plan.md`, `founder/one-pager.md`, `founder/numbers.json`
and `founder/cfo.md`, and the verdict at the top of the plan.

- Verdict Incomplete: stop. Say which numbers are missing and send the user to
  `/founder-cfo` and `/founder-plan`. Do not write a deck on missing numbers.
- Verdict Not yet: continue, but the deck and the Q&A lead with what has to change
  and the plan to change it. An honest "here is what we are fixing" beats a
  confident deck that falls apart on the first question.
- If `founder/market.json` exists, write in its language and use its currency.

Ask the user who the audience is (equity investor, bank or lender, partner,
grant body) because the ask and the questions differ.

## Step 1: the story in 10 slides

One idea per slide, each with a headline that states the point.

1. Problem: who has it, how they cope today, what it costs them.
2. Customer: the specific buyer, from `founder/idea.md` and the panel.
3. Solution: what you sell, in plain words, and the price.
4. Evidence: keep three kinds strictly separate and labelled. Simulated panel:
   projections from simulated buyers, not customers. Real interviews: count them,
   say who. Any real test (pre-sales, waitlist, pilot): the actual numbers. If
   there is no real evidence, say "none yet" on the slide.
5. Market: use only public figures with a source link. No invented TAM. If no
   sourced figure exists, describe the market in words and mark the size unknown.
6. Business model and unit economics: copied word for word from the CFO report
   (`founder/cfo.md`). Do not re-round, rephrase or improve a number.
7. Competition: from `founder/competitors.md`, with sources. Never invent a
   competitor or a claim about one.
8. Go to market: how the first customers are reached, from the marketing, launch
   and sales files, with the funnel numbers if `/founder-sales` was run.
9. Team: a placeholder the founder fills (names, relevant experience, gaps and who
   will fill them). Do not write a bio from nothing.
10. The ask and use of funds, then risks. The ask is taken from the CFO's cash
    needed number. Show how the money is split and what it buys by when. Close with
    the top risks and how each is handled.

## Step 2: speaker notes

For each slide, two to four sentences to say aloud, the one number to remember,
and the question the slide is likely to provoke. Mark every sentence that is a
guess as a guess.

## Step 3: the deck outline

Write `founder/pitch-deck.md` as markdown with one H2 per slide, in order, each
with its bullets and its speaker notes. Markdown stays the source. Offer to export
to slides or PDF afterwards, and if the user agrees, generate it from this file so
the two never drift apart.

## Step 4: the 15 hardest questions

Write `founder/pitch-qa.md`: the 15 questions an investor or lender will ask, each
with an honest answer drawn from the files and a source file named. Cover at least:
why now, why you, what real evidence of demand exists, how the price was set,
margin and break-even, what happens if sales are half the plan, what the cash
runway is, customer acquisition cost, who the competitors are and why customers
switch, what the biggest risk is, how the money is used, what the exit or
repayment looks like, what you will do if the first plan fails, and what you
have not figured out yet.

Where the files do not hold the answer, write `FOUNDER MUST ANSWER:` and say what
is needed. Do not fill the gap with a plausible answer.

## Step 5: the rules

Print these at the end of both files and follow them:

- Never present simulated panel quotes as testimonials.
- Never present projections as results.
- Never invent traction, customers, revenue or market size.
- Say what is a guess, and show it as a guess.
- Copy unit economics from the CFO report; do not adjust them for the deck.
- Every market figure and competitor fact carries a source link.
- Tell the audience about the biggest risk before they find it.

## Output

`founder/pitch-deck.md` and `founder/pitch-qa.md`. Next: none, the pack ends
here.
