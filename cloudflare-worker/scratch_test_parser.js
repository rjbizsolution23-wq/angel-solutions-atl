// Advanced parser definition
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
      // Escape regex special chars if any
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

// Test harness
const testMessages = [
  "I’m at a 670 and I have 1 collection.",
  "I have 3 late payments and 635 scores",
  "my score is a 590 and i have 3 medical collections on my report",
  "I need help with my late payments",
  "i have collections and late payments and want a house",
  "I have zero collections but my score is sitting around 580"
];

for (const msg of testMessages) {
  console.log(`--- TEXT: "${msg}" ---`);
  console.log(JSON.stringify(parseCreditProfileFromMessage(msg), null, 2));
}
