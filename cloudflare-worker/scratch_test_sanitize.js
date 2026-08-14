// Let's test different sanitizeAiReply implementations

function sanitizeAiReply(raw) {
  if (!raw) return null;
  let t = String(raw).trim();
  
  // 1. Strip out deep-thinking tags and code blocks
  t = t.replace(/<think>[\s\S]*?<\/think>/gi, "").trim();
  t = t.replace(/```[\s\S]*?```/g, "").trim();

  // 2. Strip out common AI meta-prefixes/conversation intros on the same line
  t = t.replace(/^(looking back at the history|the user has|the user is|since the user|as an ai|as jordynn)[\s\S]*?(i will (respond|reply|say)( with)?|here is (my|the) response|response):?\s*/i, "").trim();
  t = t.replace(/^(okay|sure),?\s+the user[\s\S]*?(i will (respond|reply|say)( with)?|here is (my|the) response|response):?\s*/i, "").trim();

  // 3. If the model wrapped the ENTIRE remaining response in quotes (e.g. "Hello!"), strip the outer quotes
  if ((t.startsWith('"') && t.endsWith('"')) || (t.startsWith('“') && t.endsWith('”'))) {
    t = t.substring(1, t.length - 1).trim();
  }

  // 4. Strip out other prefixes
  const prefixes = [
    /^As Jordynn Miller:?\s*/i,
    /^As Jordynn:?\s*/i,
    /^Jordynn:\s*/i,
    /^Jordynn Miller:\s*/i,
    /^Response:\s*/i,
    /^Here is (the|my) response:?\s*/i,
    /^Sure,?\s+here is\s+a\s+response:?\s*/i,
    /^Draft:\s*/i,
    /^Instagram DM:\s*/i,
    /^DM:\s*/i
  ];
  for (const p of prefixes) {
    t = t.replace(p, "").trim();
  }

  // 5. If the model still has quotes but has text outside of it, check if we should extract the quotes.
  // We only do this if there's an obvious meta-intro left.
  const hasMetaIntro = /^(okay|sure|i need to|we need to|let me|according to|looking back)/i.test(t);
  if (hasMetaIntro) {
    const quotes = [...t.matchAll(/["“]([^"”]{10,220})["”]/g)].map(m => m[1].trim());
    if (quotes.length) {
      return quotes[quotes.length - 1];
    }
  }

  // 6. Clean up headers and bullet lists
  t = t.replace(/^#{1,6}\s+/gm, "").replace(/^\s*[-*]\s+/gm, "").trim();
  
  // 7. Cap length for IG DMs
  if (t.length > 450) {
    t = t.slice(0, 447).trim() + "…";
  }

  // 8. Sentence limiter: Keep at most 3 sentences for natural IG DM texting
  const parts = t.split(/(?<=[.!?])\s+/).filter(Boolean);
  if (parts.length > 3) {
    t = parts.slice(0, 3).join(" ");
  }

  if (!t || t.length < 5) return null;
  return t;
}

// Test cases representing different real-world outputs from cheap or verbose models
const testCases = [
  {
    name: "Clean human-like output",
    input: "Hey! Buying a house this year is super practical once we clean up those collections. What credit score are we starting with right now?"
  },
  {
    name: "Output with thinking tags",
    input: "<think>The user has 2 collections and wants to buy a house. I must explain that we can help but need their credit score.</think>I can definitely help with that! Since you're trying to buy a house, we want to move quickly. What is your credit score sitting at right now?"
  },
  {
    name: "Model wrapping entire response in double quotes",
    input: "\"Yes, buying a house is absolutely possible if we work together to dispute those collections. What's your credit score sitting at right now?\""
  },
  {
    name: "Model starting with Jordynn prefix",
    input: "As Jordynn Miller: I can absolutely help you get those collections cleared. What is your credit score sitting at right now?"
  },
  {
    name: "Model showing system thinking and then response in quotes",
    input: "Okay, the user wants to buy a house and has collections. We must explain our service. I will reply: \"Hey there! That's definitely practical if we work together. What is your credit score sitting at?\""
  },
  {
    name: "Model with aggressive 'must be' phrase that would be trashed by old parser",
    input: "Buying a home must be such an exciting milestone for you! Let's get those collections taken care of. What's your score looking like right now?"
  },
  {
    name: "Stiff AI conversational transition at start, then actual message",
    input: "Looking back at the history, the user mentioned collections. I will respond with: Hey, I can help you with those 2 collections. What's your credit score sitting at?"
  }
];

console.log("=== RUNNING PARSER SANITIZATION TESTS ===\n");
for (const tc of testCases) {
  console.log(`Test: [${tc.name}]`);
  console.log(`Input: ${JSON.stringify(tc.input)}`);
  const output = sanitizeAiReply(tc.input);
  console.log(`Output: ${JSON.stringify(output)}`);
  console.log("------------------------------------------\n");
}
