import os
import re
import shutil
import tempfile
import unittest

from _load import load, SKILLS_DIR

pb = load("founder-playbook", "playbook")

GOOD = """---
slug: demo
name: Demo framework
source: A. Person, A Book (2001)
people: [A. Person]
stage: [validate]
fits: [any]
feeds: [founder-cfo]
---
# Demo framework

## The idea
%s

## When to use it
- x

## Questions to put to the founder
- x

## Red flags
- x

## How the pack uses it
x

## Limits
- x

## Sources
A. Person, A Book (2001)
"""
FILLER = " ".join(["word"] * 300)


def write(d, name, text):
    with open(os.path.join(d, name), "w", encoding="utf-8") as fh:
        fh.write(text)


class Library(unittest.TestCase):
    def test_every_framework_file_is_well_formed(self):
        self.assertEqual(pb.check(), [])

    def test_the_library_has_the_frameworks_the_board_and_skills_name(self):
        slugs = {f["slug"] for f in pb.load_all()}
        for needed in ("lean-startup", "five-forces", "jobs-to-be-done", "mom-test", "inversion", "profit-first"):
            self.assertIn(needed, slugs)

    def test_suggest_ranks_stage_and_skill_matches_above_the_rest(self):
        fws = pb.load_all()
        ranked = pb.suggest(fws, stage="validate", skill="founder-interview", top=50)
        scores = [s for s, _ in ranked]
        self.assertEqual(scores, sorted(scores, reverse=True))
        top_score, top = ranked[0]
        self.assertGreaterEqual(top_score, 4)   # matches both the stage and the skill
        self.assertIn("validate", top["stage"])
        self.assertIn("founder-interview", top["feeds"])

    def test_a_framework_marked_any_still_fits_a_kind_of_business(self):
        fws = pb.load_all()
        anyfit = [f for f in fws if "any" in f["fits"]]
        self.assertTrue(anyfit)
        listed = {f["slug"] for f in pb.select(fws, fits="physical")}
        self.assertTrue({f["slug"] for f in anyfit} <= listed)

    def test_bad_requests_are_refused(self):
        fws = pb.load_all()
        with self.assertRaises(pb.PlaybookError):
            pb.suggest(fws)
        with self.assertRaises(pb.PlaybookError):
            pb.suggest(fws, stage="someday")
        with self.assertRaises(pb.PlaybookError):
            pb.find(fws, "no-such-framework")


class Checker(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.d)

    def problems(self, text, name="demo.md"):
        write(self.d, name, text)
        return pb.problems(pb.load_all(self.d)[0])

    def test_a_good_file_passes(self):
        self.assertEqual(self.problems(GOOD % FILLER), [])

    def test_each_kind_of_mistake_is_named(self):
        cases = [
            (GOOD.replace("stage: [validate]", "stage: [someday]") % FILLER, "stage"),
            (GOOD.replace("feeds: [founder-cfo]", "feeds: [founder-nothing]") % FILLER, "feeds"),
            (GOOD.replace("## Limits", "## Caveats") % FILLER, "missing the section '## Limits'"),
            (GOOD % "too short", "words, expected"),
            ((GOOD % FILLER).replace("x\n\n## Limits", "a" + chr(0x2014) + "b\n\n## Limits"), "long dash"),
            ((GOOD % FILLER).replace("source: A. Person, A Book (2001)\n", ""), "missing source"),
        ]
        for text, expect in cases:
            found = " | ".join(self.problems(text))
            self.assertIn(expect, found, expect)

    def test_slug_must_match_the_file_name(self):
        self.assertTrue(any("does not match" in p for p in self.problems(GOOD % FILLER, name="other.md")))

    def test_a_header_that_is_not_a_list_is_refused(self):
        with self.assertRaises(pb.PlaybookError):
            self.problems((GOOD % FILLER).replace("stage: [validate]", "stage: validate"))


class PointersAreReal(unittest.TestCase):
    def test_each_skills_framework_list_matches_the_library(self):
        fws = pb.load_all()
        for skill in sorted(os.listdir(SKILLS_DIR)):
            path = os.path.join(SKILLS_DIR, skill, "SKILL.md")
            if not os.path.isfile(path) or skill == "founder-playbook":
                continue
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
            m = re.search(r"^## Frameworks that apply\s*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
            listed = set(re.findall(r"^- `([a-z0-9-]+)`", m.group(1), re.M)) if m else set()
            expected = {f["slug"] for f in fws if skill in f["feeds"]}
            self.assertEqual(listed, expected, skill)

    def test_the_boards_guest_lenses_depend_on_real_files(self):
        slugs = {f["slug"] for f in pb.load_all()}
        with open(os.path.join(SKILLS_DIR, "founder-board", "lenses.md"), encoding="utf-8") as fh:
            lenses = fh.read()
        depth = re.findall(r"^Depth: (.*)$", lenses, re.M)
        self.assertEqual(len(depth), 5)
        named = set()
        for line in depth:
            for slug in re.findall(r"`([a-z0-9-]+)`", line):
                self.assertIn(slug, slugs)
                named.add(slug)
        # the library says "the board uses this" for exactly the files the guest lenses name
        self.assertEqual(named, {f["slug"] for f in pb.load_all() if "founder-board" in f["feeds"]})


if __name__ == "__main__":
    unittest.main()
