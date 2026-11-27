#!/usr/bin/env python3
"""Unit economics for founder-cfo. Standard library only, no network.

Takes one JSON file describing the business and prints the numbers a CFO would
check before a single dollar is spent: what one unit earns, the real margin at
the volume you plan, how many units a day you need to break even, what year 1
looks like month by month, and how long it takes to earn the startup money back.

    python3 unit_economics.py founder/numbers.json
    python3 unit_economics.py founder/numbers.json --out founder/cfo.md
    python3 unit_economics.py founder/numbers.json --json
    python3 unit_economics.py founder/numbers.json --price 7.00 --volume 0.8

The input (see example.json in this folder):

    business          name, for the report
    unit              what you sell one of: "cup", "order", "client-month"
    unit_plural       the plural of unit, if it is not unit + "s" (optional; Vietnamese: same word)
    price             price per unit, before tax
    variable          [{label, cost}]  cost of ONE unit: ingredients, packaging,
                      shipping, card fees, a per-unit commission
    fixed_monthly     [{label, cost}]  costs you pay every month whatever you sell:
                      rent, salaries, software, insurance
    startup           [{label, cost}]  one-off spend before you open
    days_per_month    selling days in a month (default 30)
    capacity_per_day  the most units a day you can physically sell (optional)
    plan_per_day      the volume you plan for once you are up and running
    ramp_per_day      12 numbers: units a day in each month of year 1
                      (optional; default = plan_per_day every month)
    currency          "USD" (default), "VND", "EUR", "GBP" or any code; sets how money
                      is shown. VND is shown without decimals: 45,000₫
    volume_period     "day" (default) or "month". With "month", days_per_month is
                      ignored and plan_per_day, ramp_per_day and capacity_per_day
                      count units per MONTH (the field names stay). Use it for
                      client-months, projects and anything sold a few times a month.

Every number in the report comes from that file. Nothing is looked up or
guessed. If a field is missing the tool says so instead of filling it in.

--price and --volume run a what-if without editing the file: --price replaces
the price, --volume scales every volume (0.8 = 20 percent fewer sales).
"""

import argparse
import json
import math
import sys


class NumbersError(Exception):
    pass


CURRENCIES = {  # code: (symbol, symbol goes before or after the number, decimals)
    "USD": ("$", "prefix", 2),
    "EUR": ("€", "prefix", 2),
    "GBP": ("£", "prefix", 2),
    "VND": ("₫", "suffix", 0),
}


def _cur(code):
    code = str(code or "USD").strip().upper()
    return CURRENCIES.get(code, (code + " ", "prefix", 2))


def money(v, currency="USD", decimals=None):
    """Format an amount in the spec's currency. Public: other tools reuse it."""
    symbol, where, dec = _cur(currency)
    if decimals is not None:
        dec = min(dec, decimals)
    sign = "-" if v < 0 else ""
    num = ("{:,.%df}" % dec).format(abs(v))
    return "%s%s%s" % (sign, num, symbol) if where == "suffix" else "%s%s%s" % (sign, symbol, num)


def whole(v, currency="USD"):
    return money(round(v), currency, 0)


def _money(v, cur="USD"):
    return money(v, cur)


def _whole(v, cur="USD"):
    return whole(v, cur)


def _sum(items, field):
    total = 0.0
    for i, it in enumerate(items or []):
        if not isinstance(it, dict) or "cost" not in it:
            raise NumbersError("%s[%d] needs a 'cost'" % (field, i))
        try:
            total += float(it["cost"])
        except (TypeError, ValueError):
            raise NumbersError("%s[%d].cost is not a number: %r" % (field, i, it["cost"]))
    return total


