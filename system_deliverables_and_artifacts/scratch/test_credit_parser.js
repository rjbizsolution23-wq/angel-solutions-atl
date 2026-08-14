import { parseCreditProfileFromMessage } from "../../../../../Downloads/_ORGANIZED_DOWNLOADS/Uncategorized/angel-solutions-complete-system/cloudflare-worker/src/keyword-engine.js";

const testCases = [
  {
    text: "I have a 620 credit score with 3 collections and a bankruptcy from 2021",
    expected: { score: 620, bankruptcy: 1, childSupport: null, collectionsCount: 3 }
  },
  {
    text: "hey my score is 710, no bankruptcies or child support, clear file",
    expected: { score: 710, bankruptcy: 0, childSupport: 0, collectionsCount: null }
  },
  {
    text: "I have some collections but no bankruptcy",
    expected: { score: null, bankruptcy: 0, childSupport: null, collectionsCount: 1 }
  },
  {
    text: "my fico score is 580 and I have no collections",
    expected: { score: 580, bankruptcy: null, childSupport: null, collectionsCount: 0 }
  },
  {
    text: "I have 0 collections, score is 685, no child support",
    expected: { score: 685, bankruptcy: null, childSupport: 0, collectionsCount: 0 }
  }
];

let failed = 0;
console.log("=== RUNNING CREDIT PROFILE PARSER TESTS ===");
for (let i = 0; i < testCases.length; i++) {
  const tc = testCases[i];
  const res = parseCreditProfileFromMessage(tc.text);
  let ok = true;
  for (const key of Object.keys(tc.expected)) {
    if (res[key] !== tc.expected[key]) {
      ok = false;
      break;
    }
  }
  if (ok) {
    console.log(`✅ TEST CASE ${i + 1} PASSED: "${tc.text}"`);
    console.log(`   Result:`, res);
  } else {
    failed++;
    console.log(`❌ TEST CASE ${i + 1} FAILED: "${tc.text}"`);
    console.log(`   Expected:`, tc.expected);
    console.log(`   Got:     `, res);
  }
}

if (failed === 0) {
  console.log("\n🎉 ALL TESTS PASSED SUCCESSFULLY!");
} else {
  console.log(`\n🚨 ${failed} TESTS FAILED!`);
  process.exit(1);
}
