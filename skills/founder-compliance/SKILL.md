---
name: founder-compliance
description: >-
  Your compliance checklist builder (not a lawyer). Works out which registrations,
  taxes, licences, permits, safety rules, employment duties, consumer and advertising
  rules, data and platform rules, and trademark steps apply to this business in this
  place, with an official source link for each, who confirms it, how long it takes and
  where it sits in the launch countdown. Flags what is most likely to block a launch.
  Use when the user says "what permits do I need", "is this legal", "compliance",
  "licences", "do I need to register", or "what do I need before I open".
argument-hint: "[country and business type]"
---

# founder-compliance

Rules differ by country, city and business type, and they change. This skill builds
a checklist of what to check and where, so nothing that blocks the launch is found
the week before. It is a checklist builder, not a lawyer: every row needs
confirmation from the authority, an accountant or a lawyer.

## Step 1: what and where

Read `founder/market.json` (country), `founder/idea.md` (what the business sells and
to whom) and `founder/ops.md` (premises, staff, suppliers, sales channels). If the
country or the business type is missing, ask. Do not assume a country. Note whether
the business sells online, handles food, health, money or children, collects customer
data, imports or exports, or employs staff, because each one adds rows.

## Step 2: find official sources

For each row, search the web for the official government source (a registry, tax
authority, regulator or legal database). Open the page and confirm it exists and
covers the point. Use only links you have actually opened. If you cannot find or
verify a source, do not state the rule: write "check the current rule at <the
authority's site>" or "source not found, ask the authority". Never state a tax rate,
threshold, fee or deadline from memory. Write the date you checked each link.

## Step 3: build the checklist

Group the rows under these eight headings, and drop a heading only by writing "not
applicable" with the reason:

1. Company form and registration.
2. Tax and invoicing.
3. Sector licences and permits (food, health, finance, education, import and export, data).
4. Premises and safety.
5. Employment.
6. Consumer protection and advertising claims.
7. Data privacy and e-commerce platform rules.
8. Trademark and domain.

Each row is a table line with these columns: what; why it applies to this business;
official source link; who confirms it (authority, accountant or lawyer); when it must
be done relative to launch (for example "before opening" or "launch minus 6 weeks");
cost if a public source states it, otherwise "unknown"; status (todo, in progress,
done, or not applicable with the reason).

## Step 4: lead times and blockers

For each licence or registration, find the stated processing time from the official
source, or write "unknown, ask the authority". Add the lead time to the target launch
date and write the latest start date for each item. Then list the items most likely
to block a launch: the ones with a long or unknown lead time, or without which you
cannot legally sell or open. Put them at the top.

## Step 5: connect to the rest of the pack

- In `founder/ops.md`, change the permits section only to point to `founder/compliance.md`.
  Do not copy rules into it.
- Costs found from a public source: show them to the user and ask. Add them to the
  startup costs in `founder/numbers.json` only after the user confirms.
- Dates and deadlines go to `/founder-launch` as inputs to the countdown.

## Step 6: say the limits plainly

Start the file with this, in the user's language: rules change and differ by place,
this is a checklist to confirm and not legal, tax or financial advice, and every row
must be confirmed with the authority or a professional before acting.

## Market and language

If `founder/market.json` exists and says country `VN`, or the user is clearly in Vietnam or writes
Vietnamese, also read `${CLAUDE_SKILL_DIR}/locale-vn.md`. Write every file in the user's language
(Vietnamese when they write Vietnamese) and use the currency from `founder/market.json`
(VND is shown like `45,000₫`). Treat the Vietnam notes as places to check, not as sourced rules.

## Rules

- Never invent a rule, a fee, a deadline or a link.
- One row, one source. If two sources disagree, show both and ask the authority.
- Say "not applicable" only with a reason.
- Keep the user's decisions: a row marked done stays done until they change it.

## Output

`founder/compliance.md` with the checklist, the blockers list and the lead times.
Next: `/founder-launch` builds the countdown using these dates.
