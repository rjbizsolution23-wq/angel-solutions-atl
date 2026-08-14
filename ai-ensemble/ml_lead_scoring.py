/**
 * =====================================================================
 * ANGEL SOLUTIONS ATL - PREDICTIVE MACHINE LEARNING LEAD SCORER
 * =====================================================================
 * Scikit-Learn based RandomForest pipeline for scoring lead intent
 * and predicting conversion probabilities. Fallbacks gracefully if missing.
 * =====================================================================
 */

import os

# Graceful Scikit-Learn imports
HAS_ML_LIBRARIES = False
try:
    import numpy as np
    from sklearn.ensemble import RandomForestClassifier
    HAS_ML_LIBRARIES = True
except ImportError:
    pass

class LeadScoringModel:
    def __init__(self):
        self.model = None
        if HAS_ML_LIBRARIES:
            self.model = RandomForestClassifier(n_estimators=50, random_state=42)
            self._train_initial_mock_model()

    def _train_initial_mock_model(self):
        """
        Trains a quick offline baseline classifier on typical Angel Solutions ATL
        lead histories to compute initial scoring parameters.
        """
        # Features: [has_intent_keywords, stated_credit_score_range, stated_timeline_days, message_count, platform_encoded]
        # Credit Score encoded: 0 = Under 500, 1 = 500-600, 2 = 600-700, 3 = Over 700
        # Timeline encoded: 0 = Urgent (<30d), 1 = Standard (30-90d), 2 = DIY (>90d)
        # Platform encoded: 0 = IG, 1 = FB, 2 = WA
        X_train = np.array([
            [1, 1, 0, 8, 0], # Qualified advanced plan lead
            [1, 0, 1, 3, 1], # Mid tier lead
            [0, 3, 2, 1, 0], # Cold lead DIY
            [1, 2, 0, 12, 2],# Hot lead Whatsapp
            [0, 1, 2, 2, 1], # Low quality monthly lead
            [1, 1, 1, 5, 0], # Qualified monthly lead
            [1, 2, 0, 7, 0], # Hot credit repair lead
            [0, 0, 2, 1, 1]  # Cold spambot lead
        ])
        # Y labels: 1 = Highly likely to convert, 0 = Unlikely to convert
        y_train = np.array([1, 0, 0, 1, 0, 1, 1, 0])
        self.model.fit(X_train, y_train)

    def calculate_score(self, lead_data: dict) -> dict:
        """
        Predicts a lead conversion probability score [0.0 to 1.0].
        Calculates recommended CRM tags and ideal offer routing.
        """
        # Extract features
        has_intent = 1 if lead_data.get("has_intent_keywords", True) else 0
        
        # Normalize credit score
        score_val = lead_data.get("stated_credit_score", 550)
        score_enc = 1
        if score_val < 500:
            score_enc = 0
        elif 500 <= score_val < 600:
            score_enc = 1
        elif 600 <= score_val < 700:
            score_enc = 2
        else:
            score_enc = 3

        # Normalize timeline
        timeline_days = lead_data.get("stated_timeline_days", 60)
        timeline_enc = 1
        if timeline_days <= 30:
            timeline_enc = 0
        elif 30 < timeline_days <= 90:
            timeline_enc = 1
        else:
            timeline_enc = 2

        msg_count = lead_data.get("message_count", 3)
        
        platform_map = {"instagram": 0, "facebook": 1, "whatsapp": 2}
        plat_enc = platform_map.get(lead_data.get("platform", "instagram").lower(), 0)

        probability = 0.5 # Baseline fallback

        if HAS_ML_LIBRARIES and self.model:
            try:
                features = np.array([[has_intent, score_enc, timeline_enc, msg_count, plat_enc]])
                prob_array = self.model.predict_proba(features)
                probability = float(prob_array[0][1])
            except Exception as e:
                print(f"Error calling ML model prediction: {e}. Falling back to baseline rule-matrix.")
                probability = self._rule_based_scoring(has_intent, score_enc, timeline_enc, msg_count)
        else:
            # High-end matrix-based fallback if numpy/scikit-learn not available
            probability = self._rule_based_scoring(has_intent, score_enc, timeline_enc, msg_count)

        # Categorize conversion likelihood
        likelihood = "LOW"
        if probability >= 0.70:
            likelihood = "HIGH"
        elif probability >= 0.40:
            likelihood = "MEDIUM"

        # Determine target CRM offer routing
        recommended_offer = "Monthly Plan ($67/mo)"
        if score_enc <= 1 and timeline_enc == 0:
            recommended_offer = "Advanced Credit Restoral ($795)"
        elif lead_data.get("collections_count", 0) >= 5:
            recommended_offer = "Advanced Credit Restoral ($795)"

        return {
            "lead_score": round(probability, 2),
            "likelihood": likelihood,
            "recommended_offer": recommended_offer,
            "crm_tags": [f"score_{likelihood.lower()}", f"tier_{recommended_offer.split()[0].lower()}"],
            "model_engine": "RandomForestClassifier" if HAS_ML_LIBRARIES else "RuleMatrixEngine"
        }

    def _rule_based_scoring(self, has_intent, score_enc, timeline_enc, msg_count):
        """
        High fidelity backup scoring algorithm using scoring matrix
        """
        base = 0.3
        if has_intent: base += 0.2
        if score_enc == 1 or score_enc == 2: base += 0.15 # Best sweet spot for credit repair leads
        if timeline_enc == 0: base += 0.15 # Urgent timeline
        if msg_count > 5: base += 0.1 # High interaction
        
        return max(0.0, min(1.0, base))
