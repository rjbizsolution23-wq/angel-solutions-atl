# =====================================================================
# ANGEL SOLUTIONS ATL - DISPUTE TEMPLATES CORPUS (UNCENSORED)
# =====================================================================
# Comprehensive, premium, legal-grade dispute letter templates 
# based on FCRA, HIPAA, and FDCPA consumer protection statutes.
# Deployed for Jordan Miller to retrieve and draft for clients.
# =====================================================================

DISPUTE_TEMPLATES = {
    "round_1_general": {
        "title": "FCRA Section 609 / 611 Round 1 Starter Dispute",
        "description": "General dispute template targeting multiple inaccurate credit accounts, late payments, and collections.",
        "statutes": ["FCRA Section 609", "FCRA Section 611(a)", "15 U.S.C. § 1681g"],
        "content": """[Your Name]
[Your Address]
[Your City, State, ZIP]
[Your Date of Birth]
[Your SSN]

[Date]

[Credit Bureau Name]
[Credit Bureau Address]
[Credit Bureau City, State, ZIP]

Subject: NOTICE OF FCRA VIOLATIONS / REQUEST FOR REMOVAL OF INACCURATE INFORMATION (15 U.S.C. § 1681i)

To Whom It May Concern,

I recently conducted a comprehensive review of my credit report and discovered several critical inaccuracies that are severely damaging my credit standing. Under Section 611 of the Fair Credit Reporting Act (15 U.S.C. § 1681i), I am formally demanding that your agency investigate and immediately delete the following unverified accounts:

1. Account Name: [Account Name] | Account Number: [Account Number]
Reason for Dispute: This account is completely inaccurate. The payment history, balance, and opening date are incorrect. Please verify the physical signed contract or immediately delete this item.

2. Account Name: [Account Name] | Account Number: [Account Number]
Reason for Dispute: I have no record of this account. It is unverified. Under 15 U.S.C. § 1681i, if you cannot verify this item within 30 days, you must legally delete it.

Under FCRA Section 609 (15 U.S.C. § 1681g), I have the right to request full disclosure of all information in my file, including the original source of the data and any documentation bearing my physical signature. If you fail to verify these items with the original creditor using physical documentation, you must delete them immediately.

Please send me an updated copy of my credit report once these changes have been made.

Sincerely,

[Your Name] (Signature)
[Attach copy of Driver's License and Utility Bill for identity verification]"""
    },
    "bankruptcy_deletion": {
        "title": "FCRA Bankruptcy & Public Record Deletion Letter",
        "description": "Disputes bankruptcy listings by challenging the bureau's verification source (LexisNexis / LCI) and the court's reporting accuracy.",
        "statutes": ["FCRA Section 611(a)", "15 U.S.C. § 1681i"],
        "content": """[Your Name]
[Your Address]
[Your City, State, ZIP]
[Your Date of Birth]
[Your SSN]

[Date]

[Credit Bureau Name]
[Credit Bureau Address]
[Credit Bureau City, State, ZIP]

Subject: FORMAL PUBLIC RECORD DISPUTE / BANKRUPTCY INACCURACY (15 U.S.C. § 1681i)

To Whom It May Concern,

I am writing to formally dispute the public record public record bankruptcy filed on my credit profile:

Bankruptcy Case Number: [Bankruptcy Case Number] | Date Filed: [Date Filed]

I contacted the US Bankruptcy Court directly, and they confirmed that they do not report public records or bankruptcies directly to credit bureaus. Therefore, your agency is gathering this information from an unverified, third-party data broker (such as LexisNexis or LCI), which violates the strict accuracy requirements of the Fair Credit Reporting Act.

Under 15 U.S.C. § 1681i(a), I demand to know:
1. The exact name, address, and telephone number of the individual you contacted at the court to verify this information.
2. The physical method of verification used to validate this record.

If you verified this bankruptcy through a third-party intermediary rather than verifying it directly with the court, this item is inaccurate, unverified, and must be permanently deleted from my credit file immediately.

Sincerely,

[Your Name] (Signature)
[Attach copy of Driver's License and Utility Bill for identity verification]"""
    },
    "hipaa_medical_deletion": {
        "title": "HIPAA & FCRA Medical Deletion Letter",
        "description": "Targets medical collections by leveraging HIPAA medical privacy restrictions and the collector's inability to verify clinical details without violations.",
        "statutes": ["HIPAA Privacy Rule", "FCRA Section 611", "15 U.S.C. § 1681i"],
        "content": """[Your Name]
[Your Address]
[Your City, State, ZIP]
[Your Date of Birth]
[Your SSN]

[Date]

[Credit Bureau Name]
[Credit Bureau Address]
[Credit Bureau City, State, ZIP]

Subject: MEDICAL DEBT DISPUTE / HIPAA PRIVACY VIOLATIONS / 15 U.S.C. § 1681i

To Whom It May Concern,

I am writing to dispute a medical collection account on my credit report:

Collection Agency: [Collector Name] | Account Number: [Account Number] | Original Medical Provider: [Medical Provider Name]

Under the Health Insurance Portability and Accountability Act (HIPAA) Privacy Rule, medical providers are strictly prohibited from sharing my private protected health information (PHI) or medical records with any third-party collection agency without my explicit, written consent.

The collection agency currently reporting this account does not possess my medical records, billing records, or doctor's notes, as sharing those documents would be a federal violation of my HIPAA privacy rights. Because they cannot provide full documentation verifying the exact clinical or diagnostic services rendered to substantiate this balance, this debt is completely unverified and legally reporting an unverified debt is an FCRA violation.

Please investigate this matter. If the collection agency cannot verify every diagnostic code and billing item with an authentic, signed HIPAA disclosure from me, this collection must be permanently deleted immediately.

Sincerely,

[Your Name] (Signature)
[Attach copy of Driver's License and Utility Bill for identity verification]"""
    },
    "pay_for_delete": {
        "title": "Pay-For-Delete Settlement Agreement",
        "description": "Negotiation template sent directly to a collection agency offering full or partial payment in exchange for complete deletion of the account.",
        "statutes": ["FDCPA Section 809", "15 U.S.C. § 1692g"],
        "content": """[Your Name]
[Your Address]
[Your City, State, ZIP]

[Date]

[Collection Agency Name]
[Collection Agency Address]
[Collection Agency City, State, ZIP]

Subject: OFFER OF SETTLEMENT IN EXCHANGE FOR COMPLETE DELETION / Account # [Account Number]

To Whom It May Concern,

This letter is in reference to collection account [Account Number] which you are currently reporting under my name. 

Please note that this letter does not constitute an admission of liability or ownership of this debt. However, in an effort to resolve this matter amicably, I am offering a settlement of [Set Settlement Amount, e.g., $150.00] which represents [Set Percentage, e.g., 50%] of the alleged balance.

This offer is strictly contingent upon your agreement to complete the following:
1. Accept the proposed settlement amount as payment in full.
2. Formally request that Equifax, Experian, and TransUnion permanently delete all references, listings, and history regarding this account from my credit reports.
3. Agree never to sell, transfer, or assign this account to any other collection agency or third party.

If you agree to these terms, please sign and return a written confirmation on your company letterhead. Upon receipt of your signed agreement, I will immediately send a cashier's check or money order for the agreed-upon amount.

If you fail to agree to these terms, I will continue to dispute the full validity of this account under the FDCPA.

Sincerely,

[Your Name] (Signature)"""
    },
    "inquiry_removal": {
        "title": "FCRA Unauthorized Inquiry Deletion Letter",
        "description": "Demands removal of hard inquiries that were pulled without explicit written permission or credit transaction purpose.",
        "statutes": ["FCRA Section 604", "15 U.S.C. § 1681b"],
        "content": """[Your Name]
[Your Address]
[Your City, State, ZIP]
[Your Date of Birth]
[Your SSN]

[Date]

[Credit Bureau Name]
[Credit Bureau Address]
[Credit Bureau City, State, ZIP]

Subject: FORMAL DISPUTE OF UNAUTHORIZED CREDIT INQUIRIES (15 U.S.C. § 1681b)

To Whom It May Concern,

I recently examined my credit report and noticed several unauthorized hard credit inquiries on my profile. Under Section 604 of the Fair Credit Reporting Act (15 U.S.C. § 1681b), a credit bureau may only disclose a consumer's credit file under permissible purposes, which requires my explicit written consent or an active credit transaction.

The following hard inquiries were pulled without my knowledge, permission, or a signed application of credit:

1. Creditor Name: [Creditor Name] | Date of Inquiry: [Date of Inquiry]
2. Creditor Name: [Creditor Name] | Date of Inquiry: [Date of Inquiry]

Please provide physical proof of my signature authorizing these specific companies to pull my credit reports. If you cannot produce physical, signed authorization forms for these inquiries within 30 days, your agency must delete them immediately.

Sincerely,

[Your Name] (Signature)
[Attach copy of Driver's License and Utility Bill for identity verification]"""
    },
    "late_payment_goodwill": {
        "title": "Late Payment Goodwill Deletion Request",
        "description": "Friendly goodwill letter sent directly to a creditor asking them to remove a single late payment out of courtesy for a loyal client.",
        "statutes": ["Creditor Goodwill Policy"],
        "content": """[Your Name]
[Your Address]
[Your City, State, ZIP]

[Date]

[Creditor Name]
[Creditor Address]
[Creditor City, State, ZIP]

Subject: GOODWILL CORRECTION REQUEST / Account # [Account Number]

To Whom It May Concern,

I am writing this letter as a loyal customer. I have held an active account with your company since [Account Opening Year] and have always took pride in maintaining a pristine relationship and on-time payments.

Unfortunately, I recently noticed a late payment reported on my credit profile for [Month, Year of Late Payment]. This late payment occurred due to an unexpected [Explain Situation briefly, e.g., medical emergency / system migration issue during relocation]. 

Since that isolated event, my account has been kept entirely current and in excellent standing. Because this single late payment does not represent my actual creditworthiness, and is currently blocking me from securing business financing, I am politely asking if you would make a goodwill gesture and request the credit bureaus to delete this late payment indicator from my profile.

I would be incredibly grateful for your help with this positive adjustment.

Sincerely,

[Your Name] (Signature)"""
    }
}
