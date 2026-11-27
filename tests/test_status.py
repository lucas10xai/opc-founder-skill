import json
import os
import shutil
import tempfile
import unittest

from _load import load

st = load("founder-run", "status")


class Status(unittest.TestCase):
    def setUp(self):
        self.d = os.path.join(tempfile.mkdtemp(), "founder")

    def tearDown(self):
        shutil.rmtree(os.path.dirname(self.d))

    def touch(self, *rels):
        for rel in rels:
            path = os.path.join(self.d, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as fh:
                fh.write("x\n")

    def test_a_missing_folder_starts_at_the_board(self):
        s = st.status(self.d)
        self.assertEqual(s["next"], "founder-board")
        self.assertFalse(s["finished"])

    def test_next_is_the_first_core_step_not_done(self):
        self.touch("board.md", "competitors.md")
        self.assertEqual(st.status(self.d)["next"], "founder-consumer")

    def test_interviews_never_block_the_pack(self):
        self.touch("board.md", "competitors.md", os.path.join("panel", "results.json"))
        s = st.status(self.d)
        self.assertEqual(s["next"], "founder-pricing")
        self.assertFalse(next(x for x in s["steps"] if x["skill"] == "founder-interview")["done"])

    def test_finished_when_every_core_step_is_done(self):
        core = [f for _, f, kind, _ in st.STEPS if kind == "core"]
        self.touch(*core)
        s = st.status(self.d)
        self.assertIsNone(s["next"])
        self.assertTrue(s["finished"])
        self.assertIn("All core steps are done", st.render(s))

    def test_an_empty_file_does_not_count(self):
        os.makedirs(self.d)
        open(os.path.join(self.d, "board.md"), "w").close()
        self.assertEqual(st.status(self.d)["next"], "founder-board")

    def test_market_vn_fills_in_dong_and_vietnamese(self):
        st.write_market(self.d, "vn")
        with open(os.path.join(self.d, "market.json"), encoding="utf-8") as fh:
            self.assertEqual(json.load(fh), {"country": "VN", "currency": "VND", "language": "Vietnamese"})
        self.assertEqual(st.read_market(self.d)["currency"], "VND")

    def test_market_needs_the_missing_pieces_for_other_countries(self):
        with self.assertRaises(st.StatusError):
            st.write_market(self.d, "CA")
        with self.assertRaises(st.StatusError):
            st.write_market(self.d, "Canada", "CAD", "English")
        st.write_market(self.d, "CA", "cad", "English")
        self.assertEqual(st.read_market(self.d)["currency"], "CAD")

    def test_a_broken_market_file_is_reported(self):
        self.touch("market.json")
        with self.assertRaises(st.StatusError):
            st.read_market(self.d)


if __name__ == "__main__":
    unittest.main()
