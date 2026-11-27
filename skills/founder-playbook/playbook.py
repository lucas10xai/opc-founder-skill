#!/usr/bin/env python3
"""The framework library for founder-playbook. Standard library only, no network.

The library is a folder of markdown files, one per business framework from a
well-known founder, investor or thinker, each written in our own words with a small
header (stage, who it fits, which pack skills use it). This tool finds the right
ones for a situation and checks that every file is well formed.

    python3 playbook.py list [--stage validate] [--fits online] [--skill founder-cfo]
    python3 playbook.py suggest --stage validate --fits consumer [--skill founder-launch] [--top 6]
    python3 playbook.py show lean-startup
    python3 playbook.py check

The header of a framework file:

    slug     the file name without .md
    name     the framework's name
    source   Author, Title (year)
    people   [who it comes from]
    stage    [idea, validate, price, launch, operate, grow]
    fits     [consumer, business, online, service, physical, any]
    feeds    [the pack skills that use it]

`suggest` scores a framework 2 points for each of: matching the stage, being listed
for the skill; and 1 point for fitting the kind of business (a framework marked
`any` counts half a point). It needs at least one of --stage, --fits, --skill.
`check` exits 1 if any file is malformed, so it can sit in a test.
"""

import argparse
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DIR = os.path.join(HERE, "frameworks")
SKILLS_DIR = os.path.dirname(HERE)
STAGES = ["idea", "validate", "price", "launch", "operate", "grow"]
FITS = ["consumer", "business", "online", "service", "physical", "any"]
KEYS = ["slug", "name", "source", "people", "stage", "fits", "feeds"]
LISTS = {"people", "stage", "fits", "feeds"}
SECTIONS = ["The idea", "When to use it", "Questions to put to the founder", "Red flags",
            "How the pack uses it", "Limits", "Sources"]
MIN_WORDS, MAX_WORDS = 250, 900
DASHES = (chr(0x2014), chr(0x2013))


class PlaybookError(Exception):
    pass


def _pack_skills():
    return sorted(d for d in os.listdir(SKILLS_DIR) if os.path.isfile(os.path.join(SKILLS_DIR, d, "SKILL.md")))


def parse(path):
    """Return (header dict, body text). Raises PlaybookError if there is no header."""
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        raise PlaybookError("%s: no header between --- lines" % os.path.basename(path))
    head = {}
    for line in m.group(1).splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise PlaybookError("%s: header line without a colon: %r" % (os.path.basename(path), line))
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        if key in LISTS:
            if not (value.startswith("[") and value.endswith("]")):
                raise PlaybookError("%s: %s must look like [a, b]" % (os.path.basename(path), key))
            head[key] = [x.strip() for x in value[1:-1].split(",") if x.strip()]
        else:
            head[key] = value
    return head, m.group(2)


def load_all(directory=DEFAULT_DIR):
    found = []
    for path in sorted(glob.glob(os.path.join(directory, "*.md"))):
        head, body = parse(path)
        head.update(path=path, body=body, words=len(body.split()))
        found.append(head)
    return found


def problems(fw, pack_skills=None):
    """Every way one framework file breaks the format. Empty list means it is fine."""
    pack_skills = pack_skills if pack_skills is not None else _pack_skills()
    name = os.path.basename(fw["path"])
    out = []
    for k in KEYS:
        if not fw.get(k):
            out.append("%s: header is missing %s" % (name, k))
    if fw.get("slug") and fw["slug"] + ".md" != name:
        out.append("%s: slug %r does not match the file name" % (name, fw["slug"]))
    for key, allowed in (("stage", STAGES), ("fits", FITS), ("feeds", pack_skills)):
        for v in fw.get(key, []):
            if v not in allowed:
                out.append("%s: %s has %r, which is not one of: %s" % (name, key, v, ", ".join(allowed)))
    for section in SECTIONS:
        if not re.search(r"^## %s\s*$" % re.escape(section), fw["body"], re.M):
            out.append("%s: missing the section '## %s'" % (name, section))
    if not fw["body"].lstrip().startswith("# "):
        out.append("%s: the body must start with a '# ' title" % name)
    if not MIN_WORDS <= fw["words"] <= MAX_WORDS:
        out.append("%s: %d words, expected %d to %d" % (name, fw["words"], MIN_WORDS, MAX_WORDS))
    for d in DASHES:
        with open(fw["path"], encoding="utf-8") as fh:
            if d in fh.read():
                out.append("%s: contains a long dash (U+%04X); use a comma, colon or hyphen" % (name, ord(d)))
    return out


