import json
import os
import tempfile
import unittest

from _load import load, example

fn = load("founder-sales", "funnel")


def spec(**kw):
    s = {
        "business": "Test",
        "currency": "USD",
        "target_customers_per_month": 4,
        "deal_value": 500,
        "contribution_per_customer_month": 100,
        "expected_customer_months": 12,
        "stages": [{"name": "Reply", "conversion": 0.5},
                   {"name": "Call", "conversion": 0.25}],
        "cycle_days": 30,
    }
    s.update(kw)
    return s


class Funnel(unittest.TestCase):
    def test_backwards_maths(self):
        res = fn.analyse(spec())
        self.assertAlmostEqual(res["first_contacts_per_month"], 32)
        self.assertAlmostEqual([r["needed_per_month"] for r in res["stages"]][1], 16)
        self.assertAlmostEqual(res["first_contacts_per_selling_day"], 32 / 21.0)
        self.assertAlmostEqual(res["overall_conversion"], 0.125)

    def test_touches_shortfall_is_flagged(self):
        res = fn.analyse(spec(touches_per_day=1, selling_days_per_month=20))
        self.assertTrue(any("Shortfall: 12.0" in f for f in res["flags"]))
        ok = fn.analyse(spec(touches_per_day=2, selling_days_per_month=20))
        self.assertFalse(any("capacity" in f for f in ok["flags"]))

    def test_bad_conversions_are_refused(self):
        for bad in (0, 1.2):
            s = spec(stages=[{"name": "Reply", "conversion": bad}])
            with self.assertRaises(fn.FunnelError):
                fn.analyse(s)

    def test_cli_refusal_exit_code(self):
        d = tempfile.mkdtemp()
        p = os.path.join(d, "f.json")
        with open(p, "w") as fh:
            json.dump(spec(stages=[{"name": "x", "conversion": 0}]), fh)
        self.assertEqual(fn.main([p]), 2)

    def test_ltv_cac_and_payback(self):
        res = fn.analyse(spec(ad_or_tool_spend_month=800))
        self.assertAlmostEqual(res["cac"], 200)
        self.assertAlmostEqual(res["lifetime_contribution"], 1200)
        self.assertAlmostEqual(res["ltv_cac"], 6.0)
        self.assertAlmostEqual(res["payback_months"], 2.0)
        self.assertEqual(res["flags"], [])

    def test_weak_economics_flagged(self):
        res = fn.analyse(spec(ad_or_tool_spend_month=8000))
        self.assertAlmostEqual(res["ltv_cac"], 0.6)
        self.assertTrue(any("under 3" in f for f in res["flags"]))
        self.assertTrue(any("over 12" in f for f in res["flags"]))

    def test_no_spend_means_no_cac(self):
        res = fn.analyse(spec())
        self.assertIsNone(res["cac"])
        self.assertIsNone(res["ltv_cac"])

    def test_vnd_formatting_in_report(self):
        res = fn.analyse(spec(currency="VND", deal_value=12500000,
                              ad_or_tool_spend_month=8000000))
        text = fn.report(res)
        self.assertIn("12,500,000\u20ab", text)
        self.assertIn("2,000,000\u20ab", text)

    def test_other_currency_prefix_and_usd(self):
        self.assertEqual(fn.money(1234.5, "EUR"), "EUR 1,234.50")
        self.assertEqual(fn.money(1234.5, "USD"), "$1,234.50")

    def test_example_file_runs(self):
        d = tempfile.mkdtemp()
        out = os.path.join(d, "r.md")
        self.assertEqual(fn.main([example("founder-sales", "funnel.example.json"),
                                  "--out", out]), 0)
        with open(out, encoding="utf-8") as fh:
            self.assertIn("## Flags", fh.read())


if __name__ == "__main__":
    unittest.main()
