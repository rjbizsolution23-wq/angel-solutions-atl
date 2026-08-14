/**
 * =====================================================================
 * ANGEL SOLUTIONS ATL - ELEVENLABS TTS VOICE GENERATION
 * =====================================================================
 * Synthesizes natural, high-converting voice notes using Jordynn's
 * cloned speech profile to increase DM conversion ratios.
 * =====================================================================
 */

/**
 * Synthesizes text into Jordynn's cloned voice MP3 file
 * @param {string} text 
 * @param {object} env 
 * @returns {Promise<object>} buffer or mock success
 */
export async function generateVoiceMessage(text, env) {
  const apiKey = env.ELEVENLABS_API_KEY;
  // Fallback to high-quality female Rachel voice if clone ID not set
  const voiceId = env.ELEVENLABS_VOICE_ID || "21m00Tcm4TlvDq8ikWAM"; 

  if (!apiKey) {
    console.log(`[MOCK ELEVENLABS TTS] Synthesizing text: "${text}" into Rick voice.`);
    return {
      success: true,
      audioBuffer: new ArrayBuffer(8192), // Mock buffer
      mimeType: "audio/mpeg"
    };
  }

  const endpoint = `https://api.elevenlabs.io/v1/text-to-speech/${voiceId}`;

  try {
    const response = await fetch(endpoint, {
      method: "POST",
      headers: {
        "xi-api-key": apiKey,
        "Content-Type": "application/json",
        "accept": "audio/mpeg"
      },
      body: JSON.stringify({
        text: text,
        model_id: "eleven_monolingual_v1",
        voice_settings: {
          stability: 0.75,
          similarity_boost: 0.85
        }
      })
    });

    if (!response.ok) {
      throw new Error(`ElevenLabs API returned error status: ${response.status}`);
    }

    const audioBuffer = await response.arrayBuffer();
    console.log("ElevenLabs MP3 voice synthesis completed successfully!");

    return {
      success: true,
      audioBuffer: audioBuffer,
      mimeType: "audio/mpeg"
    };

  } catch (error) {
    console.error("ElevenLabs TTS voice synthesis failed:", error);
    return {
      success: false,
      error: error.message
    };
  }
}
