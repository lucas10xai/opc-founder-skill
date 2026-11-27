#!/usr/bin/env python3
"""Compiles the business plan for founder-plan. Standard library only, no network.

Reads everything the other ten skills wrote into founder/ and assembles one
document, founder/business-plan.md, with a verdict at the top. The verdict is
computed from the numbers, never written by hand:

    Profitable   every check that has data passes
    Not yet      at least one check fails (each failure is listed with its number)
    Incomplete   there are no numbers yet (run founder-cfo first)

The checks:
    1. each unit earns money before fixed costs        (founder/numbers.json)
    2. year 1 makes an operating profit                 (founder/numbers.json)
    3. break-even fits inside capacity, if capacity is given
    4. enough of the buyer panel buys                   (founder/panel/results.json, --min-buy-rate, default 25%)
    5. enough REAL people paid or pre-ordered, once 5 or more were interviewed
                                                        (founder/interviews/results.json, --min-real-rate, default 10%)

    python3 compile.py                      # reads ./founder, writes ./founder/business-plan.md
    python3 compile.py --dir path/to/founder --min-buy-rate 0.3
    python3 compile.py --check              # print the verdict and exit 0 (Profitable) or 1
    python3 compile.py --html               # also write founder/business-plan.html (open it, print to PDF)
    python3 compile.py --vault ~/Vault/Plans   # also write a note with frontmatter for Obsidian or Notion import
"""

import argparse
import datetime
import html
import importlib.util
import json
import math
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
SECTIONS = [  # (file in founder/, heading, which skill writes it, optional)
    ("summary.md", "Summary", "founder-plan", False),
    ("board.md", "What the board said", "founder-board", False),
    ("competitors.md", "The competition", "founder-competitors", False),
    ("panel/results.md", "The buyer panel", "founder-consumer", False),
    ("interviews/results.md", "Real customers", "founder-interview", False),
    ("pricing.md", "Pricing", "founder-pricing", False),
    ("offer.md", "The offer", "founder-offer", False),
    ("cfo.md", "The numbers", "founder-cfo", False),
    ("compliance.md", "Compliance", "founder-compliance", False),
    ("marketing.md", "Marketing", "founder-marketing", False),
    ("sales.md", "Sales", "founder-sales", True),
    ("brand.md", "Brand", "founder-brand", False),
    ("ops.md", "Operations", "founder-ops", False),
    ("launch.md", "Launch plan", "founder-launch", False),
    ("metrics.md", "How it is going", "founder-metrics", True),
    ("playbook.md", "What the frameworks say", "founder-playbook", True),
]
_UE = None


def _load_unit_economics():
    global _UE
    if _UE is None:
        path = os.path.join(HERE, "..", "founder-cfo", "unit_economics.py")
        spec = importlib.util.spec_from_file_location("founder_unit_economics", path)
        _UE = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_UE)
    return _UE


def _read(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read().strip()
    except FileNotFoundError:
        return None


def _strip_h1(text):
    lines = text.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    # demote headings one level so they nest under the section heading
    return "\n".join(("#" + l) if l.startswith("#") else l for l in lines).strip()


def _interviews(d):
    raw = _read(os.path.join(d, "interviews", "results.json"))
    return json.loads(raw) if raw else None


def verdict(d, min_buy_rate=0.25, min_real_rate=0.10):
    """Return (verdict, checks, numbers, panel). checks = [(ok, text)]."""
    checks = []
    numbers = panel = None
    raw = _read(os.path.join(d, "numbers.json"))
    if raw:
        ue = _load_unit_economics()
        numbers = ue.analyse(json.loads(raw))
        u, cur = numbers["unit"], numbers["currency"]
        per = numbers["period"]
        c = numbers["contribution"]
        checks.append((c > 0, "Each %s earns %s before fixed costs (%.0f%% contribution)." % (u, ue.money(c, cur), numbers["contribution_pct"] * 100)
                       if c > 0 else "Each %s LOSES %s before fixed costs." % (u, ue.money(-c, cur))))
        y = numbers["year1_profit"]
        checks.append((y > 0, "Year 1 operating profit: %s." % ue.whole(y, cur) if y > 0
                       else "Year 1 operating LOSS: %s." % ue.whole(-y, cur)))
        be, cap = numbers["breakeven_per_day"], numbers["capacity_per_day"]
        if cap is not None:
            fits = not math.isinf(be) and be <= float(cap)
            checks.append((fits, "Break-even is %s %s a %s against a capacity of %s." % (
                "never reached" if math.isinf(be) else "{:,.0f}".format(math.ceil(be)), numbers["unit_plural"], per, cap)))
    raw = _read(os.path.join(d, "panel", "results.json"))
    if raw:
        panel = json.loads(raw)
        r = panel["buy_rate"]
        checks.append((r >= min_buy_rate, "%d of %d simulated buyers buy (%.0f%%, the bar is %.0f%%)." % (
            panel["buys"], panel["answered"], r * 100, min_buy_rate * 100)))
    real = _interviews(d)
    if real and real.get("enough"):
        checks.append((real["commit_rate"] >= min_real_rate, "%d of %d real people paid or pre-ordered (%.0f%%, the bar is %.0f%%)." % (
            real["committed"], real["n"], real["commit_rate"] * 100, min_real_rate * 100)))
    if numbers is None:
        v = "Incomplete"
    elif all(ok for ok, _ in checks):
        v = "Profitable"
    else:
        v = "Not yet"
    return v, checks, numbers, panel


def _slug(text):
    s = unicodedata.normalize("NFKD", text.replace("đ", "d").replace("Đ", "D"))
    s = "".join(ch for ch in s if not unicodedata.combining(ch)).lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-") or "business"


def _inline(text):
    t = html.escape(text, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+|mailto:[^)\s]+)\)", r'<a href="\2">\1</a>', t)
    return re.sub(r"(?<![\w])_([^_]+)_(?![\w])", r"<em>\1</em>", t)


