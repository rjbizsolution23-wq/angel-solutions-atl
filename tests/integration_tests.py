# =====================================================================
# ANGEL SOLUTIONS ATL - END-TO-END PIPELINE INTEGRATION TESTS
# =====================================================================
# Validates the full webhook ingestion to database logging to AI reasoning
# pipeline. Runs automated simulations of standard user lifecycles.
# =====================================================================

import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../ai-ensemble")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../admin-panel")))

# Import pipeline components
from tests import keyword_engine
import jordynn_ai
import sentiment_analysis
import conversation_handoff

# Mock D1 DB context class for local pipeline simulation
class MockD1Database:
    def __init__(self):
        self.queries_run = []
        
    class MockStatement:
        def __init__(self, query, parent):
            self.query = query
            self.parent = parent
        def bind(self, *args):
            self.parent.queries_run.append({"query": self.query, "args": args})
            return self
        def run(self):
            return {"success": True}
            
    def prepare(self, query):
        return self.MockStatement(query, self)

class IntegrationPipelineTests(unittest.TestCase):

    def setUp(self):
        self.db = MockD1Database()

    def test_pipeline_path_qualified_skool_routing(self):
        """
        Validates pipeline flow when a lead expresses standard interest
        and has basic credit restoral requirements.
        """
        user_message = "I want to repair my credit score, it's currently around 580."
        
        # 1. Edge Webhook Ingestion & Scrubbing Checks
        clean_msg = keyword_engine.apply_compliance_scrubbing(user_message)
        self.assertEqual(clean_msg, user_message) # No violations

        # 2. Intention & Classification Extraction
        is_escalation = keyword_engine.check_escalation_triggers(clean_msg)
        self.assertFalse(is_escalation) # Not an emergency

        # 3. Sentiment Analysis Check
        sentiment = sentiment_analysis.analyze_sentiment(clean_msg)
        self.assertFalse(sentiment["flag_escalation"]) # Satisfied sentiment
        
        # 4. Invoke Claude Brand Voice Generation
        conversation_history = [{"role": "user", "content": clean_msg}]
        ai_reply = jordynn_ai.generate_rick_response(conversation_history)
        self.assertTrue(ai_reply["success"])
        self.assertIsNotNone(ai_reply["reply"])
        self.assertNotIn("credit sweep", ai_reply["reply"].lower()) # Double check output safety

    def test_pipeline_path_emergency_esc_handoff(self):
        """
        Validates pipeline flow when a lead outputs critical frustration.
        Disables AI triggers and executes immediate human escalation.
        """
        user_message = "Your bot is annoying. This company is a scam. I want a refund now."
        
        # 1. Edge Webhook Ingestion
        clean_msg = keyword_engine.apply_compliance_scrubbing(user_message)
        
        # 2. Sentiment analysis identifies anger
        sentiment = sentiment_analysis.analyze_sentiment(clean_msg)
        self.assertTrue(sentiment["flag_escalation"])

        # 3. Initiate Handoff Sequence in DB
        handoff_res = conversation_handoff.initiate_human_handoff(
            lead_id="lead_99", 
            conversation_id="conv_99", 
            trigger_msg=clean_msg, 
            reason="scam_and_refund_request", 
            db_env=self
        )
        
        self.assertTrue(handoff_res["success"])
        self.assertFalse(handoff_res["bot_active"])
        self.assertIn("Immediate response needed", handoff_res["sms_payload"]["body"])

if __name__ == "__main__":
    unittest.main()
