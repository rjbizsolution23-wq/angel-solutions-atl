/**
 * =====================================================================
 * ANGEL SOLUTIONS ATL - KEYWORD & COMPLIANCE MATCHING ENGINE
 * =====================================================================
 * High-performance edge parser for categorizing Meta messages/comments
 * and checking strict compliance rules.
 * =====================================================================
 */

/**
 * Normalizes input text for accurate regex matching
 * @param {string} text 
 * @returns {string}
 */
export function normalizeText(text) {
  if (!text) return "";
  return text.toLowerCase().trim().replace(/[\s\t\n]+/g, " ");
}

/**
 * Classifies the main intent of a message based on seed keywords
 * @param {string} text 
 * @returns {string} INTENT TYPE
 */
export function classifyIntent(text) {
  const norm = normalizeText(text);

  const fundingKeywords = [
    "funding", "capital", "business loan", "loan", "secure capital", 
    "business funding", "grant", "lines of credit", "credit line"
  ];
  const taxKeywords = [
    "tax debt", "irs", "tax resolution", "irs relief", "back taxes", 
    "unpaid taxes", "tax lien", "tax audit"
  ];
  const creditKeywords = [
    "credit repair", "fix credit", "dispute", "clear credit", 
    "collections", "credit score", "bankruptcy", "inquiries", "late payments"
  ];
  const onboardingCallKeywords = [
    "call to get started", "need to get on a call to get started", "call before we start"
  ];
  const phoneCallKeywords = [
    "hop on a phone call", "can we hop on a call", "can we talk on the phone", "get on a call", "call you", "phone call"
  ];

  if (onboardingCallKeywords.some(kw => norm.includes(kw))) {
    return "ONBOARDING_CALL_QUESTION";
  }
  if (phoneCallKeywords.some(kw => norm.includes(kw))) {
    return "PHONE_CALL_REQUEST";
  }
  if (fundingKeywords.some(kw => norm.includes(kw))) {
    return "BUSINESS_FUNDING";
  }
  if (taxKeywords.some(kw => norm.includes(kw))) {
    return "TAX_RESOLVE";
  }
  if (creditKeywords.some(kw => norm.includes(kw))) {
    return "CREDIT_REPAIR";
  }

  return "GENERAL_INQUIRY";
}

/**
 * Checks for specific high-priority escalation triggers (compliance issues, manual requests)
 * @param {string} text 
 * @returns {{escalate: boolean, trigger: string|null}}
 */
export function checkEscalationTriggers(text) {
  const norm = normalizeText(text);
  const triggers = [
    "refund", "scam", "lawyer", "attorney", "court", "sue", 
    "lawsuit", "fraud", "speak to human", "speak with a person"
  ];

  for (const trigger of triggers) {
    const regex = new RegExp(`\\b${trigger}\\b`, "i");
    if (regex.test(norm)) {
      return { escalate: true, trigger };
    }
  }

  return { escalate: false, trigger: null };
}

/**
 * Evaluates disqualification criteria based on user message text
 * @param {string} text 
 * @returns {{disqualified: boolean, reason: string|null}}
 */
export function checkDisqualification(text) {
  const norm = normalizeText(text);

  // Check Active Bankruptcy
  if (norm.includes("bankruptcy") && (norm.includes("active") || norm.includes("current") || norm.includes("open") || norm.includes("haven't discharged"))) {
    return { disqualified: true, reason: "Active bankruptcy found" };
  }

  // Check Active Child Support
  if ((norm.includes("child support") || norm.includes("back child support")) && (norm.includes("arrears") || norm.includes("active") || norm.includes("behind") || norm.includes("owe"))) {
    return { disqualified: true, reason: "Active child support arrears found" };
  }

  // Check massive collections
  const collectionsRegex = /(\d+)\s+collections/i;
  const match = norm.match(collectionsRegex);
  if (match) {
    const count = parseInt(match[1], 10);
    if (count >= 10) {
      return { disqualified: true, reason: `Excessive collections count: ${count}` };
    }
  }

  return { disqualified: false, reason: null };
}

/**
 * Scans generated response for compliance issues before live delivery.
 * Banned words: 'credit sweep', 'guarantee', 'guaranteed', 'best', 'yo', 'bet'
 * @param {string} text 
 * @returns {{compliant: boolean, censoredText: string, violation: string|null}}
 */