def load(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        raise NumbersError("no such file: %s" % path)
    except json.JSONDecodeError as e:
        raise NumbersError("%s is not valid JSON: %s" % (path, e))


def analyse(spec, price=None, volume=1.0):
    """Return a dict of every number in the report. Pure function, easy to test."""
    if "price" not in spec and price is None:
        raise NumbersError("'price' is missing")
    p = float(price if price is not None else spec["price"])
    if p <= 0:
        raise NumbersError("price must be above zero")
    period = spec.get("volume_period", "day")
    if period not in ("day", "month"):
        raise NumbersError("'volume_period' must be \"day\" or \"month\"")
    cur = str(spec.get("currency", "USD")).strip().upper()
    plural = spec.get("unit_plural") or "%ss" % spec.get("unit", "unit")
    days = 1.0 if period == "month" else float(spec.get("days_per_month", 30))
    var = _sum(spec.get("variable"), "variable")
    fixed = _sum(spec.get("fixed_monthly"), "fixed_monthly")
    startup = _sum(spec.get("startup"), "startup")

    if "plan_per_day" not in spec and "ramp_per_day" not in spec:
        raise NumbersError("give 'plan_per_day' or 'ramp_per_day' (12 numbers)")
    plan = float(spec.get("plan_per_day", 0)) * volume
    ramp = spec.get("ramp_per_day")
    if ramp is None:
        ramp = [plan] * 12
    else:
        if len(ramp) != 12:
            raise NumbersError("'ramp_per_day' needs 12 numbers, one per month (got %d)" % len(ramp))
        ramp = [float(v) * volume for v in ramp]
    if not plan:
        plan = ramp[-1]

    contribution = p - var
    contribution_pct = contribution / p
    breakeven_day = math.inf if contribution <= 0 else fixed / (contribution * days)
    plan_units_month = plan * days
    margin_at_plan = (contribution - (fixed / plan_units_month if plan_units_month else math.inf)) / p

    months = []
    cumulative = -startup
    payback_month = None
    for m, per_day in enumerate(ramp, start=1):
        units = per_day * days
        revenue = units * p
        variable_cost = units * var
        profit = revenue - variable_cost - fixed
        cumulative += profit
        if payback_month is None and cumulative >= 0:
            payback_month = m
        months.append({"month": m, "per_day": per_day, "units": units, "revenue": revenue,
                       "variable": variable_cost, "fixed": fixed, "profit": profit,
                       "cumulative": cumulative})
    year_profit = sum(m["profit"] for m in months)
    year_revenue = sum(m["revenue"] for m in months)
    # the cash you need: startup plus the deepest hole the monthly losses dig
    lowest = min([-startup] + [m["cumulative"] for m in months])
    cash_needed = -lowest

    capacity = spec.get("capacity_per_day")
    flags = []
    if contribution <= 0:
        flags.append("Each unit loses money before rent and salaries: the price is below the variable cost.")
    if capacity is not None and breakeven_day > float(capacity):
        flags.append("Break-even needs %.0f %s a %s but capacity is %s." % (breakeven_day, plural, period, capacity))
    if capacity is not None and plan > float(capacity):
        flags.append("The plan (%.0f a %s) is above capacity (%s)." % (plan, period, capacity))
    if year_profit < 0:
        flags.append("Year 1 loses money on operations (%s)." % _whole(year_profit, cur))
    if payback_month is None:
        flags.append("The startup spend is not earned back within year 1.")

    year_units = sum(m["units"] for m in months)
    # the price at which year 1 operating profit is exactly zero (profit is linear in price)
    breakeven_price = (var + 12 * fixed / year_units) if year_units > 0 else math.inf

    return {
        "business": spec.get("business", ""), "unit": spec.get("unit", "unit"),
        "currency": cur, "period": period, "unit_plural": plural,
        "price": p, "variable_per_unit": var, "contribution": contribution,
        "contribution_pct": contribution_pct, "fixed_monthly": fixed, "startup": startup,
        "plan_per_day": plan, "margin_at_plan": margin_at_plan, "breakeven_per_day": breakeven_day,
        "breakeven_price": breakeven_price,
        "capacity_per_day": capacity, "year1_revenue": year_revenue, "year1_profit": year_profit,
        "year1_after_startup": year_profit - startup, "payback_month": payback_month,
        "cash_needed": cash_needed, "months": months, "flags": flags,
        "variable_items": spec.get("variable", []), "fixed_items": spec.get("fixed_monthly", []),
        "startup_items": spec.get("startup", []),
    }


def sensitivity(spec):
    """The three what-ifs every plan should survive."""
    base = analyse(spec)
    rows = [("Base plan", base)]
    rows.append(("Price -10%", analyse(spec, price=base["price"] * 0.9)))
    rows.append(("Volume -20%", analyse(spec, volume=0.8)))
    worse = json.loads(json.dumps(spec))
    for it in worse.get("variable", []):
        it["cost"] = float(it["cost"]) * 1.15
    rows.append(("Unit costs +15%", analyse(worse)))
    return rows


def grid(spec, price_steps=(-0.2, -0.1, 0.0, 0.1, 0.2), volume_steps=(0.6, 0.8, 1.0, 1.2)):
    """Year 1 operating profit for every price step crossed with every volume step."""
    base = analyse(spec)["price"]
    rows = []
    for ps in price_steps:
        price = base * (1 + ps)
        rows.append({"price_step": ps, "price": price,
                     "profit": [analyse(spec, price=price, volume=v)["year1_profit"] for v in volume_steps]})
    return {"volume_steps": list(volume_steps), "rows": rows}


def report(spec, a):
    u = a["unit"]
    cur = a["currency"]
    per = a["period"]
    M = lambda v: _money(v, cur)
    W = lambda v: _whole(v, cur)
    L = []
    L.append("# Unit economics: %s" % (a["business"] or "your business"))
    L.append("")
    L.append("Every number below comes from the input file. Nothing is looked up or guessed.")
    L.append("")
    L.append("## One %s" % u)
    L.append("")
    L.append("| line | per %s |" % u)
    L.append("| --- | ---: |")
    L.append("| Price | %s |" % M(a["price"]))
    for it in a["variable_items"]:
        L.append("| %s | -%s |" % (it.get("label", "cost"), M(float(it["cost"]))))
    L.append("| **Contribution** (what each %s leaves to pay the fixed costs) | **%s** (%.0f%%) |"
             % (u, M(a["contribution"]), a["contribution_pct"] * 100))
    L.append("")
    L.append("## The margin that matters")
    L.append("")
    L.append("Fixed costs: %s a month (%s)." % (W(a["fixed_monthly"]), ", ".join(
        "%s %s" % (it.get("label", "cost"), W(float(it["cost"]))) for it in a["fixed_items"]) or "none given"))
    L.append("")
    be = a["breakeven_per_day"]
    L.append("- **Break-even: %s %s a %s.** Below that you lose money every month." % (
        "never (each unit loses money)" if math.isinf(be) else "{:,.0f}".format(math.ceil(be)), a["unit_plural"], per))
    L.append("- **Profit margin at your plan** (%s a %s): **%.0f%%** of every sale, after every cost." % (
        "{:,.0f}".format(a["plan_per_day"]), per, a["margin_at_plan"] * 100))
    bp = a["breakeven_price"]
    if not math.isinf(bp):
        L.append("- Lowest price that still breaks even over year 1 at your volume: %s (you plan %s)." % (M(bp), M(a["price"])))
    if a["capacity_per_day"] is not None:
        L.append("- Capacity: %s a %s." % (a["capacity_per_day"], per))
    L.append("")
    L.append("## Year 1, month by month")
    L.append("")
    L.append("| month | %s a %s | revenue | profit | cumulative (after %s startup) |" % (a["unit_plural"], per, W(a["startup"])))
    L.append("| ---: | ---: | ---: | ---: | ---: |")
    for m in a["months"]:
        L.append("| %d | %s | %s | %s | %s |" % (m["month"], "{:,.0f}".format(m["per_day"]), W(m["revenue"]),
                                             W(m["profit"]), W(m["cumulative"])))
    L.append("")
    L.append("- **Year 1 operating profit: %s** on %s of revenue." % (W(a["year1_profit"]), W(a["year1_revenue"])))
    L.append("- After the %s startup spend: %s." % (W(a["startup"]), W(a["year1_after_startup"])))
    L.append("- Startup money earned back: %s." % ("month %d" % a["payback_month"] if a["payback_month"] else "not within year 1"))
    L.append("- Cash you need before it pays for itself: **%s**." % W(a["cash_needed"]))
    L.append("")
    L.append("## What if")
    L.append("")
    L.append("| scenario | margin at plan | break-even a %s | year 1 profit |" % per)
    L.append("| --- | ---: | ---: | ---: |")
    for name, s in sensitivity(spec):
        be = s["breakeven_per_day"]
        L.append("| %s | %.0f%% | %s | %s |" % (name, s["margin_at_plan"] * 100,
                                              "never" if math.isinf(be) else "{:,.0f}".format(math.ceil(be)),
                                              W(s["year1_profit"])))
    L.append("")
    g = grid(spec)
    L.append("## Year 1 profit: price against volume")
    L.append("")
    L.append("Rows are the price, columns are how much you sell compared with the plan. A negative number is a loss.")
    L.append("")
    L.append("| price | " + " | ".join("%+.0f%% volume" % ((v - 1) * 100) if v != 1 else "plan volume" for v in g["volume_steps"]) + " |")
    L.append("| ---: |" + " ---: |" * len(g["volume_steps"]))
    for row in g["rows"]:
        label = M(row["price"]) + ("" if row["price_step"] == 0 else " (%+.0f%%)" % (row["price_step"] * 100))
        L.append("| %s | %s |" % (label, " | ".join(W(x) for x in row["profit"])))
    L.append("")
    if a["flags"]:
        L.append("## Red flags")
        L.append("")
        for f in a["flags"]:
            L.append("- %s" % f)
    else:
        L.append("No red flags in these numbers. They are only as good as the inputs: check every cost against a real quote.")
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("numbers", help="the business's numbers.json")
    ap.add_argument("--out", help="write the report here (markdown)")
    ap.add_argument("--json", action="store_true", help="print the numbers as JSON")
    ap.add_argument("--price", type=float, help="what-if price")
    ap.add_argument("--volume", type=float, default=1.0, help="what-if volume multiplier")
    args = ap.parse_args(argv)
    try:
        spec = load(args.numbers)
        if args.price is not None:
            spec = dict(spec, price=args.price)
        if args.volume != 1.0:
            spec = dict(spec)
            if "plan_per_day" in spec:
                spec["plan_per_day"] = float(spec["plan_per_day"]) * args.volume
            if "ramp_per_day" in spec:
                spec["ramp_per_day"] = [float(v) * args.volume for v in spec["ramp_per_day"]]
        a = analyse(spec)
    except NumbersError as e:
        print("error: %s" % e, file=sys.stderr)
        return 2
    if args.json:
        out = {k: v for k, v in a.items() if not k.endswith("_items")}
        for k in ("breakeven_per_day", "breakeven_price"):
            out[k] = None if math.isinf(out[k]) else out[k]
        print(json.dumps(out, indent=1))
        return 0
    text = report(spec, a)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("wrote %s" % args.out)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
