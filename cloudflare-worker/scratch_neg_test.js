const norm = "i’m at a 670 and i have 1 collection.";
const negationKeywords = ["no", "never", "none", "don't have", "dont have", "not", "clear", "clean"];

for (const neg of negationKeywords) {
  const index = norm.indexOf(neg);
  if (index !== -1) {
    console.log(`Matched negation keyword "${neg}" at index ${index}. Substring: "${norm.substring(index, index + neg.length + 10)}"`);
  }
}