export function enforceCompliance(text) {
  if (!text) return { compliant: true, censoredText: "", violation: null };
  
  let censoredText = text;
  let compliant = true;
  let violation = null;

  const bannedPhrases = ["credit sweep", "guarantee", "guaranteed", "best", "yo", "bet"];

  for (const phrase of bannedPhrases) {
    const regex = new RegExp(`\\b${phrase}\\b`, "gi");
    if (regex.test(text)) {
      compliant = false;
      violation = phrase;
      // Soft replacement to preserve grammar but ensure total compliance
      let replacement = "[approved services]";
      if (phrase === "guarantee" || phrase === "guaranteed") replacement = "strive for";
      if (phrase === "best") replacement = "premium";
      if (phrase === "yo" || phrase === "bet") replacement = "hello";
      
      censoredText = censoredText.replace(regex, replacement);
    }
  }

  // cleanedText alias kept for callers that expect that key
  return { compliant, censoredText, cleanedText: censoredText, violation };
}

/**
 * Strips URLs from response text that do not match the approved links list
 * Approved links:
 * - https://www.skool.com/creditsolution/about
 * - https://angelsolutionsatl.com/book-online
 * - https://angelsolutionsatl.com
 * - https://share.google/FTVB6seubNwgSVDnd
 * @param {string} text 
 * @returns {string} cleaned response
 */
export function stripUnapprovedLinks(text) {
  if (!text) return "";

  const urlRegex = /(https?:\/\/[^\s]+)/gi;
  const approvedLinks = [
    "https://www.skool.com/creditsolution/about",
    "https://angelsolutionsatl.com/book-online",
    "https://angelsolutionsatl.com",
    "https://share.google/FTVB6seubNwgSVDnd"
  ];

  return text.replace(urlRegex, (url) => {
    // Strip trailing punctuation from URL if grabbed by regex
    const cleanUrl = url.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]+$/, "");
    const isApproved = approvedLinks.some(approved => cleanUrl.toLowerCase().startsWith(approved.toLowerCase()));
    return isApproved ? url : "[link removed for security]";
  });
}

/**
 * Real-time DM Attribute Parser to extract credit score, bankruptcy, child support, and collections count
 * @param {string} text
 * @returns {{score: number|null, bankruptcy: number|null, childSupport: number|null, collectionsCount: number|null}}
 */
export function parseCreditProfileFromMessage(text) {
  if (!text) return { score: null, bankruptcy: null, childSupport: null, collectionsCount: null };
  
  // Normalize text: replace smart curly apostrophes and other symbols to simplify matching
  let norm = text.toLowerCase()
    .replace(/[\u2018\u2019]/g, "'") // replace smart single quotes
    .replace(/[\u201C\u201D]/g, '"') // replace smart double quotes
    .replace(/[\s\t\n]+/g, " ")
    .trim();

  let score = null;
  let bankruptcy = null;
  let childSupport = null;
  let collectionsCount = null;

  // 1. Score extraction (3-digit numbers between 300 and 850)
  // Let's find all 3-digit numbers in the text
  const scoreMatches = [...norm.matchAll(/\b([3-8][0-9]{2})\b/g)];
  if (scoreMatches.length > 0) {
    // If there is a 3-digit number in the credit score range, verify it's likely a score
    for (const match of scoreMatches) {
      const parsedScore = parseInt(match[1], 10);
      
      // Indicators of a score
      const scoreIndicators = [
        "score", "scores", "credit", "fico", "points", "point", "mid", "transunion", "equifax", "experian", 
        "at", "im", "i'm", "i am", "around", "about", "sitting", "standing", "have", "is", "was", "level", "range"
      ];
      
      // Check if any indicator is within 25 characters of the matched score
      const matchIndex = match.index;
      const startSearch = Math.max(0, matchIndex - 25);
      const endSearch = Math.min(norm.length, matchIndex + match[1].length + 25);
      const searchWindow = norm.substring(startSearch, endSearch);
      
      const hasIndicatorNearby = scoreIndicators.some(ind => {
        const regex = new RegExp(`\\b${ind}\\b`, "i");
        return regex.test(searchWindow);
      });

      if (hasIndicatorNearby || scoreMatches.length === 1) {
        score = parsedScore;
        break; // Take the first valid score match
      }
    }
  }

  // Helper function to check negation
  const isTermNegated = (targetTerm) => {
    const negationKeywords = ["no", "never", "none", "don't", "dont", "not", "clear", "clean", "zero", "0"];
    const termIndex = norm.indexOf(targetTerm);
    if (termIndex === -1) return false;
    
    // Check search window of 25 characters before the term
    const startSearch = Math.max(0, termIndex - 25);
    const searchWindow = norm.substring(startSearch, termIndex);
    
    return negationKeywords.some(neg => {
      const regex = new RegExp(`\\b${neg}\\b`, "i");
      return regex.test(searchWindow);
    });
  };

  // 2. Bankruptcy extraction
  const bkTerms = ["bankruptcy", "bankruptcies", " bk ", "bk "];
  const matchedBkTerm = bkTerms.find(term => norm.includes(term));
  if (matchedBkTerm) {
    bankruptcy = isTermNegated(matchedBkTerm) ? 0 : 1;
  }

  // 3. Child Support extraction
  const csTerms = ["child support", "childsupport"];
  const matchedCsTerm = csTerms.find(term => norm.includes(term));
  if (matchedCsTerm) {
    childSupport = isTermNegated(matchedCsTerm) ? 0 : 1;
  }

  // 4. Collections / Negative items count extraction
  const collTerms = ["collection", "collections", "charge off", "charge-off", "chargeoff", "late payment", "late payments", "late"];
  const matchedCollTerm = collTerms.find(term => norm.includes(term));
  
  if (matchedCollTerm) {
    if (isTermNegated(matchedCollTerm)) {
      collectionsCount = 0;
    } else {
      // Find the index of the collections term
      const termIndex = norm.indexOf(matchedCollTerm);
      
      // Look for any number in the entire normalized text and find the one closest to the collections term
      const numberMatches = [...norm.matchAll(/\b(\d+)\b/g)];
      let closestNumber = null;
      let minDistance = Infinity;

      for (const numMatch of numberMatches) {
        const numValue = parseInt(numMatch[1], 10);
        // Exclude the score itself if we found one
        if (score && numValue === score) continue;
        
        // Only consider numbers representing counts (typically < 100)
        if (numValue < 100) {
          const numIndex = numMatch.index;
          const distance = Math.abs(numIndex - termIndex);
          if (distance < minDistance) {
            minDistance = distance;
            closestNumber = numValue;
          }
        }
      }

      // If we found a close number (within 30 characters), use it. Otherwise default to 1.
      if (closestNumber !== null && minDistance < 30) {
        collectionsCount = closestNumber;
      } else {
        collectionsCount = 1; // default if term is mentioned and not negated
      }
    }
  }

  return { score, bankruptcy, childSupport, collectionsCount };
}

