import json
import os
import tempfile
import unittest

from _load import load, example

iv = load("founder-interview", "interview")


def make(rows, panel=None):
    root = tempfile.mkdtemp()
    d = os.path.join(root, "interviews")
    for i, (c, src, price, obj) in enumerate(rows, 1):
        iv.add(d, {"id": "I%02d" % i, "commitment": c, "source": src,
                   "price_said": price, "objection": obj})
    if panel is not None:
        os.makedirs(os.path.join(root, "panel"))
        with open(os.path.join(root, "panel", "results.json"), "w") as fh:
            json.dump({"buy_rate": panel}, fh)
    return d


def tally(d):
    recs = iv.check(d)["records"]
    return iv.tally(recs, iv._panel_rate(d))


ROWS = [("paid", "stranger", 6, "Too far"), ("preorder", "customer", 7, "too far"),
        ("waitlist", "stranger", None, ""), ("none", "stranger", 5, "too  expensive"),
        ("interest", "colleague", 6, "Too far"), ("preorder", "friend", 9, ""),
        ("paid", "friend", 9, "")]


class Interview(unittest.TestCase):
    def test_friends_are_excluded_from_every_rate(self):
        res = tally(make(ROWS))
        self.assertEqual(res["n"], 5)
        self.assertEqual(res["excluded_friends"], 2)
        self.assertEqual(sum(res["by_commitment"].values()), 5)
        self.assertEqual(res["by_commitment"]["preorder"], 1)

    def test_commit_rate_and_soft_rate(self):
        res = tally(make(ROWS))
        self.assertEqual(res["committed"], 2)
        self.assertAlmostEqual(res["commit_rate"], 0.4)
        self.assertAlmostEqual(res["soft_rate"], 0.6)

    def test_price_median_and_objections_are_normalised(self):
        res = tally(make(ROWS))
        self.assertEqual(res["price_said_median"], 6)
        self.assertEqual(res["top_objections"][0], ["too far", 3])

    def test_bad_records_and_duplicates_are_refused(self):
        d = make([("paid", "stranger", 6, "")])
        for bad in ({"id": "I02", "commitment": "maybe"},
                    {"id": "I02", "commitment": "paid", "source": "cousin"},
                    {"id": "I02", "commitment": "paid", "price_said": "cheap"},
                    {"id": "I01", "commitment": "paid"}):
            with self.assertRaises(iv.InterviewError):
                iv.add(d, bad)
        self.assertEqual(len(os.listdir(d)), 1)

    def test_add_command_refuses_with_exit_2(self):
        d = tempfile.mkdtemp()
        self.assertEqual(iv.main(["add", "--dir", d, "--id", "I01",
                                  "--commitment", "yes please"]), 2)
        self.assertEqual(iv.main(["add", "--dir", d, "--id", "I01",
                                  "--commitment", "paid", "--price-said", "6.5"]), 0)
        self.assertEqual(iv.main(["add", "--dir", d, "--id", "I01",
                                  "--commitment", "none"]), 2)

    def test_enough_is_false_under_five(self):
        res = tally(make(ROWS[:3]))
        self.assertFalse(res["enough"])
        self.assertIn("too few", res["verdict_line"])
        self.assertIn("2 more", res["verdict_line"])
        self.assertTrue(tally(make(ROWS))["enough"])

    def test_gap_against_the_panel(self):
        res = tally(make(ROWS, panel=0.7))
        self.assertAlmostEqual(res["panel_buy_rate"], 0.7)
        self.assertAlmostEqual(res["gap"], 0.3)
        self.assertIn("/founder-offer", res["verdict_line"])
        none = tally(make(ROWS))
        self.assertIsNone(none["panel_buy_rate"])
        self.assertIsNone(none["gap"])

    def test_tally_writes_files_with_the_key_numbers(self):
        d = make(ROWS, panel=0.7)
        self.assertEqual(iv.main(["tally", "--dir", d]), 0)
        md = open(os.path.join(d, "results.md")).read()
        data = json.load(open(os.path.join(d, "results.json")))
        self.assertEqual(data["n"], 5)
        for needle in ("40%", "70%", "too far", "friend", "Limits"):
            self.assertIn(needle, md)

    def test_tally_with_nothing_countable_writes_nothing(self):
        d = make([("paid", "friend", 5, "")])
        self.assertEqual(iv.main(["tally", "--dir", d]), 2)
        self.assertFalse(os.path.exists(os.path.join(d, "results.md")))
        self.assertFalse(os.path.exists(os.path.join(d, "results.json")))

    def test_broken_file_is_reported_by_check(self):
        d = make([("paid", "stranger", 6, "")])
        with open(os.path.join(d, "I09.json"), "w") as fh:
            json.dump({"id": "I09", "commitment": "maybe"}, fh)
        got = iv.check(d)
        self.assertEqual(len(got["records"]), 1)
        self.assertEqual(len(got["problems"]), 1)
        self.assertEqual(iv.main(["check", "--dir", d]), 2)

    def test_shipped_examples_are_valid(self):
        d = example("founder-interview", "interview.example")
        got = iv.check(d)
        self.assertEqual(got["problems"], [])
        self.assertEqual([r["id"] for r in got["records"]], ["I01", "I02", "I03"])


if __name__ == "__main__":
    unittest.main()
