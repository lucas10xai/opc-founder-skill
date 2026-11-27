#!/usr/bin/env python3
"""Where the founder pack stands, for founder-run. Standard library only, no network.

Looks in the founder/ folder, says which skills have already written their file,
which one comes next, and which are optional. It never runs a skill and never
writes anything except market.json when you ask for it.

    python3 status.py                       # reads ./founder
    python3 status.py --dir path/to/founder
    python3 status.py --json
    python3 status.py market --country VN   # writes founder/market.json (VND, Vietnamese)
    python3 status.py market --country CA --currency CAD --language English

The order is the order of the pack: board, competitors, consumer, pricing, offer,
cfo, compliance, marketing, brand, ops, launch, plan. Four are never blocking:
interview (real people take days; start them and carry on), sales (businesses that
sell to businesses), metrics (after launch) and pitch (only when raising money).
"""

import argparse
import json
import os
import sys

# (skill, file it writes in founder/, kind, one line on what it is for)
STEPS = [
    ("founder-board", "board.md", "core", "the idea in front of the board"),
    ("founder-competitors", "competitors.md", "core", "who else sells this, at what price"),
    ("founder-consumer", os.path.join("panel", "results.json"), "core", "100 simulated buyers"),
    ("founder-interview", os.path.join("interviews", "results.json"), "parallel", "5 to 10 real people, to check the panel"),
    ("founder-pricing", "pricing.md", "core", "the price range and what to test"),
    ("founder-offer", "offer.md", "core", "the offer that answers the objections"),
    ("founder-cfo", "cfo.md", "core", "the real margins and the cash needed"),
    ("founder-compliance", "compliance.md", "core", "licences, tax and permits to confirm"),
    ("founder-marketing", "marketing.md", "core", "positioning and a 30-day campaign"),
    ("founder-sales", "sales.md", "optional", "for businesses that sell to businesses"),
    ("founder-brand", "brand.md", "core", "name, voice and look"),
    ("founder-ops", "ops.md", "core", "how it runs on day one"),
    ("founder-launch", "launch.md", "core", "the test, the countdown, the first 30 days"),
    ("founder-plan", "business-plan.md", "core", "everything in one plan, with a computed verdict"),
    ("founder-metrics", "metrics.md", "optional", "after launch: plan against reality"),
    ("founder-pitch", "pitch-deck.md", "optional", "only if raising money or asking a lender"),
    ("founder-playbook", "playbook.md", "optional", "any time: what top founders have published, applied to your numbers"),
]
MARKETS = {"VN": ("VND", "Vietnamese")}


class StatusError(Exception):
    pass


def _has(d, rel):
    path = os.path.join(d, rel)
    return os.path.isfile(path) and os.path.getsize(path) > 0


def read_market(d):
    path = os.path.join(d, "market.json")
    if not os.path.isfile(path):
        return None
    try:
        with open(path, encoding="utf-8") as fh:
            m = json.load(fh)
    except ValueError as e:
        raise StatusError("%s is not valid JSON: %s" % (path, e))
    if not isinstance(m, dict) or not {"country", "currency", "language"} <= set(m):
        raise StatusError("%s needs country, currency and language" % path)
    return m


def status(d):
    steps = [{"skill": s, "file": f, "kind": k, "about": a, "done": _has(d, f)} for s, f, k, a in STEPS]
    nxt = next((s["skill"] for s in steps if s["kind"] == "core" and not s["done"]), None)
    return {"dir": d, "idea": _has(d, "idea.md"), "numbers": _has(d, "numbers.json"),
            "market": read_market(d), "steps": steps, "next": nxt,
            "finished": nxt is None and bool(steps)}


def render(st):
    L = []
    m = st["market"]
    L.append("Market: %s" % ("%s, %s, %s" % (m["country"], m["currency"], m["language"]) if m
                            else "not set (run: status.py market --country XX)"))
    L.append("Idea: %s" % ("founder/idea.md" if st["idea"] else "not written yet (founder-board writes it)"))
    L.append("")
    for s in st["steps"]:
        if s["done"]:
            mark = "done "
        elif s["skill"] == st["next"]:
            mark = "NEXT "
        else:
            mark = "     "
        tag = "" if s["kind"] == "core" else "  (%s)" % s["kind"]
        L.append("%s /%s: %s%s" % (mark, s["skill"], s["about"], tag))
    L.append("")
    if st["next"]:
        L.append("Next: /%s" % st["next"])
    else:
        L.append("All core steps are done. Run /founder-plan again to refresh the plan, then /founder-metrics once you have real sales.")
    return "\n".join(L) + "\n"


def write_market(d, country, currency=None, language=None):
    country = country.strip().upper()
    if len(country) != 2 or not country.isalpha():
        raise StatusError("--country is a two letter code like VN, CA or GB")
    preset = MARKETS.get(country, (None, None))
    currency = (currency or preset[0] or "").strip().upper()
    language = (language or preset[1] or "").strip()
    if len(currency) != 3 or not currency.isalpha():
        raise StatusError("give --currency as a three letter code like VND or USD")
    if not language:
        raise StatusError("give --language, for example English")
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, "market.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({"country": country, "currency": currency, "language": language}, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    return path


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--dir", default="founder")
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    mk = sub.add_parser("market", help="write founder/market.json")
    mk.add_argument("--country", required=True)
    mk.add_argument("--currency")
    mk.add_argument("--language")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "market":
            print("wrote %s" % write_market(a.dir, a.country, a.currency, a.language))
            return 0
        st = status(a.dir)
    except StatusError as e:
        print("error: %s" % e, file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps(st, indent=1, ensure_ascii=False))
    else:
        sys.stdout.write(render(st))
    return 0


if __name__ == "__main__":
    sys.exit(main())
