# The Founder skill

Seventeen Claude skills that test a business before you launch it, and check it
once it is live. Free, MIT, no signup, no API key, nothing to connect.

`skills/founder-board` `skills/founder-marketing` `skills/founder-cfo`
`skills/founder-consumer` `skills/founder-launch` `skills/founder-pricing`
`skills/founder-offer` `skills/founder-competitors` `skills/founder-brand`
`skills/founder-ops` `skills/founder-plan` `skills/founder-interview`
`skills/founder-compliance` `skills/founder-sales` `skills/founder-metrics`
`skills/founder-pitch` `skills/founder-run`

One of them is your board of directors, trained on the frameworks of Alex
Hormozi, Peter Thiel and Steve Jobs. One is your marketing director. One is your
CFO and finds your real profit margins. And one is the consumer panel: it spins
up 100 buyer agents trained on your target customer and runs your business
through 100 buyer scenarios.

So you know how to launch, how to market and how to actually make money, before
you spend thousands of dollars finding out the hard way.

## Install

Paste this repo link into Claude and say `install skill`:

```
https://github.com/lucas10xai/opc-founder-skill

install skill
```

Or as a plugin, in Claude Code:

```
/plugin marketplace add lucas10xai/opc-founder-skill
/plugin install opc-founder-skill@opc-founder-skill
```

Claude Code namespaces plugin skills, so installed as a plugin they show up as
`/opc-founder-skill:founder-board` and so on. Copy the folders instead if you want
plain `/founder-board`:

```bash
git clone https://github.com/lucas10xai/opc-founder-skill.git
cp -r opc-founder-skill/skills/founder-* ~/.claude/skills/
```

Project-local instead of global: copy the same folders into your repo's
`.claude/skills/`. No Claude Code at all? Paste any single `SKILL.md` at the top
of a chat and it runs as a mode. You lose the sub-agents and the Python tools,
but the method works.

The tools need Python 3.8 or newer. Nothing to pip install.

Working in Vietnam? Say so (or run `/founder-run`, which asks once and writes
`founder/market.json`). Every skill then reads its `locale-vn.md`, counts in VND,
and writes in Vietnamese. Examples in VND: `skills/founder-cfo/example.vn.json` and
`skills/founder-consumer/customer.example.vn.json`.

## The seventeen

