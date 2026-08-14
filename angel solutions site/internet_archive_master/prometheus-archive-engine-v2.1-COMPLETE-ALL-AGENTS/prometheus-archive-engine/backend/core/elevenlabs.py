"""
Prometheus Archive Engine - ElevenLabs Text-to-Speech Integration
Supports high-quality AI narration and audiobook generation for rebranded book content.
"""
import os
import logging
from typing import Optional, Dict, Any
import httpx

logger = logging.getLogger(__name__)

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
ELEVENLABS_DEFAULT_VOICE_ID = os.getenv("ELEVENLABS_DEFAULT_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")  # Rachel
ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1"

class ElevenLabsClient:
    """
    Client wrapper for ElevenLabs Audio AI Services.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or ELEVENLABS_API_KEY
        self.headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        } if self.api_key else {}

    async def generate_speech(
        self,
        text: str,
        voice_id: Optional[str] = None,
        model_id: str = "eleven_multilingual_v2",
        stability: float = 0.5,
        similarity_boost: float = 0.75
    ) -> Optional[bytes]:
        """
        Synthesizes text into high-quality spoken audio using ElevenLabs.
        
        Args:
            text: Text to synthesize
            voice_id: Voice identifier (defaults to Rachel)
            model_id: ElevenLabs model identifier (eleven_v3, eleven_multilingual_v2)
            stability: Consistency/variability factor
            similarity_boost: Matching boost
            
        Returns:
            bytes: MP3 audio file content or None if error or unconfigured
        """
        if not self.api_key:
            logger.info("ElevenLabs API Key not configured. Simulating speech synthesis.")
            # Mock empty audio payload for testing/simulated fallback
            return b"MOCK_ELEVENLABS_AUDIO_PAYLOAD"

        target_voice = voice_id or ELEVENLABS_DEFAULT_VOICE_ID
        url = f"{ELEVENLABS_API_URL}/text-to-speech/{target_voice}"
        
        payload = {
            "text": text,
            "model_id": model_id,
            "voice_settings": {
                "stability": stability,
                "similarity_boost": similarity_boost
            }
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(url, json=payload, headers=self.headers)
                if response.status_code == 200:
                    logger.info("✅ ElevenLabs speech synthesis succeeded")
                    return response.content
                else:
                    logger.error(f"❌ ElevenLabs API error ({response.status_code}): {response.text}")
                    return None
        except Exception as exc:
            logger.error(f"❌ Exception during ElevenLabs speech generation: {str(exc)}")
            return None

    async def list_voices(self) -> Optional[Dict[str, Any]]:
        """Retrieve all premium custom and premade voices in library"""
        if not self.api_key:
            return {"voices": [{"voice_id": "mock_voice_1", "name": "Simulated voice"}]}

        url = f"{ELEVENLABS_API_URL}/voices"
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, headers=self.headers)
                if response.status_code == 200:
                    return response.json()
                return None
        except Exception as exc:
            logger.error(f"❌ Failed to query ElevenLabs voice library: {str(exc)}")
            return None
