import json
import math
import os
import shutil
import tempfile
import unittest

from _load import load, example

ue = load("founder-cfo", "unit_economics")
panel = load("founder-consumer", "panel")
vw = load("founder-pricing", "van_westendorp")


def vn_numbers():
    with open(example("founder-cfo", "example.vn.json"), encoding="utf-8") as fh:
        return json.load(fh)


def vn_customer():
    with open(example("founder-consumer", "customer.example.vn.json"), encoding="utf-8") as fh:
        return json.load(fh)


class Money(unittest.TestCase):
    def test_vnd_example_reproduces_by_hand(self):
        a = ue.analyse(vn_numbers())
        self.assertEqual(a["currency"], "VND")
        self.assertEqual(a["contribution"], 32300)
        self.assertEqual(math.ceil(a["breakeven_per_day"]), 88)
        self.assertEqual(round(a["margin_at_plan"] * 100), 33)
        self.assertEqual(round(a["year1_profit"]), 786216000)
        self.assertEqual(a["payback_month"], 7)
        self.assertEqual(a["flags"], [])

    def test_report_shows_vnd_without_decimals_and_no_dollars(self):
        s = vn_numbers()
        text = ue.report(s, ue.analyse(s))
        for needle in ("32,300₫", "88 ly a day", "786,216,000₫", "month 7"):
            self.assertIn(needle, text)
        self.assertNotIn("$", text)
        self.assertNotIn("lys", text)

    def test_money_formats(self):
        self.assertEqual(ue.money(6.5), "$6.50")
        self.assertEqual(ue.money(-4.76), "-$4.76")
        self.assertEqual(ue.money(45000, "VND"), "45,000₫")
        self.assertEqual(ue.whole(1234.6, "EUR"), "€1,235")
        self.assertEqual(ue.money(10, "THB"), "THB 10.00")


class PerMonth(unittest.TestCase):
    def agency(self):
        return {"business": "Agency", "unit": "client-month", "price": 1000,
                "variable": [{"label": "tools", "cost": 200}], "fixed_monthly": [{"label": "salary", "cost": 3000}],
                "startup": [{"label": "setup", "cost": 2000}], "volume_period": "month", "plan_per_day": 10}

    def test_month_volume_means_units_a_month(self):
        a = ue.analyse(self.agency())
        self.assertEqual(math.ceil(a["breakeven_per_day"]), 4)   # 3000 / 800 clients a month
        self.assertEqual(round(a["margin_at_plan"] * 100), 50)
        self.assertEqual(round(a["year1_profit"]), 12 * (10 * 800 - 3000))
        self.assertIn("4 client-months a month", ue.report(self.agency(), a))

    def test_bad_period_is_refused(self):
        s = self.agency()
        s["volume_period"] = "week"
        with self.assertRaises(ue.NumbersError):
            ue.analyse(s)


class Sensitivity(unittest.TestCase):
    def test_breakeven_price_is_where_year_one_stops_losing(self):
        s = vn_numbers()
        a = ue.analyse(s)
        at = ue.analyse(s, price=a["breakeven_price"])
        self.assertLess(abs(at["year1_profit"]), 1)
        self.assertLess(a["breakeven_price"], a["price"])

    def test_grid_centre_is_the_plan(self):
        s = vn_numbers()
        g = ue.grid(s)
        centre = next(r for r in g["rows"] if r["price_step"] == 0)
        self.assertAlmostEqual(centre["profit"][g["volume_steps"].index(1.0)], ue.analyse(s)["year1_profit"], places=2)
        self.assertGreater(centre["profit"][-1], centre["profit"][0])   # more volume, more profit


class VietnamesePanel(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.d)

    def brief(self, customer, n=20):
        path = os.path.join(self.d, "customer.json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(customer, fh, ensure_ascii=False)
        panel.init(self.d, path, example("founder-consumer", "pitch.example.vn.md"), n=n, seed=3)
        waves = panel.write_briefs(self.d)
        with open(waves[0][0][1], encoding="utf-8") as fh:
            return fh.read()

    def test_names_come_from_the_profile(self):
        cards = panel.deal(vn_customer(), 20, 3)
        names = set(vn_customer()["names"])
        self.assertTrue(all(c["name"] in names for c in cards))
        self.assertEqual(len({c["name"] for c in cards}), 20)

    def test_more_buyers_than_names_still_unique(self):
        cards = panel.deal(vn_customer(), 100, 3)
        self.assertEqual(len({c["name"] for c in cards}), 100)

    def test_brief_speaks_vnd_per_month_and_asks_for_vietnamese(self):
        brief = self.brief(vn_customer())
        self.assertRegex(brief, r"You earn about [\d,]+₫ a month\.")
        self.assertIn("Write the free-text answers in Vietnamese", brief)
        self.assertIn("a number in VND", brief)
        self.assertNotIn("$", brief)

    def test_a_business_buyer_gets_the_profile_sentence_not_a_salary(self):
        c = vn_customer()
        c.update({"kind": "business", "income_period": "year",
                  "income_line": "Your team spends about {amount} a year on tools like this."})
        brief = self.brief(c)
        self.assertRegex(brief, r"Your team spends about [\d,]+₫ a year on tools like this\.")
        self.assertNotIn("You earn about", brief)

    def test_bad_profile_options_are_refused(self):
        for change in ({"kind": "government"}, {"income_period": "week"}, {"names": [1, 2]}):
            c = vn_customer()
            c.update(change)
            with self.assertRaises(panel.PanelError):
                panel.deal(c, 5, 1)


class VietnamesePrices(unittest.TestCase):
    def test_price_answers_read_the_way_they_are_written_in_vietnam(self):
        for raw in ("45000", "45,000", "45.000", "45k", "45000đ", "45.000₫", " 45 000 VND "):
            self.assertEqual(vw._f(raw), 45000, raw)
        self.assertEqual(vw._f("$6.50"), 6.5)
        self.assertEqual(vw._f("6.5"), 6.5)
        self.assertIsNone(vw._f("free"))

    def test_report_uses_the_panel_currency(self):
        rows = [(30000 + i * 1000, 40000 + i * 1000, 55000 + i * 1000, 70000 + i * 1000) for i in range(10)]
        text = vw.report(vw.analyse(rows), 0, price=55000, currency="VND")
        self.assertIn("₫", text)
        self.assertNotIn("$", text)

    def test_currency_is_read_from_the_panel_next_to_the_answers(self):
        d = tempfile.mkdtemp()
        try:
            os.makedirs(os.path.join(d, "answers"))
            with open(os.path.join(d, "panel.json"), "w", encoding="utf-8") as fh:
                json.dump({"customer": {"currency": "vnd"}}, fh)
            self.assertEqual(vw._currency_of(os.path.join(d, "answers")), "VND")
            self.assertEqual(vw._currency_of(os.path.join(d, "nowhere", "answers")), "USD")
        finally:
            shutil.rmtree(d)


if __name__ == "__main__":
    unittest.main()
