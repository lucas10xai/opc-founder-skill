#!/usr/bin/env python3
"""Customer-interview records and tally for founder-interview. Standard library only.

    interview.py template
    interview.py add --id I04 --commitment preorder [--source stranger] [--segment S]
                     [--price-said 6.5] [--objection TEXT] [--reason TEXT]
                     [--quote TEXT] [--date YYYY-MM-DD] [--dir founder/interviews]
    interview.py check [--dir founder/interviews]
    interview.py tally [--dir founder/interviews] [--out founder/interviews/results.md]

One JSON file per interview (I01.json, I02.json ...). Friends are listed but never
counted: they say yes to be kind. Nothing is guessed: a bad record is refused.
"""

import argparse
import datetime
import glob
import json
import os
import sys

COMMITMENTS = ("none", "interest", "waitlist", "preorder", "paid")
SOURCES = ("stranger", "customer", "friend", "colleague")
ENOUGH = 5
FIELDS = ("id", "commitment", "source", "date", "segment", "price_said",
          "objection", "reason", "quote")


class InterviewError(Exception):
    pass


def blank():
    return {"id": "I01", "commitment": "none", "source": "stranger", "date": None,
            "segment": "", "price_said": None, "objection": "", "reason": "",
            "quote": ""}


def clean(rec, stem=None):
    """Validate one record and return a normalised copy. Raise InterviewError."""
    if not isinstance(rec, dict):
        raise InterviewError("record is not a JSON object")
    rid = rec.get("id")
    if not isinstance(rid, str) or not rid.strip():
        raise InterviewError("missing id")
    rid = rid.strip()
    if stem is not None and rid != stem:
        raise InterviewError("id %r does not match file name %r" % (rid, stem))
    c = rec.get("commitment")
    if c not in COMMITMENTS:
        raise InterviewError("%s: commitment must be one of %s, got %r"
                             % (rid, ", ".join(COMMITMENTS), c))
    src = rec.get("source", "stranger")
    if src not in SOURCES:
        raise InterviewError("%s: source must be one of %s, got %r"
                             % (rid, ", ".join(SOURCES), src))
    price = rec.get("price_said")
    if price is not None:
        if isinstance(price, bool):
            raise InterviewError("%s: price_said is not a number" % rid)
        try:
            price = float(price)
        except (TypeError, ValueError):
            raise InterviewError("%s: price_said is not a number: %r" % (rid, price))
        if price != price or price in (float("inf"), float("-inf")) or price < 0:
            raise InterviewError("%s: price_said must be a number, 0 or more" % rid)
    date = rec.get("date")
    if date is not None:
        try:
            datetime.datetime.strptime(str(date), "%Y-%m-%d")
        except ValueError:
            raise InterviewError("%s: date must be YYYY-MM-DD, got %r" % (rid, date))
        date = str(date)
    out = {"id": rid, "commitment": c, "source": src, "date": date,
           "segment": str(rec.get("segment") or "").strip(),
           "price_said": price,
           "objection": str(rec.get("objection") or "").strip(),
           "reason": str(rec.get("reason") or "").strip(),
           "quote": str(rec.get("quote") or "").strip()}
    return out


def _files(d):
    return sorted(p for p in glob.glob(os.path.join(d, "I*.json")))


def check(d):
    """Return {'records': [...], 'problems': [...]} for every I*.json in d."""
    records, problems, seen = [], [], {}
    for p in _files(d):
        stem = os.path.splitext(os.path.basename(p))[0]
        try:
            with open(p, encoding="utf-8") as fh:
                raw = json.load(fh)
        except (OSError, ValueError) as e:
            problems.append("%s: cannot read (%s)" % (os.path.basename(p), e))
            continue
        try:
            rec = clean(raw, stem)
        except InterviewError as e:
            problems.append("%s: %s" % (os.path.basename(p), e))
            continue
        if rec["id"].lower() in seen:
            problems.append("%s: duplicate id %s" % (os.path.basename(p), rec["id"]))
            continue
        seen[rec["id"].lower()] = p
        records.append(rec)
    return {"records": records, "problems": problems}


