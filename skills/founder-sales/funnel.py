#!/usr/bin/env python3
"""Sales funnel maths for founder-sales. Standard library only.

Works backwards from the number of customers you want per month to the number of
first contacts you need, then checks capacity, CAC, LTV:CAC and payback.

Input is a JSON file (see funnel.example.json):
  business, currency, target_customers_per_month, deal_value,
  contribution_per_customer_month, expected_customer_months,
  stages [{name, conversion}], cycle_days, touches_per_day (optional),
  selling_days_per_month (default 21), ad_or_tool_spend_month (optional).

Usage:
  funnel.py funnel.json [--out sales-funnel.md] [--json]

Numbers are projections from your own conversion guesses, not results.
"""

import argparse
import json
import sys


class FunnelError(Exception):
    pass


def _num(spec, key, required=True, positive=True, default=None):
    if key not in spec or spec[key] is None:
        if required:
            raise FunnelError("missing %s" % key)
        return default
    v = spec[key]
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise FunnelError("%s must be a number" % key)
    if positive and v <= 0:
        raise FunnelError("%s must be above 0" % key)
    if not positive and v < 0:
        raise FunnelError("%s must not be negative" % key)
    return float(v)


def money(v, currency):
    if v is None:
        return "n/a"
    cur = (currency or "USD").upper()
    if cur == "USD":
        return "$%s" % format(v, ",.2f")
    if cur == "VND":
        return "%s\u20ab" % format(int(round(v)), ",")
    return "%s %s" % (cur, format(v, ",.2f"))


def analyse(spec):
    if not isinstance(spec, dict):
        raise FunnelError("input must be a JSON object")
    target = _num(spec, "target_customers_per_month")
    deal = _num(spec, "deal_value")
    contrib = _num(spec, "contribution_per_customer_month")
    months = _num(spec, "expected_customer_months")
    cycle = _num(spec, "cycle_days", positive=False)
    days = _num(spec, "selling_days_per_month", required=False, default=21.0)
    touches = _num(spec, "touches_per_day", required=False)
    spend = _num(spec, "ad_or_tool_spend_month", required=False, positive=False)

    stages = spec.get("stages")
    if not isinstance(stages, list) or not stages:
        raise FunnelError("stages must be a non-empty list")
    convs = []
    for i, s in enumerate(stages):
        if not isinstance(s, dict) or not s.get("name"):
            raise FunnelError("stage %d needs a name" % (i + 1))
        c = s.get("conversion")
        if isinstance(c, bool) or not isinstance(c, (int, float)):
            raise FunnelError("stage '%s' needs a numeric conversion" % s["name"])
        if c <= 0 or c > 1:
            raise FunnelError(
                "stage '%s' conversion must be above 0 and at most 1, got %s"
                % (s["name"], c))
        convs.append(float(c))

    # needed[i] = how many must ENTER stage i per month; last entry = signed customers.
    needed = [0.0] * (len(stages) + 1)
    needed[-1] = target
    for i in range(len(stages) - 1, -1, -1):
        needed[i] = needed[i + 1] / convs[i]
    rows = [{"stage": stages[i]["name"], "conversion": convs[i], "needed_per_month": needed[i]}
            for i in range(len(stages))]

    first = needed[0]
    per_day = first / days
    overall = target / first
    flags = []
    capacity = None
    if touches is not None:
        capacity = touches * days
        if capacity < first:
            short = first - capacity
            flags.append("Not enough capacity: %.1f first contacts a month are needed but "
                         "%.1f fit (%.1f a day for %g selling days). Shortfall: %.1f a month."
                         % (first, capacity, touches, days, short))
    lifetime = contrib * months
    cac = ltv_cac = payback = None
    if spend is not None:
        cac = spend / target
        if cac > 0:
            ltv_cac = lifetime / cac
            payback = cac / contrib
            if ltv_cac < 3:
                flags.append("LTV:CAC is %.2f, under 3. Each customer may not repay "
                             "what it costs to win." % ltv_cac)
            if payback > 12:
                flags.append("Payback is %.1f months, over 12. Cash is tied up for "
                             "more than a year per customer." % payback)
        else:
            payback = 0.0
    else:
        flags.append("No ad_or_tool_spend_month given, so CAC, LTV:CAC and payback are "
                     "not computed. Your own time is not counted either way.")
    return {
        "business": spec.get("business", ""),
        "currency": spec.get("currency", "USD"),
        "target_customers_per_month": target,
        "deal_value": deal,
        "stages": rows,
        "first_contacts_per_month": first,
        "first_contacts_per_selling_day": per_day,
        "selling_days_per_month": days,
        "touches_per_day": touches,
        "capacity_per_month": capacity,
        "overall_conversion": overall,
        "cycle_days": cycle,
        "monthly_revenue_from_new": target * deal,
        "lifetime_contribution": lifetime,
        "cac": cac,
        "ltv_cac": ltv_cac,
        "payback_months": payback,
        "flags": flags,
    }


def report(res):
    cur = res["currency"]
    L = ["# Sales funnel: %s" % (res["business"] or "your business"), ""]
    L.append("Target: %g new customers a month, first month worth %s each. "
             "These are projections from your own conversion guesses, not results."
             % (res["target_customers_per_month"], money(res["deal_value"], cur)))
    L += ["", "| Stage | Moves on | Needed per month |", "|---|---|---|"]
    for r in res["stages"]:
        L.append("| %s | %.0f%% | %.1f |" % (r["stage"], r["conversion"] * 100, r["needed_per_month"]))
    L.append("| Signed | | %.1f |" % res["target_customers_per_month"])
    L += ["", "- First contacts needed: %.1f a month, %.1f per selling day (%g selling days)."
          % (res["first_contacts_per_month"], res["first_contacts_per_selling_day"],
             res["selling_days_per_month"]),
          "- Overall conversion, first contact to signed: %.2f%%." % (res["overall_conversion"] * 100),
          "- Sales cycle: %g days from first touch to signed, so a contact made today "
          "pays in about that long." % res["cycle_days"]]
    if res["capacity_per_month"] is not None:
        L.append("- Capacity: %.1f first contacts a month at %g a day."
                 % (res["capacity_per_month"], res["touches_per_day"]))
    L.append("- New monthly revenue at target: %s."
             % money(res["monthly_revenue_from_new"], cur))
    L.append("- Lifetime contribution per customer: %s." % money(res["lifetime_contribution"], cur))
    L.append("- CAC: %s." % money(res["cac"], cur))
    L.append("- LTV to CAC: %s." % ("n/a" if res["ltv_cac"] is None else "%.2f" % res["ltv_cac"]))
    L.append("- Payback: %s." % ("n/a" if res["payback_months"] is None
                                  else "%.1f months" % res["payback_months"]))
    L += ["", "## Flags", ""]
    L += ["- " + f for f in res["flags"]] or ["- None."]
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("spec", help="funnel JSON file")
    ap.add_argument("--out", help="write a markdown report here")
    ap.add_argument("--json", action="store_true", help="print the result as JSON")
    a = ap.parse_args(argv)
    try:
        try:
            with open(a.spec, encoding="utf-8") as fh:
                spec = json.load(fh)
        except (OSError, ValueError) as e:
            raise FunnelError("cannot read %s: %s" % (a.spec, e))
        res = analyse(spec)
    except FunnelError as e:
        print("error: %s" % e, file=sys.stderr)
        return 2
    text = report(res)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            fh.write(text)
    if a.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    elif not a.out:
        print(text, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
