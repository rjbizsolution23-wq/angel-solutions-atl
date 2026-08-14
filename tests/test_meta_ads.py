# =====================================================================
# ANGEL SOLUTIONS ATL - META ADS SUITE VERIFICATION TESTS
# =====================================================================
# Validates the programmatic launcher, campaign metric insights,
# compliance filters, and KPI analytics engine.
# =====================================================================

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Set up module path resolution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../admin-panel")))

import meta_ads_client
from meta_ads_client import MetaAdsClient
from analytics_dashboard import compute_conversion_kpis

class MetaAdsSuiteTests(unittest.TestCase):

    def setUp(self):
        # Force client into simulation/fallback mode for predictable and decoupled unit testing
        self.client = MetaAdsClient()
        self.client.is_live = False

    def test_client_initialization_defaults(self):
        """
        Validates that the MetaAdsClient initializes with appropriate default settings
        and handles credential fallback gracefully.
        """
        # Test module-level configurations
        self.assertEqual(meta_ads_client.META_VERSION, "v25.0")
        self.assertEqual(meta_ads_client.GRAPH_URL, "https://graph.facebook.com")
        
        # Ensure account ID has 'act_' prefix if not already present or fallback is set
        if "MOCK" in self.client.ad_account_id:
            self.assertTrue(self.client.ad_account_id.startswith("act_") or self.client.ad_account_id == "MOCK_AD_ACCOUNT_ID")

    def test_fetch_campaigns_structure(self):
        """
        Ensures that pulling active campaign statistics produces standardized,
        well-structured dictionary feeds (spend, clicks, impressions, conversions).
        """
        campaigns = self.client.fetch_campaigns()
        self.assertIsInstance(campaigns, list)
        self.assertGreater(len(campaigns), 0)

        # Validate structure of the returned campaigns
        for camp in campaigns:
            self.assertIn("id", camp)
            self.assertIn("name", camp)
            self.assertIn("status", camp)
            self.assertIn("budget", camp)
            self.assertIn("spend", camp)
            self.assertIn("impressions", camp)
            self.assertIn("clicks", camp)
            self.assertIn("conversions", camp)
            
            # Numeric type validations
            self.assertIsInstance(camp["budget"], (int, float))
            self.assertIsInstance(camp["spend"], (int, float))
            self.assertIsInstance(camp["impressions"], int)
            self.assertIsInstance(camp["clicks"], int)
            self.assertIsInstance(camp["conversions"], int)

    def test_campaign_publishing_compliance_simulation(self):
        """
        Validates that launching a new campaign in simulation mode enforces CROA
        compliance parameters, such as designating ['CREDIT'] special ad categories.
        """
        campaign_name = "Unit Test Compliance Campaign"
        budget = 45.0
        copy_text = "Let's clear negative collection accounts. Instant results."
        lead_form = "form_unit_test_99"

        # Execute campaign creation dry-run simulation
        result = self.client.create_leadgen_campaign(
            name=campaign_name,
            daily_budget_dollars=budget,
            ai_copy=copy_text,
            lead_form_id=lead_form
        )

        self.assertTrue(result["success"])
        self.assertIn("logs", result)
        
        # Verify that special ad category 'CREDIT' compliance was logged/validated
        compliance_check = any("CREDIT" in log for log in result["logs"])
        self.assertTrue(compliance_check, "Campaign failed to set or log mandatory CREDIT Special Ad Category.")

    @patch("meta_ads_client.requests.post")
    def test_campaign_publishing_live_mocked(self, mock_post):
        """
        Tests the live execution path of create_leadgen_campaign with mocked requests,
        verifying that API endpoints are called with appropriate payloads.
        """
        # Force live mode temporarily for this specific unit test
        self.client.is_live = True
        self.client.access_token = "mock_valid_long_access_token_to_pass_live_check_threshold_key"
        
        # Configure mocks for the 4 HTTP POST endpoints in the live creation pipeline
        response_camp = MagicMock()
        response_camp.status_code = 200
        response_camp.json.return_value = {"id": "11111111"}

        response_adset = MagicMock()
        response_adset.status_code = 200
        response_adset.json.return_value = {"id": "22222222"}

        response_creative = MagicMock()
        response_creative.status_code = 200
        response_creative.json.return_value = {"id": "33333333"}

        response_ad = MagicMock()
        response_ad.status_code = 200
        response_ad.json.return_value = {"id": "44444444"}

        mock_post.side_effect = [response_camp, response_adset, response_creative, response_ad]

        result = self.client.create_leadgen_campaign(
            name="Live Mock Campaign",
            daily_budget_dollars=35.0,
            ai_copy="Get funded now.",
            lead_form_id="form_mock_001"
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["campaign_id"], "11111111")
        self.assertEqual(result["adset_id"], "22222222")
        self.assertEqual(result["creative_id"], "33333333")
        self.assertEqual(result["ad_id"], "44444444")
        
        # Ensure 'CREDIT' special ad category is present in the payload sent to Meta
        camp_call_args = mock_post.call_args_list[0]
        payload = camp_call_args[1]["data"]
        self.assertEqual(payload["special_ad_categories"], "['CREDIT']")

    def test_analytics_dashboard_kpi_math(self):
        """
        Verifies that the analytics dashboard correctly aggregates metrics
        and returns calculated CPC, CTR, CPL, and ROAS.
        """
        # Call compute_conversion_kpis with a mock database context (None handles default mocks)
        kpi_data = compute_conversion_kpis(None)
        
        self.assertIn("metrics", kpi_data)
        metrics = kpi_data["metrics"]
        
        # Verify specific Ad metrics exist
        self.assertIn("ad_spend", metrics)
        self.assertIn("ctr_percentage", metrics)
        self.assertIn("cpc", metrics)
        self.assertIn("cpl", metrics)
        self.assertIn("roas", metrics)
        self.assertIn("estimated_revenue", metrics)

        # Mathematical verification
        spend = metrics["ad_spend"]
        clicks = metrics["ad_clicks"]
        impressions = metrics["ad_impressions"]
        conversions = metrics["ad_conversions"]
        
        if impressions > 0:
            expected_ctr = round((clicks / impressions * 100), 2)
            self.assertEqual(metrics["ctr_percentage"], expected_ctr)
            
        if clicks > 0:
            expected_cpc = round((spend / clicks), 2)
            self.assertEqual(metrics["cpc"], expected_cpc)

        if conversions > 0:
            expected_cpl = round((spend / conversions), 2)
            self.assertEqual(metrics["cpl"], expected_cpl)

    def test_form_creation_simulation(self):
        """
        Validates the structure and logs returned when creating a Lead Gen Form in simulation mode.
        """
        form_name = "Simulation Funding Form"
        privacy_url = "https://angelsolutionsatl.com/privacy"
        redirect_url = "https://angelsolutionsatl.com/book-online"
        custom_q = "Estimated Credit Score?"

        result = self.client.create_lead_form(
            name=form_name,
            privacy_policy_url=privacy_url,
            redirect_url=redirect_url,
            custom_question_text=custom_q
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["mode"], "SIMULATION")
        self.assertTrue(result["form_id"].startswith("form_sim_"))
        
        # Verify specific bound URLs and custom questions are in the creation logs
        logs_joined = " ".join(result["logs"])
        self.assertIn(privacy_url, logs_joined)
        self.assertIn(redirect_url, logs_joined)
        self.assertIn(custom_q, logs_joined)

    @patch("meta_ads_client.requests.post")
    def test_form_creation_live_mocked(self, mock_post):
        """
        Tests the live execution path of create_lead_form with mocked requests,
        verifying that API endpoints are called with appropriate payloads.
        """
        self.client.is_live = True
        self.client.access_token = "mock_valid_long_access_token_to_pass_live_check_threshold_key"
        
        response_form = MagicMock()
        response_form.status_code = 200
        response_form.json.return_value = {"id": "form_live_1234567"}
        
        mock_post.return_value = response_form

        form_name = "Live Mock Form"
        privacy_url = "https://angelsolutionsatl.com/privacy"
        redirect_url = "https://angelsolutionsatl.com/book-online"
        
        result = self.client.create_lead_form(
            name=form_name,
            privacy_policy_url=privacy_url,
            redirect_url=redirect_url
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["form_id"], "form_live_1234567")
        self.assertEqual(result["mode"], "LIVE")

        # Verify post payload arguments
        call_args = mock_post.call_args
        payload = call_args[1]["data"]
        self.assertEqual(payload["name"], form_name)
        self.assertEqual(payload["follow_up_action_url"], redirect_url)
        self.assertIn(privacy_url, payload["privacy_policy"])

if __name__ == "__main__":
    unittest.main()
