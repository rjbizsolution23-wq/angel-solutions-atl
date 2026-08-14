# =====================================================================
# ANGEL SOLUTIONS ATL - MULTILANGUAGE ENSEMBLE ROUTER
# =====================================================================
# Integrates translation and language detection pipelines to serve
# the Spanish-speaking community seamlessly.
# =====================================================================

import re
import os
import requests

SPANISH_INDICATORS = [
    r"\bhola\b", r"\bcredito\b", r"\bdeuda\b", r"\bgracias\b", r"\bayuda\b",
    r"\breparacion\b", r"\bprecio\b", r"\bcosto\b", r"\binformacion\b", r"\bpor favor\b"
]

def detect_language(text: str) -> str:
    """
    Detects if a user message is primarily English ('en') or Spanish ('es').
    """
    if not text:
        return "en"

    clean_text = text.lower().strip()
    
    # Count Spanish keywords
    spanish_hits = 0
    for pattern in SPANISH_INDICATORS:
        if re.search(pattern, clean_text):
            spanish_hits += 1

    # Simple indicator matching
    if spanish_hits >= 1 or any(word in clean_text for word in ["como", "para", "quiero", "reparar", "historial"]):
        return "es"

    return "en"

def translate_text(text: str, target_lang: str) -> str:
    """
    Translates text to target language ('en' or 'es') using Workers AI.
    Falls back to regex-based glossary for testing if AI keys are offline.
    """
    if not text:
        return ""

    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
    ai_gateway_url = os.getenv("AI_ENSEMBLE_URL") or "https://api.anthropic.com/v1/messages"

    if not api_key:
        # Fallback basic glossary map
        glossary = {
            "hola": "hello",
            "reparacion de credito": "credit repair",
            "cuanto cuesta": "how much does it cost",
            "gracias": "thank you",
            "book your strategy call here": "reserve su llamada de estrategia aqui",
            "credit repair monthly": "reparación de crédito mensual",
            "advanced credit restoral": "restauración de crédito avanzada"
        }
        translated = text.lower()
        if target_lang == "en":
            for k, v in glossary.items():
                translated = translated.replace(k, v)
        else:
            for k, v in glossary.items():
                translated = translated.replace(v, k)
        return translated.capitalize()

    # Call AI Translation via unified prompt
    prompt = f"You are a professional financial translator. Translate the following text into fluent, modern, premium {'Spanish' if target_lang == 'es' else 'English'}. Return ONLY the direct translated text. Do not add any conversational remarks.\n\nText: {text}"
    
    payload = {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 512,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1
    }

    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    try:
        response = requests.post(ai_gateway_url, json=payload, headers=headers, timeout=10)
        data = response.json()
        return data["content"][0]["text"].strip()
    except Exception as e:
        print(f"Translation pipeline error: {e}. Returning original text.")
        return text