def to_html(md, title):
    """A small markdown to HTML converter for the plan: headings, tables, lists, code, bold, links."""
    out, para, i = [], [], 0
    lines = md.splitlines()

    def flush():
        if para:
            out.append("<p>%s</p>" % _inline(" ".join(para)))
            para.clear()

    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            flush()
            code = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(lines[i])
                i += 1
            out.append("<pre><code>%s</code></pre>" % html.escape("\n".join(code), quote=False))
        elif re.match(r"#{1,6} ", line):
            flush()
            n = len(line) - len(line.lstrip("#"))
            out.append("<h%d>%s</h%d>" % (n, _inline(line[n:].strip()), n))
        elif line.lstrip().startswith("|"):
            flush()
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            i -= 1
            if rows:
                head, body = rows[0], rows[1:]
                out.append("<table><thead><tr>%s</tr></thead><tbody>%s</tbody></table>" % (
                    "".join("<th>%s</th>" % _inline(c) for c in head),
                    "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % _inline(c) for c in r) for r in body)))
        elif re.match(r"\s*([-*]|\d+\.) ", line):
            flush()
            tag = "ol" if re.match(r"\s*\d+\. ", line) else "ul"
            items = []
            while i < len(lines) and re.match(r"\s*([-*]|\d+\.) ", lines[i]):
                items.append(re.sub(r"^\s*([-*]|\d+\.) ", "", lines[i]))
                i += 1
            i -= 1
            out.append("<%s>%s</%s>" % (tag, "".join("<li>%s</li>" % _inline(x) for x in items), tag))
        elif not line.strip():
            flush()
        else:
            para.append(line.strip())
        i += 1
    flush()
    css = ("body{font:16px/1.5 system-ui,sans-serif;max-width:820px;margin:2rem auto;padding:0 1rem;color:#111}"
           "table{border-collapse:collapse;margin:1rem 0}td,th{border:1px solid #ccc;padding:.3rem .6rem;text-align:left}"
           "th{background:#f3f3f3}pre{background:#f6f6f6;padding:.8rem;overflow:auto}h2{margin-top:2rem;border-bottom:1px solid #ddd}"
           "@media print{body{margin:0;max-width:none}h2{page-break-after:avoid}table{page-break-inside:avoid}}")
    return ("<!doctype html>\n<html><head><meta charset=\"utf-8\"><title>%s</title><style>%s</style></head>\n<body>\n%s\n</body></html>\n"
            % (html.escape(title), css, "\n".join(out)))


def vault_note(text, title, v, today=None):
    """The plan with frontmatter, ready for an Obsidian vault or a Notion markdown import."""
    today = today or datetime.date.today().isoformat()
    front = ["---", "title: \"%s\"" % title.replace("\"", "'"), "verdict: %s" % v, "generated: %s" % today,
             "source: opc-founder-skill", "tags: [business-plan, founder]", "---", "", ""]
    return "\n".join(front) + text


def _title(d, numbers):
    idea = _read(os.path.join(d, "idea.md"))
    if idea:
        first = idea.splitlines()[0]
        if first.startswith("# "):
            return first[2:].strip()
    return numbers["business"] if numbers and numbers.get("business") else "Your business"


def compile_plan(d, min_buy_rate=0.25, min_real_rate=0.10):
    idea = _read(os.path.join(d, "idea.md"))
    v, checks, numbers, panel = verdict(d, min_buy_rate, min_real_rate)
    real = _interviews(d)
    title = _title(d, numbers)
    L = ["# %s · Business plan" % title, ""]
    L.append("**Verdict: %s**" % v)
    L.append("")
    for ok, text in checks:
        L.append("- %s %s" % ("✓" if ok else "✗", text))
    if v == "Incomplete":
        L.append("- No numbers yet. Run /founder-cfo, then compile again.")
    L.append("")
    if numbers:
        ue = _load_unit_economics()
        cur, per, u = numbers["currency"], numbers["period"], numbers["unit"]
        be = numbers["breakeven_per_day"]
        L += ["| key number | |", "| --- | ---: |",
              "| Price | %s a %s |" % (ue.money(numbers["price"], cur), u),
              "| Profit margin at plan | %.0f%% per %s |" % (numbers["margin_at_plan"] * 100, u),
              "| Break-even | %s %s a %s |" % ("never" if math.isinf(be) else "{:,.0f}".format(math.ceil(be)), numbers["unit_plural"], per),
              "| Year 1 operating profit | %s |" % ue.whole(numbers["year1_profit"], cur),
              "| Startup spend | %s |" % ue.whole(numbers["startup"], cur),
              "| Cash needed before it pays for itself | %s |" % ue.whole(numbers["cash_needed"], cur),
              "| Startup money earned back | %s |" % ("month %d" % numbers["payback_month"] if numbers["payback_month"] else "not in year 1")]
        if panel:
            L.append("| Buyer panel | %d buy · %d pass |" % (panel["buys"], panel["passes"]))
        if real:
            L.append("| Real people | %d paid or pre-ordered of %d%s |" % (
                real["committed"], real["n"], "" if real.get("enough") else " (too few to count: need 5)"))
        L.append("")
    if idea:
        L += ["## The idea", "", _strip_h1(idea), ""]
    missing = []
    for fname, heading, skill, optional in SECTIONS:
        text = _read(os.path.join(d, fname))
        if text:
            L += ["## %s" % heading, "", _strip_h1(text), ""]
        elif not optional:
            missing.append((heading, skill))
    if missing:
        L += ["## Not done yet", ""]
        for heading, skill in missing:
            L.append("- %s: run /%s" % (heading, skill))
        L.append("")
    L.append("_The panel is simulated buyers and the numbers are projections from your inputs. Confirm demand with real"
             " customers and costs with real quotes before you spend. Not financial, legal or tax advice._")
    return v, "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--dir", default="founder")
    ap.add_argument("--min-buy-rate", type=float, default=0.25)
    ap.add_argument("--min-real-rate", type=float, default=0.10)
    ap.add_argument("--check", action="store_true", help="print the verdict only; exit 0 if Profitable")
    ap.add_argument("--out", help="default: <dir>/business-plan.md")
    ap.add_argument("--html", nargs="?", const="", metavar="PATH", help="also write an HTML copy (default: <dir>/business-plan.html)")
    ap.add_argument("--vault", metavar="DIR", help="also write the plan with frontmatter into this folder (an Obsidian vault)")
    a = ap.parse_args(argv)
    if not os.path.isdir(a.dir):
        print("error: no %s/ folder here. Run the other founder skills first." % a.dir, file=sys.stderr)
        return 2
    try:
        v, text = compile_plan(a.dir, a.min_buy_rate, a.min_real_rate)
        if a.check:
            _, checks, _, _ = verdict(a.dir, a.min_buy_rate, a.min_real_rate)
            print("Verdict: %s" % v)
            for ok, t in checks:
                print("  %s %s" % ("✓" if ok else "✗", t))
            return 0 if v == "Profitable" else 1
    except (ValueError, KeyError, _load_unit_economics().NumbersError) as e:
        print("error: %s" % e, file=sys.stderr)
        return 2
    out = a.out or os.path.join(a.dir, "business-plan.md")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(text)
    print("Verdict: %s. Wrote %s" % (v, out))
    title = _title(a.dir, verdict(a.dir, a.min_buy_rate, a.min_real_rate)[2])
    if a.html is not None:
        path = a.html or os.path.join(a.dir, "business-plan.html")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(to_html(text, "%s · Business plan" % title))
        print("Wrote %s (open it in a browser and print to PDF)" % path)
    if a.vault:
        os.makedirs(a.vault, exist_ok=True)
        slug = _slug(title)
        path = os.path.join(a.vault, "%s-business-plan.md" % slug)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(vault_note(text, "%s · Business plan" % title, v))
        print("Wrote %s" % path)
        one = _read(os.path.join(a.dir, "one-pager.md"))
        if one:
            path = os.path.join(a.vault, "%s-one-pager.md" % slug)
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(vault_note(one + "\n", "%s · One-pager" % title, v))
            print("Wrote %s" % path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
