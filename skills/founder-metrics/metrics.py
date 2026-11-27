#!/usr/bin/env python3
"""After launch: plan against reality, for founder-metrics. Standard library only, no network.

Takes the CFO's plan (founder/numbers.json) and what really happened
(founder/actuals.csv, one row per month, updated as the month fills up) and says
whether the business is on track, which number is off, and what year 1 looks like
now that part of it is known.

    python3 metrics.py founder/numbers.json founder/actuals.csv
    python3 metrics.py founder/numbers.json founder/actuals.csv --out founder/metrics.md
    python3 metrics.py founder/numbers.json founder/actuals.csv --json
    python3 metrics.py --template                  # print the CSV header

actuals.csv columns (plain numbers, no currency signs; leave a cell empty if unknown):

    month           1 to 12, the month of year 1 this row is about (required)
    units           units sold so far this month (required)
    days            selling days covered by this row (default: the whole month). A row
                    for the first 7 days is month 1 with days 7. Ignored when
                    numbers.json has "volume_period": "month".
    revenue         money taken so far (default: units times the planned price, marked assumed)
    variable_cost   total variable cost so far (default: units times the planned cost, marked assumed)
    fixed_cost      fixed costs so far (default: the planned fixed costs for those days)
    ad_spend        what you spent to win customers
    new_customers   new customers won

One row per month; replace the row as the month fills up. Optional in numbers.json:
"max_cac", the most you can pay to win one customer.

The call, from the latest row (change the bars with --amber and --red):

    stop and rethink   each unit loses money at the real price and cost, or sales were
                       under 60% of plan in each of the last two months
    change something   sales under 80% of plan, unit profit more than 15% under plan,
                       or customers cost more than max_cac
    on track           none of the above

Nothing is estimated for you. Missing columns fall back to the plan and the report
says so. The reforecast keeps the real months, runs the rest of year 1 at the plan
scaled by how far real sales are from plan, and uses real price and cost when every
row has them.
"""

import argparse
import csv
import importlib.util
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
COLUMNS = ["month", "units", "days", "revenue", "variable_cost", "fixed_cost", "ad_spend", "new_customers"]


class MetricsError(Exception):
    pass


