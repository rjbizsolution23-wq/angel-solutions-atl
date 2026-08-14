import sys
import os
import pytest
from unittest.mock import patch, MagicMock

# Ensure backend root is in search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.core.elevenlabs import ElevenLabsClient
from backend.core.base44_sync import sync_to_base44

@pytest.mark.asyncio
async def test_elevenlabs_simulation():
    """Verify that ElevenLabs client initializes and performs fallback/simulation correctly"""
    client = ElevenLabsClient(api_key="")
    audio = await client.generate_speech(text="Welcome to RJ Business Solutions")
    assert audio is not None
    assert audio == b"MOCK_ELEVENLABS_AUDIO_PAYLOAD" or audio.startswith(b"ID3") or audio.startswith(b"\xff\xfb") or audio.startswith(b"\xff\xf3")

@pytest.mark.asyncio
async def test_base44_simulation():
    """Verify that Base44 sync handles unconfigured environment keys gracefully"""
    with patch("backend.core.base44_sync.BASE44_API_KEY", ""):
        success = await sync_to_base44("SearchHistory", {"query": "test query"})
        assert success is True

@pytest.mark.asyncio
async def test_base44_sync_transmits():
    """Verify that Base44 sync structures and transmits REST requests correctly when keys are present"""
    with patch("httpx.AsyncClient.post") as mock_post:
        # Mock successful POST response
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.text = "Created"
        mock_post.return_value = mock_response

        with patch("backend.core.base44_sync.BASE44_API_KEY", "test_key"), \
             patch("backend.core.base44_sync.BASE44_APP_ID", "test_app_id"):
            
            success = await sync_to_base44("SearchHistory", {
                "query": "Napoleon Hill",
                "search_type": "books",
                "results_count": 5,
                "results_summary": "Found books"
            })
            assert success is True
            assert mock_post.called