| command | job | what it does |
| --- | --- | --- |
| `/founder-board` | Board of Directors | Three board members, each a sub-agent applying one published framework (Offers, from *$100M Offers*; Monopoly, from *Zero to One*; Product, from Isaacson's *Steve Jobs*), score the idea, name what would kill it and vote. |
| `/founder-competitors` | Competitor Scout | Maps direct competitors, indirect ones and substitutes from public sources, with prices, positioning and what their customers complain about, every fact linked. |
| `/founder-consumer` | Consumer Panel | Spins up a swarm of buyer agents (100 by default) from your target customer, each with its own income, habits and objection, and tallies who buys, who doesn't and why. |
| `/founder-pricing` | Pricing Strategist | Turns the panel's price answers into an acceptable price range, sets it against competitors and your margin, and picks what to test. |
| `/founder-offer` | Offer Architect | Builds the offer stack (bonuses, guarantee, real urgency, a name) that answers the panel's objections, then re-tests it on the panel. |
| `/founder-cfo` | CFO | Unit economics: contribution per sale, the real profit margin, break-even per day, year 1 month by month, cash needed, payback, what-ifs. |
| `/founder-marketing` | Marketing Director | Positioning, the channels your buyers use, a dated 30-day launch campaign, ten hooks and the most you can pay for a customer. |
| `/founder-brand` | Brand Designer | Name candidates with the trademark, domain and handle checks to run, a voice, a promise and a brief for the look. |
| `/founder-ops` | Operations Manager | Suppliers, staffing, day-one routines, tools, the permits to check and a risk register, feeding real costs back to the CFO. |
| `/founder-launch` | Launch Lead | A cheap real-world test first, then a dated countdown, the launch-day run sheet and the first 30 days. |
| `/founder-plan` | Business Planner | Compiles everything into one business plan with a verdict computed from the numbers: Profitable, Not yet or Incomplete. |
| `/founder-interview` | Customer Discovery Coach | The panel is simulated; this checks it against 5 to 10 real people. A screener and interview script, a record for each conversation, and the real pay-or-pre-order rate set beside the panel's buy rate. Friends are listed but not counted. |
| `/founder-compliance` | Compliance Checklist | Licences, tax, invoicing, premises, employment and advertising rules to confirm for your country and business, each with the official page to check, who confirms it and the lead time before launch. It refuses to state a rule it cannot source. |
| `/founder-sales` | Sales Lead | For businesses that sell to businesses: the ideal customer, outreach and follow-ups, a call script, and the funnel maths (conversations needed a week, CAC, LTV to CAC, payback). |
| `/founder-metrics` | Performance Analyst | After launch: real sales and costs against the plan, month by month. On track, change something or stop and rethink, with the failing number named, and year 1 redrawn from the real months. |
| `/founder-pitch` | Pitch Writer | Only if you are raising money or asking a lender: a 10-slide outline and the 15 hardest questions, built from the plan's own numbers. Never invents traction. |
| `/founder-run` | Chief of Staff | Sets the market once, sees what is already in `founder/`, and runs the next skill in order. |

## How to use it

Run them in this order. Each one reads what the others wrote, in a `founder/`
folder in your project.

```
board -> competitors -> consumer -> pricing -> offer -> cfo -> compliance -> marketing -> brand -> ops -> launch -> plan
          (interview in parallel after consumer; sales for B2B; metrics after launch; pitch if raising)
```

An example: a matcha café in Toronto, iced matcha lattes at $6.50 a cup. (Every
input is in the example files in this repo, so you can run the tools on it.)

1. **`/founder-board`** writes `founder/idea.md` from what you told it and puts it
   in front of three board members. Each scores it, lists the risks and votes:
   fund, fund if, or pass. The conditions become a checklist for the rest.
2. **`/founder-competitors`** maps the matcha bars and coffee shops within walking
   distance, what they charge for a latte and what their reviews complain about.
3. **`/founder-consumer`** builds the target customer (urban professionals, 24 to
   38, who buy coffee most days), deals 100 buyer cards across income, habits and
   objections, and runs one sub-agent per buyer. Back comes who buys, who passes,
   the reasons in their words ("my coffee place is closer", "$6.50 is steep for a
   drink") and what would flip a no.
4. **`/founder-pricing`** reads the panel's four price answers per buyer into a
   price range and checks $6.50 against it and against the competitors.
5. **`/founder-offer`** answers the top objections with the offer (a launch-week
   price, a loyalty card) and re-runs a quick panel to see if the buy rate moves.
6. **`/founder-cfo`** runs the unit economics. With the example numbers: each cup
   leaves $4.76 after its own costs, break-even is 186 cups a day, the profit
   margin at the planned 383 cups a day is 38%, year 1 makes $93,926 on operations
   after a slow ramp, the $25,280 startup spend is earned back in month 8, and the
   founder needs $34,092 in cash before it pays for itself.
7. **`/founder-marketing`**, **`/founder-brand`**, **`/founder-ops`** and
   **`/founder-launch`** turn it into a 30-day campaign, a name and a look, the
   suppliers and routines, and a dated launch that starts with a pop-up to test
   real buyers.
8. **`/founder-plan`** compiles `founder/business-plan.md`. Its verdict is
   computed, not written: Profitable only if every unit earns money, year 1 makes
   a profit, break-even fits capacity, enough of the panel buys and, once five or
   more real people have been interviewed, enough of them paid or pre-ordered.
   `compile.py --html` gives a page you can print to PDF; `compile.py --vault
   <folder>` writes the plan into an Obsidian vault (or a Notion markdown import).
9. **`/founder-metrics`**, once you are open: put the real sales and costs in
   `founder/actuals.csv` each week and it tells you if you are on plan.

You can also run any one on its own. `/founder-consumer --quick` on an idea you
are only thinking about is a good way to find out if you should.

## The tools

Eight of them, all standard-library Python. None touch the network.

```bash
python3 skills/founder-cfo/unit_economics.py founder/numbers.json --out founder/cfo.md   # margins, break-even, year 1
python3 skills/founder-consumer/panel.py init --customer founder/customer.json --pitch founder/pitch.md
python3 skills/founder-pricing/van_westendorp.py founder/panel/answers --price 6.50       # the acceptable price range
python3 skills/founder-interview/interview.py tally                                        # real people against the panel
python3 skills/founder-sales/funnel.py founder/funnel.json                                 # conversations needed, CAC, payback
python3 skills/founder-metrics/metrics.py founder/numbers.json founder/actuals.csv         # plan against reality
python3 skills/founder-plan/compile.py --dir founder                                     # the plan and its verdict
python3 skills/founder-run/status.py                                                      # where you are and what is next
```

**`unit_economics.py`** reads one JSON (example: `skills/founder-cfo/example.json`)
and reports contribution, break-even, the margin at plan, year 1 by month, cash
needed, payback, the lowest price that still breaks even, and what-ifs including a
price against volume grid. Money shows in the file's `currency` (USD, VND...). Every
number traces to an input; a missing field is an error, never a guess.

**`panel.py`** deals persona cards from your target customer (same seed, same
cards), writes one brief per buyer, checks the answers and tallies them. It never
answers for a buyer.

**`van_westendorp.py`** reads four price answers per buyer (from the panel, or a
CSV from a real survey) and finds the points of marginal cheapness and
expensiveness, the optimal and the indifference price.

**`interview.py`** files one record per real conversation and tallies them. People
who are friends are listed but not counted, because they say yes to be kind.

**`funnel.py`** works a sales target backwards through your stages to the number of
first conversations you need, and the CAC and payback if you give it a spend.

**`metrics.py`** compares `numbers.json` with `actuals.csv` and gives a call, a
table of plan against real, and a reforecast of year 1.

**`compile.py`** assembles the plan and computes the verdict.

**`status.py`** reads `founder/` and names the next skill; it can also write
`founder/market.json`.

```bash
python3 -m unittest discover -s tests -v
```

## Fine print

**The board applies published frameworks. It is not those people.** The three
lenses are short summaries, in our words, of ideas from *$100M Offers* by Alex
Hormozi, *Zero to One* by Peter Thiel with Blake Masters, and Walter Isaacson's
biography of Steve Jobs. The board never speaks as them, quotes them or claims
they endorse anything. This project is not affiliated with any of them.

**The consumer panel is simulated buyers, not customers.** It is a fast, cheap way
to find objections, segments and wording before you spend. It is not a forecast:
language models lean agreeable, so read the buy rate as an upper bound, and
confirm the big calls with real people: `/founder-interview` is built for that,
and `/founder-launch` starts with a real test too. Panel answers are research;
never use them as testimonials.

**The numbers are only as good as the inputs.** The CFO marks every estimate as an
estimate and asks for real quotes. Check costs with suppliers and the structure,
payroll and tax with an accountant.

**Research uses public sources, with links.** No invented competitors, prices,
reviews or quotes. No scraping against a site's terms.

**Not financial, legal or tax advice.** Permits, trademarks and claims depend on
where you are. The skills tell you what to check and where; a professional
confirms it.

## Files

```
skills/founder-board/        SKILL.md, lenses.md, locale-vn.md
skills/founder-competitors/  SKILL.md, locale-vn.md
skills/founder-consumer/     SKILL.md, panel.py, customer.example.json, pitch.example.md, *.vn.* examples, locale-vn.md
skills/founder-interview/    SKILL.md, interview.py, interview.example/
skills/founder-pricing/      SKILL.md, van_westendorp.py, locale-vn.md
skills/founder-offer/        SKILL.md, locale-vn.md
skills/founder-cfo/          SKILL.md, unit_economics.py, example.json, example.vn.json, locale-vn.md
skills/founder-compliance/   SKILL.md, locale-vn.md
skills/founder-marketing/    SKILL.md, locale-vn.md
skills/founder-sales/        SKILL.md, funnel.py, funnel.example.json
skills/founder-brand/        SKILL.md, locale-vn.md
skills/founder-ops/          SKILL.md, locale-vn.md
skills/founder-launch/       SKILL.md, locale-vn.md
skills/founder-metrics/      SKILL.md, metrics.py, actuals.example.csv
skills/founder-plan/         SKILL.md, compile.py
skills/founder-pitch/        SKILL.md
skills/founder-run/          SKILL.md, status.py
tests/                       the tests for every tool
```

Your own files live in `founder/` in your project. The skills read each other's.

## Made by

Made by Lucas from [opcaios.org](https://opcaios.org).

## License

MIT. Take it, change it, ship it.
