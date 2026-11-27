import json
import os
import shutil
import tempfile
import unittest

from _load import load, example

plan = load("founder-plan", "compile")


class Extras(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.d)

    def write(self, rel, obj):
        path = os.path.join(self.d, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(obj if isinstance(obj, str) else json.dumps(obj, ensure_ascii=False))

    def numbers(self, name="example.json"):
        with open(example("founder-cfo", name), encoding="utf-8") as fh:
            self.write("numbers.json", fh.read())

    def panel(self, buys=40):
        self.write("panel/results.json", {"buys": buys, "passes": 100 - buys, "answered": 100, "buy_rate": buys / 100.0})

    def interviews(self, n, committed):
        self.write("interviews/results.json", {"n": n, "committed": committed, "commit_rate": committed / float(n),
                                               "enough": n >= 5})

    def test_a_vnd_plan_is_in_dong_with_the_right_plural(self):
        self.numbers("example.vn.json")
        self.panel()
        v, text = plan.compile_plan(self.d)
        self.assertEqual(v, "Profitable")
        self.assertIn("| Price | 55,000₫ a ly |", text)
        self.assertIn("| Break-even | 88 ly a day |", text)
        self.assertNotIn("$", text)

    def test_real_people_who_do_not_pay_fail_the_plan(self):
        self.numbers()
        self.panel()
        self.interviews(8, 0)
        v, text = plan.compile_plan(self.d)
        self.assertEqual(v, "Not yet")
        self.assertIn("✗ 0 of 8 real people paid or pre-ordered", text)

    def test_real_people_who_pay_pass_and_are_shown(self):
        self.numbers()
        self.panel()
        self.interviews(8, 2)
        v, text = plan.compile_plan(self.d)
        self.assertEqual(v, "Profitable")
        self.assertIn("| Real people | 2 paid or pre-ordered of 8 |", text)

    def test_too_few_interviews_are_shown_but_not_judged(self):
        self.numbers()
        self.panel()
        self.interviews(3, 0)
        v, text = plan.compile_plan(self.d)
        self.assertEqual(v, "Profitable")
        self.assertIn("too few to count", text)

    def test_optional_sections_are_not_listed_as_missing(self):
        self.numbers()
        _, text = plan.compile_plan(self.d)
        self.assertNotIn("run /founder-sales", text)
        self.assertNotIn("run /founder-metrics", text)
        self.assertIn("run /founder-interview", text)

    def test_html_escapes_and_keeps_tables(self):
        md = "# T\n\n| a | b |\n| --- | --- |\n| 1 | <script>x</script> |\n\n- one\n- **two**\n\n[bad](javascript:alert(1)) [ok](https://example.com)\n"
        page = plan.to_html(md, "T")
        self.assertIn("<table>", page)
        self.assertIn("&lt;script&gt;", page)
        self.assertNotIn("<script>", page)
        self.assertIn("<li><strong>two</strong></li>", page)
        self.assertNotIn('<a href="javascript', page)
        self.assertIn('<a href="https://example.com">ok</a>', page)

    def test_vault_note_has_frontmatter_and_a_plain_filename(self):
        note = plan.vault_note("body\n", 'Quán "A"', "Profitable", today="2026-01-02")
        self.assertTrue(note.startswith("---\ntitle: \"Quán 'A'\"\nverdict: Profitable\ngenerated: 2026-01-02\n"))
        self.assertTrue(note.endswith("---\n\nbody\n"))
        self.assertEqual(plan._slug("Quán Matcha Đà Nẵng"), "quan-matcha-da-nang")

    def test_main_writes_html_and_vault_files(self):
        self.write("idea.md", "# Quán Matcha Sài Gòn\n\nMột quán nhỏ.\n")
        self.write("one-pager.md", "# One page\n\nShort.\n")
        self.numbers("example.vn.json")
        vault = os.path.join(self.d, "vault")
        self.assertEqual(plan.main(["--dir", self.d, "--html", "--vault", vault]), 0)
        self.assertTrue(os.path.exists(os.path.join(self.d, "business-plan.html")))
        self.assertTrue(os.path.exists(os.path.join(vault, "quan-matcha-sai-gon-business-plan.md")))
        self.assertTrue(os.path.exists(os.path.join(vault, "quan-matcha-sai-gon-one-pager.md")))


if __name__ == "__main__":
    unittest.main()