def check(directory=DEFAULT_DIR):
    fws = load_all(directory)
    if not fws:
        raise PlaybookError("no framework files in %s" % directory)
    skills = _pack_skills()
    seen, out = {}, []
    for fw in fws:
        out += problems(fw, skills)
        if fw.get("slug") in seen:
            out.append("duplicate slug %s" % fw["slug"])
        seen[fw.get("slug")] = True
    return out


def select(fws, stage=None, fits=None, skill=None):
    """Frameworks that match every filter given."""
    out = []
    for fw in fws:
        if stage and stage not in fw["stage"]:
            continue
        if fits and fits not in fw["fits"] and "any" not in fw["fits"]:
            continue
        if skill and skill not in fw["feeds"]:
            continue
        out.append(fw)
    return out


def suggest(fws, stage=None, fits=None, skill=None, top=6):
    """Ranked best matches (score, framework). Needs at least one criterion."""
    if not (stage or fits or skill):
        raise PlaybookError("give at least one of --stage, --fits, --skill")
    for label, value, allowed in (("stage", stage, STAGES), ("fits", fits, FITS)):
        if value and value not in allowed:
            raise PlaybookError("--%s must be one of: %s" % (label, ", ".join(allowed)))
    scored = []
    for fw in fws:
        score = 0.0
        if stage and stage in fw["stage"]:
            score += 2
        if skill and skill in fw["feeds"]:
            score += 2
        if fits:
            if fits in fw["fits"]:
                score += 1
            elif "any" in fw["fits"]:
                score += 0.5
        if score > 0:
            scored.append((score, fw))
    scored.sort(key=lambda t: (-t[0], t[1]["slug"]))
    return scored[:top]


def find(fws, slug):
    for fw in fws:
        if fw["slug"] == slug:
            return fw
    raise PlaybookError("no framework called %r (try: playbook.py list)" % slug)


def _row(fw):
    return "%-32s %s  [%s]" % (fw["slug"], fw["name"], fw["source"])


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--dir", default=DEFAULT_DIR, help="the frameworks folder")
    sub = ap.add_subparsers(dest="cmd", required=True)
    ls = sub.add_parser("list")
    sg = sub.add_parser("suggest")
    for p in (ls, sg):
        p.add_argument("--stage")
        p.add_argument("--fits")
        p.add_argument("--skill")
    sg.add_argument("--top", type=int, default=6)
    sh = sub.add_parser("show")
    sh.add_argument("slug")
    sub.add_parser("check")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "check":
            probs = check(a.dir)
            for p in probs:
                print(p)
            print("%d frameworks, %d problems" % (len(load_all(a.dir)), len(probs)))
            return 1 if probs else 0
        fws = load_all(a.dir)
        if a.cmd == "show":
            with open(find(fws, a.slug)["path"], encoding="utf-8") as fh:
                sys.stdout.write(fh.read())
        elif a.cmd == "list":
            for fw in select(fws, a.stage, a.fits, a.skill):
                print(_row(fw))
        else:
            for score, fw in suggest(fws, a.stage, a.fits, a.skill, a.top):
                print("%4.1f  %s" % (score, _row(fw)))
    except (PlaybookError, FileNotFoundError) as e:
        print("error: %s" % e, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
