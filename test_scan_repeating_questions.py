"""Regression checks for repeat matching, extraction, and offline report safety."""
import json
from pathlib import Path
import tempfile
import unittest

import pymupdf
import scan_repeating_questions as scanner


def question(stem, choices=None, paper="2007S_AM", review=None, year=2007):
    return {"stem": stem, "choices": choices or ["alpha", "beta", "gamma", "delta"],
            "paper_id": paper, "review_reasons": review or [], "year": year}


class MatchingTests(unittest.TestCase):
    def test_formatting_and_choice_order(self):
        a = question("Which protocol provides reliable\n delivery of network packets?")
        b = question("Which protocol provides reliable delivery of network packets?", list(reversed(a["choices"])), "2007A_AM")
        self.assertEqual(scanner.question_key(a), scanner.question_key(b))
        self.assertEqual([r["kind"] for r in scanner.match_questions([a, b])], ["exact"])

    def test_preserve_math(self):
        self.assertNotEqual(scanner.normalize("x² + 10"), scanner.normalize("x2 + 10"))
        self.assertNotEqual(scanner.normalize("x + 10"), scanner.normalize("x - 10"))
        self.assertEqual(scanner.normalize("x − 10"), scanner.normalize("x - 10"))

    def test_changed_values_and_choices(self):
        a = question("A processor executes 100 instructions each second. How many instructions execute in 30 seconds?")
        b = question("A processor executes 200 instructions each second. How many instructions execute in 60 seconds?", ["30", "60", "3000", "12000"], "2008S_AM", year=2008)
        self.assertNotEqual(scanner.question_key(a), scanner.question_key(b))
        self.assertGreaterEqual(scanner.similarity(a, b), .8)
        self.assertEqual(len(scanner.match_questions([a, b])), 1)

    def test_changed_options_are_near(self):
        a = question("Which network protocol provides reliable delivery of packets over a connection?")
        b = question(a["stem"], ["alpha", "beta", "gamma", "epsilon"], "2008S_AM")
        self.assertEqual(scanner.match_questions([a, b])[0]["kind"], "strong")

    def test_boilerplate_does_not_match(self):
        a = question("Which of the following is the correct description of a database transaction?")
        b = question("Which of the following is the correct description of an optical communication cable?", paper="2008S_AM")
        self.assertEqual(scanner.match_questions([a, b]), [])

    def test_same_paper_excluded_and_visual_separated(self):
        a = question("Which network protocol provides reliable delivery of packets over a connection?")
        self.assertEqual(scanner.match_questions([a, dict(a)]), [])
        b = question(a["stem"], paper="2007A_AM", review=["Embedded image"])
        self.assertEqual(scanner.match_questions([a, b])[0]["kind"], "visual")

    def test_near_matches_do_not_form_transitive_groups(self):
        a = question("Which network protocol provides reliable delivery of packets over a connection?")
        b = question("Which network protocol provides reliable delivery of packets over a secure connection?", paper="2008S_AM")
        c = question("Which network protocol provides reliable delivery of messages over a secure connection?", paper="2009S_AM")
        matches = scanner.match_questions([a, b, c])
        self.assertTrue(matches)
        self.assertTrue(all(len(r["ids"]) == 2 for r in matches))


class ExtractionTests(unittest.TestCase):
    def test_choices_and_question_number(self):
        stem, choices = scanner.split_question("Q12. Choose a protocol.\na) TCP\nb) UDP\nc) IP\nd) HTTP")
        self.assertEqual(stem, "Choose a protocol.")
        self.assertEqual(choices, ["TCP", "UDP", "IP", "HTTP"])

    def test_real_2009_diagram_labels(self):
        pdf = scanner.ROOT / "Exam_Q&A/2009/April/2009Apr_FE_AM_Questions.pdf"
        with pymupdf.open(pdf) as doc:
            bounds = scanner.boundaries(doc, "AM")
            self.assertEqual(len(bounds), 80)
            self.assertEqual(bounds[2][0], 2)
            stem, choices, reasons = scanner.read_question(doc, bounds[18], bounds[19])
            self.assertIn("flip-flop", stem)
            self.assertTrue(reasons)

    def test_ambiguous_boundary_rejected(self):
        with pymupdf.open() as doc:
            for n in range(1, 61):
                page = doc.new_page()
                page.insert_text((60, 70), f"Q{n}. Select an option.")
                if n == 20:
                    page.insert_text((60, 120), "Q20. Another heading.")
            with self.assertRaisesRegex(ValueError, "Ambiguous Q20"):
                scanner.boundaries(doc, "A")

    def test_partial_and_malformed_pdf_reported(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            sources = root / "Exam_Q&A/2026/April"
            sources.mkdir(parents=True)
            (sources / "2026S_FE-A_Questions.pdf").write_bytes(b"not a pdf")
            questions, coverage, failures, _ = scanner.scan(root, root / "output")
            self.assertEqual(questions, [])
            self.assertEqual(len(failures), 1)
            self.assertEqual(coverage[0]["questions"], 0)

    def test_years_and_missing_note(self):
        self.assertEqual(scanner.parse_years("2007,2024-2026"), {2007, 2024, 2025, 2026})
        with tempfile.TemporaryDirectory() as folder:
            self.assertIsNone(scanner.note_for(Path(folder), 2007, "S", "AM", 1))

    def test_embedded_data_cannot_close_script(self):
        with tempfile.TemporaryDirectory() as folder:
            q = question('</script><img src=x onerror="alert(1)">')
            q.update({"_pdf": "unused", "_bounds": [], "previews": []})
            scanner.write_report(Path(folder), [q], [], [], [], [], .8)
            html = (Path(folder) / "index.html").read_text(encoding="utf-8")
            embedded = html.split('<script id="report-data" type="application/json">')[1].split('</script>')[0]
            self.assertNotIn("<", embedded)
            self.assertEqual(json.loads(embedded)["questions"][0]["stem"], q["stem"])


if __name__ == "__main__":
    unittest.main()