def _ue():
    path = os.path.join(HERE, "..", "founder-cfo", "unit_economics.py")
    spec = importlib.util.spec_from_file_location("founder_unit_economics", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _num(v, field, line):
    if v is None or str(v).strip() == "":
        return None
    try:
        return float(str(v).replace(",", "").replace("$", "").replace("₫", "").strip())
    except ValueError:
        raise MetricsError("row %d: %s is not a number: %r" % (line, field, v))


def read_actuals(path):
    rows, seen = [], set()
    try:
        fh = open(path, newline="", encoding="utf-8")
    except FileNotFoundError:
        raise MetricsError("no such file: %s (make it with: metrics.py --template)" % path)
    with fh:
        reader = csv.DictReader(fh)
        missing = {"month", "units"} - set(reader.fieldnames or [])
        if missing:
            raise MetricsError("%s needs the columns: %s" % (path, ", ".join(sorted(missing))))
        for i, raw in enumerate(reader, start=2):
            if not any((v or "").strip() for v in raw.values()):
                continue
            r = {c: _num(raw.get(c), c, i) for c in COLUMNS}
            if r["month"] is None or r["month"] != int(r["month"]) or not 1 <= r["month"] <= 12:
                raise MetricsError("row %d: month must be a whole number from 1 to 12" % i)
            r["month"] = int(r["month"])
            if r["month"] in seen:
                raise MetricsError("row %d: month %d appears twice (one row per month: replace it)" % (i, r["month"]))
            seen.add(r["month"])
            if r["units"] is None or r["units"] < 0:
                raise MetricsError("row %d: units is needed and cannot be negative" % i)
            if r["days"] is not None and r["days"] <= 0:
                raise MetricsError("row %d: days must be above zero" % i)
            rows.append(r)
    if not rows:
        raise MetricsError("%s has no rows yet" % path)
    return sorted(rows, key=lambda r: r["month"])


def analyse_actuals(spec, rows, amber=0.8, red=0.6):
    ue = _ue()
    plan = ue.analyse(spec)
    per = plan["period"]
    full = 1.0 if per == "month" else float(spec.get("days_per_month", 30))
    price, var, fixed = plan["price"], plan["variable_per_unit"], plan["fixed_monthly"]
    plan_contrib = price - var

    out, cum_a, cum_p = [], -plan["startup"], -plan["startup"]
    for r in rows:
        days = full if per == "month" or r["days"] is None else r["days"]
        share = days / full
        planned = plan["months"][r["month"] - 1]
        units_plan = planned["per_day"] * days
        profit_plan = units_plan * (price - var) - fixed * share
        assumed = [c for c, v in (("revenue", r["revenue"]), ("variable_cost", r["variable_cost"]),
                                  ("fixed_cost", r["fixed_cost"])) if v is None]
        revenue = r["revenue"] if r["revenue"] is not None else r["units"] * price
        variable = r["variable_cost"] if r["variable_cost"] is not None else r["units"] * var
        fixed_cost = r["fixed_cost"] if r["fixed_cost"] is not None else fixed * share
        profit = revenue - variable - fixed_cost
        cum_a += profit
        cum_p += profit_plan
        out.append({
            "month": r["month"], "days": days, "partial": per == "day" and share < 1, "units": r["units"], "units_plan": units_plan,
            "per_day": r["units"] / days, "per_day_plan": planned["per_day"],
            "units_vs_plan": (r["units"] / units_plan) if units_plan else None,
            "price": (revenue / r["units"]) if r["units"] else price,
            "unit_cost": (variable / r["units"]) if r["units"] else var,
            "revenue": revenue, "variable": variable, "fixed": fixed_cost, "profit": profit,
            "profit_plan": profit_plan, "cumulative": cum_a, "cumulative_plan": cum_p,
            "assumed": assumed, "ad_spend": r["ad_spend"], "new_customers": r["new_customers"],
            "have": {"revenue": r["revenue"] is not None, "variable": r["variable_cost"] is not None,
                     "fixed": r["fixed_cost"] is not None},
        })

    latest = out[-1]
    contrib = latest["price"] - latest["unit_cost"]
    reasons, level = [], 0  # 0 on track, 1 change something, 2 stop and rethink
    if contrib <= 0:
        level = 2
        reasons.append("Each %s loses money at the real price and cost (%s a %s)." % (
            plan["unit"], ue.money(contrib, plan["currency"]), plan["unit"]))
    elif contrib < 0.85 * plan_contrib:
        level = max(level, 1)
        reasons.append("Profit per %s is %s against %s planned (more than 15%% under)." % (
            plan["unit"], ue.money(contrib, plan["currency"]), ue.money(plan_contrib, plan["currency"])))
    last_two = [o["units_vs_plan"] for o in out[-2:] if o["units_vs_plan"] is not None]
    if len(out) >= 2 and len(last_two) == 2 and all(x < red for x in last_two):
        level = 2
        reasons.append("Sales were under %.0f%% of plan in each of the last two months." % (red * 100))
    elif latest["units_vs_plan"] is not None and latest["units_vs_plan"] < amber:
        level = max(level, 1)
        reasons.append("Sales are %.0f%% of plan in month %d (the bar is %.0f%%)." % (
            latest["units_vs_plan"] * 100, latest["month"], amber * 100))

    spend = sum(o["ad_spend"] for o in out if o["ad_spend"] and o["new_customers"])
    won = sum(o["new_customers"] for o in out if o["ad_spend"] and o["new_customers"])
    cac = spend / won if won else None
    max_cac = spec.get("max_cac")
    if cac is not None and max_cac is not None and cac > float(max_cac):
        level = max(level, 1)
        reasons.append("A customer costs %s to win; the most you can pay is %s." % (
            ue.money(cac, plan["currency"]), ue.money(float(max_cac), plan["currency"])))

    # reforecast: real months as they happened, the rest of the plan scaled by real vs planned sales
    total_plan_units = sum(o["units_plan"] for o in out)
    ratio = sum(o["units"] for o in out) / total_plan_units if total_plan_units else 1.0
    real = {o["month"]: o["per_day"] for o in out}
    ramp = [real.get(m, plan["months"][m - 1]["per_day"] * ratio) for m in range(1, 13)]
    spec2 = json.loads(json.dumps(spec))
    spec2["ramp_per_day"] = ramp
    spec2["plan_per_day"] = ramp[-1]
    total_units = sum(o["units"] for o in out)
    if total_units and all(o["have"]["revenue"] for o in out):
        spec2["price"] = sum(o["revenue"] for o in out) / total_units
    if total_units and all(o["have"]["variable"] for o in out):
        spec2["variable"] = [{"label": "Real variable cost per unit", "cost": sum(o["variable"] for o in out) / total_units}]
    if all(o["have"]["fixed"] for o in out):
        spec2["fixed_monthly"] = [{"label": "Real fixed costs", "cost": sum(o["fixed"] / (o["days"] / full) for o in out) / len(out)}]
    if spec2["price"] <= 0:
        raise MetricsError("the real price works out at zero or less")
    reforecast = ue.analyse(spec2)

    return {
        "business": plan["business"], "unit": plan["unit"], "unit_plural": plan["unit_plural"],
        "currency": plan["currency"], "period": per,
        "status": ["on track", "change something", "stop and rethink"][level], "level": level,
        "reasons": reasons, "rows": out, "plan": plan, "reforecast": reforecast, "sales_vs_plan": ratio,
        "cac": cac, "max_cac": float(max_cac) if max_cac is not None else None,
    }


def report(a):
    ue = _ue()
    cur, per, u = a["currency"], a["period"], a["unit"]
    M = lambda v: ue.money(v, cur)
    W = lambda v: ue.whole(v, cur)
    inf = lambda v: "never" if math.isinf(v) else "{:,.0f}".format(math.ceil(v))
    L = ["# How it is going: %s" % (a["business"] or "your business"), "",
         "**Status: %s.**" % a["status"], ""]
    if a["reasons"]:
        L += ["- %s" % r for r in a["reasons"]]
    else:
        L.append("- Nothing is under the bars: sales, unit profit and customer cost are where the plan put them.")
    L += ["", "## Plan against reality", "",
          "| month | %s a %s (plan) | %s a %s (real) | vs plan | profit (plan) | profit (real) | cumulative (real) |" % (a["unit_plural"], per, a["unit_plural"], per),
          "| ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for o in a["rows"]:
        L.append("| %d%s | %s | %s | %s | %s | %s | %s |" % (
            o["month"], " (%g days)" % o["days"] if o["partial"] else "",
            "{:,.0f}".format(o["per_day_plan"]), "{:,.1f}".format(o["per_day"]),
            "n/a" if o["units_vs_plan"] is None else "%.0f%%" % (o["units_vs_plan"] * 100),
            W(o["profit_plan"]), W(o["profit"]), W(o["cumulative"])))
    L.append("")
    assumed = sorted({c for o in a["rows"] for c in o["assumed"]})
    if assumed:
        L += ["Not given, so the plan's figure was used: %s. Fill these in for a truer picture." % ", ".join(assumed), ""]
    last = a["rows"][-1]
    L += ["## The unit", "",
          "| | plan | real (latest month) |", "| --- | ---: | ---: |",
          "| Price | %s | %s |" % (M(a["plan"]["price"]), M(last["price"])),
          "| Cost per %s | %s | %s |" % (u, M(a["plan"]["variable_per_unit"]), M(last["unit_cost"])),
          "| Profit per %s | %s | %s |" % (u, M(a["plan"]["contribution"]), M(last["price"] - last["unit_cost"])), ""]
    if a["cac"] is not None:
        L += ["Customers cost %s each to win%s." % (M(a["cac"]), (" (the most you can pay: %s)" % M(a["max_cac"])) if a["max_cac"] is not None else ""), ""]
    p, r = a["plan"], a["reforecast"]
    L += ["## Year 1 now", "",
          "Real months kept as they happened; the rest of the year runs at the plan scaled to %.0f%% (real sales against planned so far)." % (a["sales_vs_plan"] * 100), "",
          "| | plan | reforecast |", "| --- | ---: | ---: |",
          "| Year 1 operating profit | %s | %s |" % (W(p["year1_profit"]), W(r["year1_profit"])),
          "| Break-even a %s | %s | %s |" % (per, inf(p["breakeven_per_day"]), inf(r["breakeven_per_day"])),
          "| Startup money earned back | %s | %s |" % (
              "month %d" % p["payback_month"] if p["payback_month"] else "not in year 1",
              "month %d" % r["payback_month"] if r["payback_month"] else "not in year 1"),
          "| Cash needed | %s | %s |" % (W(p["cash_needed"]), W(r["cash_needed"])), ""]
    if r["flags"]:
        L += ["Red flags on the reforecast:", ""] + ["- %s" % f for f in r["flags"]] + [""]
    L.append("_Real numbers from the founder's own records. The reforecast is arithmetic on them, not a prediction._")
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("numbers", nargs="?", help="the CFO's numbers.json")
    ap.add_argument("actuals", nargs="?", help="actuals.csv")
    ap.add_argument("--out", help="write the report here (markdown)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--amber", type=float, default=0.8, help="sales below this share of plan: change something")
    ap.add_argument("--red", type=float, default=0.6, help="sales below this share of plan two months running: stop")
    ap.add_argument("--template", action="store_true", help="print the CSV header and exit")
    a = ap.parse_args(argv)
    if a.template:
        print(",".join(COLUMNS))
        return 0
    if not a.numbers or not a.actuals:
        ap.error("give numbers.json and actuals.csv (or --template)")
    try:
        ue = _ue()
        res = analyse_actuals(ue.load(a.numbers), read_actuals(a.actuals), a.amber, a.red)
    except (MetricsError, ue.NumbersError) as e:
        print("error: %s" % e, file=sys.stderr)
        return 2
    if a.json:
        def clean(o):
            if isinstance(o, float) and math.isinf(o):
                return None
            if isinstance(o, dict):
                return {k: clean(v) for k, v in o.items()}
            if isinstance(o, list):
                return [clean(v) for v in o]
            return o
        print(json.dumps(clean({k: v for k, v in res.items() if k not in ("plan", "reforecast")}), indent=1))
        return 0
    text = report(res)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("%s. Wrote %s" % (res["status"].capitalize(), a.out))
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
