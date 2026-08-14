/**
 * ⚡ RJ VAULT FLOW - API INTEGRATIONS SUITE
 * Edge-Native Cloudflare Serverless / Base44 Integrations
 * Mapped to: OpenRouter, Together AI (FLUX), ElevenLabs, and Cloudflare R2 Storage
 */

// 1. 🤖 OPENROUTER DEEPSEEK V3 GAME GENERATOR
export async function generateGameCode(prompt, platform = 'HTML5/Phaser') {
  const apiKey = process.env.OPENROUTER_API_KEY;
  if (!apiKey) throw new Error("Missing OPENROUTER_API_KEY environment variable");

  const systemPrompt = `You are an elite retro game engine and expert Phaser 3 developer.
Generate a single self-contained HTML5 file containing custom CSS, canvas, logic, and asset references based on the requested idea.
Make sure the game is fully interactive, responsive, contains retro audio synthesize fallbacks, and keyboard key controller bindings.
Output ONLY the clean executable code, do not write markdown or commentary.`;

  try {
    const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${apiKey}`,
        "Content-Type": "application/json",
        "HTTP-Referer": "https://rj-vault-flow.base44.app",
        "X-Title": "RJ Vault Flow"
      },
      body: JSON.stringify({
        model: "deepseek/deepseek-chat", // DeepSeek V3
        messages: [
          { role: "system", content: systemPrompt },
          { role: "user", content: `Create a retro game for platform ${platform} based on: ${prompt}` }
        ],
        temperature: 0.2
      })
    });

    const data = await response.json();
    return data.choices[0].message.content;
  } catch (error) {
    console.error("[API_ERROR] OpenRouter generation failed:", error);
    throw error;
  }
}

// 2. 🎨 TOGETHER AI (FLUX.1 SCHNELL) IMAGE SPRITE GENERATOR
export async function generatePixelSprite(prompt) {
  const apiKey = process.env.TOGETHER_API_KEY;
  if (!apiKey) throw new Error("Missing TOGETHER_API_KEY environment variable");

  try {
    const response = await fetch("https://api.together.xyz/v1/images/generations", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${apiKey}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        model: "black-forest-labs/FLUX.1-schnell",
        prompt: `Classic 16-bit retro video game sprite sheet texture, isolated pixel art on flat dark solid color background, extremely clear outlines: ${prompt}`,
        steps: 4,
        width: 512,
        height: 512,
        response_format: "b64_json"
      })
    });

    const data = await response.json();
    return `data:image/png;base64,${data.data[0].b64_json}`;
  } catch (error) {
    console.error("[API_ERROR] Together AI FLUX Sprite failed:", error);
    throw error;
  }
}

// 3. 🎙️ ELEVENLABS RETRO SOUND SYNTHESIZER
export async function generateRetroSound(text, voiceId = "21m00Tcm4TlvDq8ikWAM") {
  const apiKey = process.env.ELEVENLABS_API_KEY;
  if (!apiKey) throw new Error("Missing ELEVENLABS_API_KEY environment variable");

  try {
    const response = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voiceId}/stream`, {
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

    if (!response.ok) throw new Error(`ElevenLabs returned HTTP ${response.status}`);
    const buffer = await response.arrayBuffer();
    return buffer;
  } catch (error) {
    console.error("[API_ERROR] ElevenLabs sound synthesis failed:", error);
    throw error;
  }
}

// 4. 📁 CLOUDFLARE R2 BUCKET BINARY DIRECT STORAGE UPLOADER
export async function uploadToR2(fileName, dataBuffer, contentType = "application/octet-stream") {
  const bucketUrl = process.env.CLOUDFLARE_R2_BUCKET_URL; // e.g. https://<id>.r2.cloudflarestorage.com/rj-vault-games
  const accessKeyId = process.env.CLOUDFLARE_R2_ACCESS_KEY_ID;
  const secretAccessKey = process.env.CLOUDFLARE_R2_SECRET_ACCESS_KEY;

  if (!bucketUrl || !accessKeyId || !secretAccessKey) {
    throw new Error("Missing Cloudflare R2 credentials in environment variables");
  }

  try {
    // Uses HTTP PUT method directly with bucket url endpoint
    const targetUrl = `${bucketUrl}/${fileName}`;
    const response = await fetch(targetUrl, {
      method: "PUT",
      headers: {
        "Content-Type": contentType,
        "x-amz-content-sha256": "UNSIGNED-PAYLOAD"
      },
      body: dataBuffer
    });

    if (!response.ok) throw new Error(`R2 upload returned HTTP ${response.status}`);
    return targetUrl;
  } catch (error) {
    console.error("[API_ERROR] Cloudflare R2 direct uploader failed:", error);
    throw error;
  }
}