def add(d, rec):
    """Write one new record; refuse duplicates and bad values. Return the record."""
    rec = clean(rec)
    for p in _files(d):
        stem = os.path.splitext(os.path.basename(p))[0]
        if stem.lower() == rec["id"].lower():
            raise InterviewError("duplicate id %s (%s exists)" % (rec["id"], p))
    if os.sep in rec["id"] or "/" in rec["id"] or not rec["id"].startswith("I"):
        raise InterviewError("id must start with I and contain no slash, e.g. I04")
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, rec["id"] + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(rec, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return rec


def _median(xs):
    xs = sorted(xs)
    m = len(xs) // 2
    return xs[m] if len(xs) % 2 else (xs[m - 1] + xs[m]) / 2.0


def _panel_rate(d):
    path = os.path.join(d, "..", "panel", "results.json")
    try:
        with open(path, encoding="utf-8") as fh:
            v = json.load(fh).get("buy_rate")
    except (OSError, ValueError, AttributeError):
        return None
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not 0 <= v <= 1:
        return None
    return float(v)


def tally(records, panel_buy_rate=None):
    friends = [r for r in records if r["source"] == "friend"]
    counted = [r for r in records if r["source"] != "friend"]
    n = len(counted)
    if n == 0:
        raise InterviewError("no countable interviews (friends are excluded); "
                             "add records with source stranger, customer or colleague")
    by = dict((k, 0) for k in COMMITMENTS)
    for r in counted:
        by[r["commitment"]] += 1
    committed = by["preorder"] + by["paid"]
    commit_rate = committed / float(n)
    soft_rate = (committed + by["waitlist"]) / float(n)
    prices = [r["price_said"] for r in counted if r["price_said"] is not None]
    objs = {}
    for r in counted:
        k = " ".join(r["objection"].lower().split())
        if k:
            objs[k] = objs.get(k, 0) + 1
    top = sorted(objs.items(), key=lambda kv: (-kv[1], kv[0]))
    gap = None if panel_buy_rate is None else panel_buy_rate - commit_rate
    enough = n >= ENOUGH
    if not enough:
        verdict = ("Only %d real interview%s counted, too few to trust: do %d more "
                   "before you decide anything." % (n, "" if n == 1 else "s", ENOUGH - n))
    elif gap is None:
        verdict = ("%d of %d real people committed with money (%.0f%%); there is no "
                   "panel result to compare with." % (committed, n, commit_rate * 100))
    elif gap > 0.15:
        verdict = ("Real people fall well short of the panel (%.0f%% against %.0f%%): "
                   "trust the real buyers and go back to /founder-offer or "
                   "/founder-pricing." % (commit_rate * 100, panel_buy_rate * 100))
    elif gap < -0.15:
        verdict = ("Real people commit more than the panel predicted (%.0f%% against "
                   "%.0f%%): good sign, but keep the sample growing." %
                   (commit_rate * 100, panel_buy_rate * 100))
    else:
        verdict = ("Real commitment (%.0f%%) is close to the panel (%.0f%%): the panel "
                   "held up on this sample; keep testing with more people." %
                   (commit_rate * 100, panel_buy_rate * 100))
    return {"n": n, "excluded_friends": len(friends), "by_commitment": by,
            "committed": committed, "commit_rate": commit_rate, "soft_rate": soft_rate,
            "price_said_median": _median(prices) if prices else None,
            "top_objections": [[k, v] for k, v in top],
            "panel_buy_rate": panel_buy_rate, "gap": gap, "enough": enough,
            "verdict_line": verdict}


def _pct(v):
    return "n/a" if v is None else "%.0f%%" % (v * 100)


def _num(v):
    return ("%.2f" % v).rstrip("0").rstrip(".")


def report(res, records):
    L = ["# Real interviews: results", "", res["verdict_line"], ""]
    L += ["Counted interviews: **%d**. Friends listed but excluded: **%d**."
          % (res["n"], res["excluded_friends"]), ""]
    L += ["## By commitment", "", "| commitment | people |", "| --- | --- |"]
    for k in COMMITMENTS:
        L.append("| %s | %d |" % (k, res["by_commitment"][k]))
    L += ["", "Commitment with money (preorder or paid): **%d of %d = %s**. "
          "Including waitlist: %s." % (res["committed"], res["n"],
                                       _pct(res["commit_rate"]), _pct(res["soft_rate"])), ""]
    L += ["## Objections that repeated", ""]
    rep = [o for o in res["top_objections"] if o[1] > 1]
    if rep:
        L += ["- %s (%d)" % (t, c) for t, c in rep]
    elif res["top_objections"]:
        L.append("Nothing repeated yet. Each objection was said once:")
        L += ["- %s" % t for t, _ in res["top_objections"]]
    else:
        L.append("No objections recorded.")
    L += ["", "## Price said", ""]
    if res["price_said_median"] is None:
        L.append("No price was recorded.")
    else:
        L.append("Median price people said they would pay: **%s**."
                 % _num(res["price_said_median"]))
    L += ["", "## Panel against real people", ""]
    if res["panel_buy_rate"] is None:
        L.append("No `founder/panel/results.json` found, so there is nothing to compare.")
    else:
        L += ["| | buy rate |", "| --- | --- |",
              "| simulated panel | %s |" % _pct(res["panel_buy_rate"]),
              "| real people (money committed) | %s |" % _pct(res["commit_rate"]),
              "| gap (panel minus real) | %.0f points |" % (res["gap"] * 100)]
    L += ["", "## Every record", "", "| id | source | commitment | price said | counted |",
          "| --- | --- | --- | --- | --- |"]
    for r in records:
        L.append("| %s | %s | %s | %s | %s |" % (
            r["id"], r["source"], r["commitment"],
            "" if r["price_said"] is None else _num(r["price_said"]),
            "no (friend)" if r["source"] == "friend" else "yes"))
    L += ["", "## Limits", "",
          "- A small sample. Under %d people is noise, and even %d is a hint." % (ENOUGH, ENOUGH * 2),
          "- It shows only the people you could reach, not the whole market.",
          "- Commitment with money counts. A waitlist is a soft yes, and a smile or "
          "\"sounds great\" does not count at all.",
          "- Friends and family are excluded because they say yes to be kind.",
          "- These are projections to guide the next step, not advice.", ""]
    return "\n".join(L)


def _load_all(d):
    if not os.path.isdir(d):
        raise InterviewError("folder not found: %s" % d)
    got = check(d)
    if got["problems"]:
        raise InterviewError("fix these records first:\n  " + "\n  ".join(got["problems"]))
    return got["records"]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("template")
    a = sub.add_parser("add")
    a.add_argument("--id", required=True)
    a.add_argument("--commitment", required=True)
    a.add_argument("--source", default="stranger")
    a.add_argument("--segment")
    a.add_argument("--price-said")
    a.add_argument("--objection")
    a.add_argument("--reason")
    a.add_argument("--quote")
    a.add_argument("--date")
    for name in ("add", "check", "tally"):
        p = a if name == "add" else sub.add_parser(name)
        p.add_argument("--dir", default="founder/interviews")
    t = sub.choices["tally"]
    t.add_argument("--out")
    try:
        args = ap.parse_args(argv)
    except SystemExit as e:
        return 0 if e.code in (0, None) else 2
    try:
        if args.cmd == "template":
            print(json.dumps(blank(), indent=2))
        elif args.cmd == "add":
            rec = {"id": args.id, "commitment": args.commitment, "source": args.source,
                   "date": args.date, "segment": args.segment,
                   "price_said": args.price_said, "objection": args.objection,
                   "reason": args.reason, "quote": args.quote}
            r = add(args.dir, rec)
            print("added %s (%s, %s)" % (r["id"], r["commitment"], r["source"]))
        elif args.cmd == "check":
            got = check(args.dir)
            for p in got["problems"]:
                print("problem: " + p)
            print("%d valid record(s), %d problem(s)"
                  % (len(got["records"]), len(got["problems"])))
            return 2 if got["problems"] else 0
        elif args.cmd == "tally":
            recs = _load_all(args.dir)
            res = tally(recs, _panel_rate(args.dir))
            out = args.out or os.path.join(args.dir, "results.md")
            md = report(res, recs)
            with open(out, "w", encoding="utf-8") as fh:
                fh.write(md)
            with open(os.path.join(args.dir, "results.json"), "w", encoding="utf-8") as fh:
                json.dump(res, fh, indent=2)
                fh.write("\n")
            print(res["verdict_line"])
            print("wrote %s" % out)
        else:
            ap.print_usage(sys.stderr)
            return 2
    except InterviewError as e:
        print("error: %s" % e, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
