import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location(
    "lint", ROOT / "skills" / "unslop-pl-en" / "scripts" / "lint.py")
lint_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lint_mod)


def rules(text, lang="pl", sev=None):
    found = lint_mod.lint(text, lang)["findings"]
    return [f["rule"] for f in found if sev is None or f["sev"] == sev]


class PolishChecks(unittest.TestCase):
    def test_mismatched_quote_closer(self):
        self.assertIn("pl-quote-mismatch", rules('To jest „test".'))

    def test_correct_quotes_are_clean(self):
        self.assertNotIn("pl-quote-mismatch", rules("To jest „test”."))
        self.assertNotIn("pl-quote-straight", rules("To jest „test”."))

    def test_straight_quotes(self):
        self.assertIn("pl-quote-straight", rules('Napisał "krótko" i wyszedł.'))

    def test_ended_role_in_present_tense(self):
        text = "07.2010 – 03.2026 | Dyrektor\nKieruję zespołami analityków.\n"
        self.assertIn("pl-tense-vs-dates", rules(text))

    def test_ongoing_role_in_present_tense_is_fine(self):
        text = "04.2026 – obecnie | Kierownik\nKieruję zespołami analityków.\n"
        self.assertNotIn("pl-tense-vs-dates", rules(text))

    def test_mixed_address_forms(self):
        self.assertIn("pl-address-mixed",
                      rules("Pracujemy na Waszych danych. Zaplanujmy szkolenie dla Twojej firmy."))

    def test_single_address_form_is_fine(self):
        self.assertNotIn("pl-address-mixed", rules("Pracujemy na Waszych danych i Waszych przypadkach."))

    def test_delivery_calque_and_register(self):
        r = rules("Prowadzę dostarczanie projektów i spinam zespoły.")
        self.assertEqual(r.count("calque"), 2)

    def test_single_correction_is_not_p1(self):
        self.assertNotIn("contrast-candidate", rules("Użyj wersji 3, nie 2.", sev="P1"))

    def test_three_contrasts_are_p1(self):
        text = ("Uczę na Waszych danych, nie na demo. Zespół wychodzi z workflow, nie z notatkami. "
                "To zmiana nawyków, nie jednorazowy event.")
        self.assertEqual(rules(text, sev="P1").count("contrast-candidate"), 3)

    def test_unspaced_em_dash(self):
        self.assertIn("pl-dash-unspaced", rules("Szybko—i tanio."))

    def test_code_is_ignored(self):
        text = "Opis.\n\n```\nprint('kompleksowe rozwiązanie')\n```\n"
        self.assertNotIn("stock-phrase", rules(text))

    def test_title_case_heading(self):
        text = "# Szkolenia I Wdrożenia Dla Firm\n\nTreść.\n"
        res = lint_mod.lint(text, "pl", {1})
        self.assertIn("pl-title-case", [f["rule"] for f in res["findings"]])

    def test_clean_prose_has_no_p1(self):
        text = ("Od 2015 roku prowadzę szkolenia z rynku energii. "
                "Zespół wdrożył moduł rozliczeń w trzy miesiące, a testy wykazały 12 błędów.")
        self.assertEqual(rules(text, sev="P1"), [])


class EnglishChecks(unittest.TestCase):
    def test_stock_words(self):
        r = rules("We leverage a robust, seamless platform to unlock value.", "en")
        self.assertGreaterEqual(r.count("stock-phrase"), 4)

    def test_negative_parallelism(self):
        self.assertIn("contrast-candidate", rules("It's not a tool, it's a mindset.", "en"))

    def test_correction_is_p2_only(self):
        self.assertEqual(rules("The drop was 40%, not 4%.", "en", sev="P1"), [])

    def test_plain_text_is_clean(self):
        self.assertEqual(rules("The team shipped the export feature on Tuesday.", "en", sev="P1"), [])


class Input(unittest.TestCase):
    def test_html_is_stripped(self):
        html = "<html><head><style>x{}</style></head><body><h1>Tytuł</h1><p>Prowadzę dostarczanie.</p></body></html>"
        p = lint_mod._Text()
        p.feed(html)
        p._flush()
        self.assertIn("Prowadzę dostarczanie.", p.lines)
        self.assertEqual(p.headings, {1})

    def test_language_detection(self):
        self.assertEqual(lint_mod.detect_lang("To jest tekst, który jest po polsku i nie ma wątpliwości."), "pl")
        self.assertEqual(lint_mod.detect_lang("This is the text that is in English and the answer is clear."), "en")


if __name__ == "__main__":
    unittest.main()
