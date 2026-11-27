import json
import os
import shutil
import tempfile
import unittest

from _load import load, example

mt = load("founder-metrics", "metrics")


def spec(**change):
    with open(example("founder-cfo", "example.json"), encoding="utf-8") as fh:
        s = json.load(fh)
    s.update(change)
    return s


def row(month, units, **kw):
    r = {c: None for c in mt.COLUMNS}
    r.update(month=month, units=units)
    r.update(kw)
    return r


class Call(unittest.TestCase):
    # the example plan: 140 cups a day in month 1 (4,200 a month), 170 in month 2 (5,100), $6.50, $1.74 a cup

    def test_on_plan_is_on_track(self):
        a = mt.analyse_actuals(spec(), [row(1, 4200), row(2, 5100)])
        self.assertEqual(a["status"], "on track")
        self.assertEqual(a["reasons"], [])
        self.assertAlmostEqual(a["rows"][0]["profit"], a["rows"][0]["profit_plan"])

    def test_a_first_week_is_compared_with_a_week_of_plan(self):
        a = mt.analyse_actuals(spec(), [row(1, 980, days=7)])
        self.assertEqual(a["status"], "on track")
        self.assertAlmostEqual(a["rows"][0]["units_vs_plan"], 1.0)

    def test_weak_sales_in_one_month_means_change_something(self):
        a = mt.analyse_actuals(spec(), [row(1, 2400)])
        self.assertEqual(a["status"], "change something")
        self.assertIn("57% of plan", a["reasons"][0])

    def test_two_months_under_the_red_bar_means_stop(self):
        a = mt.analyse_actuals(spec(), [row(1, 2000), row(2, 2000)])
        self.assertEqual(a["status"], "stop and rethink")

    def test_a_unit_that_loses_money_means_stop_even_with_full_sales(self):
        a = mt.analyse_actuals(spec(), [row(1, 4200, revenue=4200 * 1.5)])
        self.assertEqual(a["status"], "stop and rethink")
        self.assertIn("loses money", a["reasons"][0])

    def test_unit_profit_well_under_plan_is_named(self):
        a = mt.analyse_actuals(spec(), [row(1, 4200, revenue=4200 * 6.5, variable_cost=4200 * 2.5)])
        self.assertEqual(a["status"], "change something")
        self.assertIn("Profit per cup", a["reasons"][0])

    def test_customers_costing_more_than_the_cap_are_named(self):
        a = mt.analyse_actuals(spec(max_cac=5), [row(1, 4200, ad_spend=1000, new_customers=100)])
        self.assertEqual(a["status"], "change something")
        self.assertAlmostEqual(a["cac"], 10)
        self.assertIn("A customer costs", a["reasons"][0])

    def test_missing_columns_fall_back_to_the_plan_and_say_so(self):
        a = mt.analyse_actuals(spec(), [row(1, 4200)])
        self.assertEqual(set(a["rows"][0]["assumed"]), {"revenue", "variable_cost", "fixed_cost"})
        self.assertIn("Not given, so the plan's figure was used", mt.report(a))


class Reforecast(unittest.TestCase):
    def test_weak_sales_pull_year_one_down_and_real_months_stay_real(self):
        a = mt.analyse_actuals(spec(), [row(1, 2100), row(2, 2550)])
        self.assertLess(a["reforecast"]["year1_profit"], a["plan"]["year1_profit"])
        self.assertAlmostEqual(a["reforecast"]["months"][0]["per_day"], 70)
        self.assertAlmostEqual(a["sales_vs_plan"], 0.5)
        self.assertAlmostEqual(a["reforecast"]["months"][11]["per_day"], 0.5 * a["plan"]["months"][11]["per_day"])

    def test_real_price_and_cost_replace_the_plan_when_every_row_has_them(self):
        a = mt.analyse_actuals(spec(), [row(1, 4000, revenue=4000 * 6.0, variable_cost=4000 * 2.0)])
        self.assertAlmostEqual(a["reforecast"]["price"], 6.0)
        self.assertAlmostEqual(a["reforecast"]["variable_per_unit"], 2.0)


class Reading(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.d)

    def csv(self, text):
        path = os.path.join(self.d, "actuals.csv")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        return path

    def test_reads_rows_and_blank_cells(self):
        rows = mt.read_actuals(self.csv("month,units,days,revenue\n2,5000,,32,500\n".replace("32,500", "32500")))
        self.assertEqual(rows[0]["month"], 2)
        self.assertIsNone(rows[0]["days"])
        self.assertEqual(rows[0]["revenue"], 32500)

    def test_refuses_duplicates_bad_months_and_missing_columns(self):
        for text in ("month,units\n1,10\n1,20\n", "month,units\n13,10\n", "month,units\n1.5,10\n",
                     "month,revenue\n1,10\n", "month,units\n1,-4\n", "month,units\n1,lots\n", "month,units\n"):
            with self.assertRaises(mt.MetricsError, msg=text):
                mt.read_actuals(self.csv(text))

    def test_the_example_file_runs_end_to_end(self):
        numbers = os.path.join(self.d, "numbers.json")
        with open(numbers, "w", encoding="utf-8") as fh:
            json.dump(spec(), fh)
        out = os.path.join(self.d, "metrics.md")
        self.assertEqual(mt.main([numbers, example("founder-metrics", "actuals.example.csv"), "--out", out]), 0)
        with open(out, encoding="utf-8") as fh:
            text = fh.read()
        self.assertIn("**Status:", text)
        self.assertIn("## Year 1 now", text)

    def test_vnd_report_has_no_dollars(self):
        with open(example("founder-cfo", "example.vn.json"), encoding="utf-8") as fh:
            s = json.load(fh)
        text = mt.report(mt.analyse_actuals(s, [row(1, 2100)]))
        self.assertIn("₫", text)
        self.assertNotIn("$", text)


if __name__ == "__main__":
    unittest.main()