/**
 * Detects offensive, abusive, profane, or highly disrespectful language.
 * @param {string} text
 * @returns {{detected: boolean, pattern: string|null}}
 */
export function hasOffensiveOrDisrespectfulLanguage(text) {
  const norm = normalizeText(text);

  // Broad list of profanities, disrespectful terms, and abusive language
  const offensivePatterns = [
    // Standard profanity / slurs
    "\\bfuck(ing|er|ed|s)?\\b",
    "\\bshit(ty|head|s)?\\b",
    "\\bbitch(es)?\\b",
    "\\basshole(s)?\\b",
    "\\bcunt(s)?\\b",
    "\\bdick(head|s)?\\b",
    "\\bpussy\\b",
    "\\bbastard(s)?\\b",
    "\\bwhore(s)?\\b",
    "\\bslut(s)?\\b",
    "\\bcrap\\b",
    
    // Abusive/disrespectful phrases
    "\\bf\\s*u\\s*c\\s*k\\b",
    "\\bshut\\s*up\\b",
    "\\bgo\\s*to\\s*hell\\b",
    "\\bpiece\\s*of\\s*shit\\b",
    "\\bbullshit\\b",
    "\\blying\\s*ass\\b",
    "\\bscrew\\s*you\\b",
    "\\bkiss\\s*my\\s*ass\\b",
    "\\bgo\\s*fuck\\b",
    "\\bget\\s*lost\\b",
    "\\btrash\\b",
    "\\bgarbage\\b",
    
    // Highly defensive/insulting terms
    "\\bstupid\\b",
    "\\bidiot(s)?\\b",
    "\\bdumb\\b",
    "\\bclown(s)?\\b",
    "\\bmoron(s)?\\b",
    "\\bjackass(es)?\\b",
    "\\bscammer(s)?\\b",
    "\\bfraud(s)?\\b",
    "\\bcrook(s)?\\b"
  ];

  for (const pattern of offensivePatterns) {
    const regex = new RegExp(pattern, "i");
    if (regex.test(norm)) {
      return { detected: true, pattern };
    }
  }

  return { detected: false, pattern: null };
}

/**
 * Detects if the client explicitly requests to stop/pause the bot or opt-out.
 * @param {string} text
 * @returns {{requested: boolean, trigger: string|null}}
 */
export function checkClientStopRequest(text) {
  const norm = normalizeText(text);
  const stopTriggers = [
    "stop", "stop bot", "pause bot", "pause the bot", "opt out", "opt-out", 
    "unsubscribe", "stop texting", "stop messaging", "leave me alone", 
    "no more messages", "don't message", "dont message", "stop sending"
  ];

  for (const trigger of stopTriggers) {
    const regex = new RegExp(`\\b${trigger}\\b`, "i");
    if (regex.test(norm)) {
      return { requested: true, trigger };
    }
  }

  return { requested: false, trigger: null };
}
