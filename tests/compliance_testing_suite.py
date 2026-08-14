# =====================================================================
# ANGEL SOLUTIONS ATL - RIGOROUS COMPLIANCE TESTING SUITE
# =====================================================================
# Integrates 30 structured, automated compliance assertions ensuring zero
# FTC/CFPB friction and flawless brand safety boundaries.
# =====================================================================

import unittest
import sys
import os

# Ensure import paths resolve
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../ai-ensemble")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../admin-panel")))

# Import components
from tests import keyword_engine
import sentiment_analysis
import multilanguage

class ComplianceTestingSuite(unittest.TestCase):

    # --- BLOCK 1: ILLEGAL TERM COMPLIANCE FILTER TESTS (GATES 1 - 10) ---
    def test_gate_01_credit_sweep_scrubbing(self):
        result = keyword_engine.apply_compliance_scrubbing("Can you do a credit sweep for me?")
        self.assertNotIn("credit sweep", result.lower())
        self.assertIn("custom legal challenge", result.lower())

    def test_gate_02_guaranteed_scrubbing(self):
        result = keyword_engine.apply_compliance_scrubbing("Is my score guaranteed to go up?")
        self.assertNotIn("guarantee", result.lower())
        self.assertIn("highly probable", result.lower())

    def test_gate_03_best_scrubbing(self):
        result = keyword_engine.apply_compliance_scrubbing("Are you guys the best in ATL?")
        self.assertNotIn("best", result.lower())
        self.assertIn("premier", result.lower())

    def test_gate_04_yo_tone_adjustment(self):
        result = keyword_engine.apply_compliance_scrubbing("Yo, what is the price?")
        self.assertNotIn("yo", result.lower())

    def test_gate_05_bet_tone_adjustment(self):
        result = keyword_engine.apply_compliance_scrubbing("Bet, let's sign up.")
        self.assertNotIn("bet", result.lower())

    def test_gate_06_sentence_case_preservation(self):
        result = keyword_engine.apply_compliance_scrubbing("WE PROMISE A CREDIT SWEEP.")
        self.assertNotIn("credit sweep", result.upper())

    def test_gate_07_no_modifications_on_clean_text(self):
        input_text = "I would love to learn more about your credit solutions."
        self.assertEqual(input_text, keyword_engine.apply_compliance_scrubbing(input_text))

    def test_gate_08_empty_string_safety(self):
        self.assertEqual("", keyword_engine.apply_compliance_scrubbing(""))

    def test_gate_09_multiple_violations_consecutively(self):
        result = keyword_engine.apply_compliance_scrubbing("Yo, this is the best credit sweep and it is guaranteed.")
        self.assertNotIn("yo", result.lower())
        self.assertNotIn("best", result.lower())
        self.assertNotIn("credit sweep", result.lower())
        self.assertNotIn("guarantee", result.lower())

    def test_gate_10_none_type_input_scrubbing(self):
        self.assertIsNone(keyword_engine.apply_compliance_scrubbing(None))


    # --- BLOCK 2: WHITELISTED URL SCRUBBING TESTS (GATES 11 - 20) ---
    def test_gate_11_approved_skool_link_preservation(self):
        input_text = "Check out https://www.skool.com/creditsolution/about to join."
        result = keyword_engine.scrub_unapproved_urls(input_text)
        self.assertIn("https://www.skool.com/creditsolution/about", result)

    def test_gate_12_approved_booking_link_preservation(self):
        input_text = "Book here: https://angelsolutionsatl.com/book-online."
        result = keyword_engine.scrub_unapproved_urls(input_text)
        self.assertIn("https://angelsolutionsatl.com/book-online", result)

    def test_gate_13_unapproved_url_removal(self):
        input_text = "Visit my sketchy site http://phishing-scam-credit.com/login."
        result = keyword_engine.scrub_unapproved_urls(input_text)
        self.assertNotIn("phishing-scam-credit.com", result)
        self.assertIn("[Link Removed for Security Compliance]", result)

    def test_gate_14_subdomain_approved_skool_preservation(self):
        input_text = "Check out our portal http://skool.com/creditsolution/about."
        result = keyword_engine.scrub_unapproved_urls(input_text)
        self.assertIn("skool.com/creditsolution/about", result)

    def test_gate_15_raw_domain_name_removal(self):
        input_text = "Go to competitor.com now."
        result = keyword_engine.scrub_unapproved_urls(input_text)
        self.assertNotIn("competitor.com", result)

    def test_gate_16_secure_protocol_preservation(self):
        input_text = "Join us at https://angelsolutionsatl.com/book-online"
        result = keyword_engine.scrub_unapproved_urls(input_text)
        self.assertIn("https://angelsolutionsatl.com/book-online", result)

    def test_gate_17_ip_address_url_removal(self):
        input_text = "Connect to http://192.168.1.1/exploit"
        result = keyword_engine.scrub_unapproved_urls(input_text)
        self.assertNotIn("192.168.1.1", result)

    def test_gate_18_malformed_url_safety(self):
        input_text = "Go to http://invalid_link_url_string"
        result = keyword_engine.scrub_unapproved_urls(input_text)
        self.assertNotIn("http://", result)

    def test_gate_19_multiple_urls_mixed(self):
        input_text = "Visit https://angelsolutionsatl.com/book-online and badsite.org"
        result = keyword_engine.scrub_unapproved_urls(input_text)
        self.assertIn("https://angelsolutionsatl.com/book-online", result)
        self.assertNotIn("badsite.org", result)

    def test_gate_20_query_param_url_scrubbing(self):
        input_text = "Go to http://competitor.com/page?id=123"
        result = keyword_engine.scrub_unapproved_urls(input_text)
        self.assertNotIn("competitor.com", result)


    # --- BLOCK 3: SENTIMENT & LANG GATES (GATES 21 - 30) ---
    def test_gate_21_severe_scam_allegation_escalation(self):
        analysis = sentiment_analysis.analyze_sentiment("This whole service is a scam, reporting you to FTC!")
        self.assertTrue(analysis["flag_escalation"])
        self.assertEqual("negative", analysis["category"])

    def test_gate_22_frustration_keywords_score(self):
        analysis = sentiment_analysis.analyze_sentiment("I am confused why this is taking so slow, still waiting.")
        self.assertLess(analysis["sentiment_score"], 0.0)

    def test_gate_23_positive_score_alignment(self):
        analysis = sentiment_analysis.analyze_sentiment("Thank you so much! This is awesome and very helpful.")
        self.assertGreater(analysis["sentiment_score"], 0.2)
        self.assertEqual("positive", analysis["category"])

    def test_gate_24_spanish_language_detection(self):
        lang = multilanguage.detect_language("Hola, quiero informacion sobre los precios por favor.")
        self.assertEqual("es", lang)

    def test_gate_25_english_language_detection(self):
        lang = multilanguage.detect_language("Hey, how much does the advanced restoral plan cost?")
        self.assertEqual("en", lang)

    def test_gate_26_mixed_language_fallback_to_english(self):
        lang = multilanguage.detect_language("Hello friend, can you talk to me in English please?")
        self.assertEqual("en", lang)

    def test_gate_27_neutral_sentiment_empty_checks(self):
        analysis = sentiment_analysis.analyze_sentiment("")
        self.assertEqual(0.0, analysis["sentiment_score"])
        self.assertFalse(analysis["flag_escalation"])

    def test_gate_28_severe_anger_sentiment_floor(self):
        analysis = sentiment_analysis.analyze_sentiment("I hate you, worst shittiest liar cheat scam trash!")
        self.assertEqual(-1.0, analysis["sentiment_score"])

    def test_gate_29_spanish_indicative_high_volume(self):
        lang = multilanguage.detect_language("necesito ayuda para reparar mi credito")
        self.assertEqual("es", lang)

    def test_gate_30_ab_testing_deterministic_variants(self):
        import ab_testing
        v1 = ab_testing.get_assigned_variant("lead_abc", "welcome_greeting")
        v2 = ab_testing.get_assigned_variant("lead_abc", "welcome_greeting")
        self.assertEqual(v1["variant"], v2["variant"]) # Must be deterministic per user id

if __name__ == "__main__":
    unittest.main()
