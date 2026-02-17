# Expected PII Entities Checklist - sample_input.txt

## Document Overview
- **Pages:** 17
- **Primary Subject:** Elena Rodriguez
- **Secondary Subject:** Julian Silva
- **Document Type:** Wealth Management, Financial, Legal, HR, Real Estate

---

## 1. PERSON (Names) - Expected Count: ~15+

### Primary Person:
- [ ] Elena Rodriguez (multiple occurrences)
- [ ] Marcus Thorne
- [ ] Sarah Jenkins
- [ ] Detective Aris Thorne
- [ ] Mark V.

### Secondary Person:
- [ ] Julian Silva (nephew, multiple occurrences)

---

## 2. AGE - Expected Count: 4

- [ ] 62 years old (Elena - multiple mentions)
- [ ] 62 (Elena)
- [ ] 29 years old (Julian)
- [ ] Age: 62 (Elena)

---

## 3. GENDER - Expected Count: 3+

- [ ] Female (Elena - multiple mentions)
- [ ] Gender: Female

---

## 4. ETHNICITY - Expected Count: 4+

- [ ] Hispanic/Latina (Elena - multiple mentions)
- [ ] Ethnicity: Hispanic/Latina

---

## 5. PHONE_NUMBER - Expected Count: 3

- [ ] (206) 555-0198 (Elena's primary)
- [ ] (206) 555-0199 (security officer)
- [ ] (305) 555-0122 (Julian Silva)

---

## 6. EMAIL_ADDRESS - Expected Count: 3+

- [ ] elena.rodriguez.tax@protonmail.com (multiple occurrences)
- [ ] e.rodriguez@skybound-aviation.com

---

## 7. LOCATION - Expected Count: 10+

### Cities:
- [ ] Seattle (multiple occurrences)
- [ ] Miami
- [ ] Florida
- [ ] Washington

### States:
- [ ] Washington (multiple occurrences)
- [ ] WA (multiple occurrences)
- [ ] Florida

---

## 8. ZIP_CODE - Expected Count: 5+

- [ ] 98101 (Seattle - multiple occurrences)
- [ ] 33101 (Miami)

---

## 9. US_SSN (Social Security Numbers) - Expected Count: 3

- [ ] ending in -44-8902 (Elena - partial)
- [ ] 442-88-8902 (Elena - full)
- [ ] 551-00-1234 (Julian Silva)

---

## 10. US_BANK_NUMBER / Account Numbers - Expected Count: 10+

### Bank Accounts:
- [ ] 8829-1102-9930 (old account)
- [ ] 0044-9182-7731 (High-Yield account - multiple mentions)
- [ ] 9910-0023-4412 (Legacy Savings)
- [ ] 1100-9923-4456 (Seattle Credit Union)

### Other Account Numbers:
- [ ] CR-882-991-002 (crypto account)
- [ ] Routing Number: 125000024

---

## 11. IP_ADDRESS - Expected Count: 12+

### IPv4 Addresses:
- [ ] 192.168.1.104 (Elena's home - multiple mentions)
- [ ] 192.168.1.55 (fitness tracker)
- [ ] 72.14.201.11 (session start - multiple mentions)
- [ ] 104.16.44.22 (VPN)
- [ ] 185.22.44.101 (unauthorized - fraud)
- [ ] 103.44.11.22 (suspicious XSS attempt)
- [ ] 45.33.22.11 (crypto login)
- [ ] 172.58.22.109 (airport kiosk)

### IPv6 Addresses:
- [ ] 2001:0db8:85a3:0000:0000:8a2e:0370:7334 (VPN - multiple mentions)

---

## 12. COOKIE / Session IDs - Expected Count: 6+

- [ ] _auth_session_id_772fb
- [ ] _SECURE_AUTH_TOKEN_9921_
- [ ] _UID_SESSION_99
- [ ] _CBP_TRAVEL_ID_88201
- [ ] Cookie-based session (mentioned)

---

## 13. GOVERNMENT IDs / CERTIFICATE NUMBERS - Expected Count: 10+

### Passport:
- [ ] A-99823411 (Elena - multiple mentions)

### Driver's License:
- [ ] WDL-772-BBN-01 (Elena - multiple mentions)

### Pilot's License:
- [ ] FTL-990234-B (Elena - multiple mentions)

### Global Entry:
- [ ] 982230415 (Elena - multiple mentions)

### Medical ID:
- [ ] MED-9920-X

### Group Policy:
- [ ] GRP-44102

### Policy Numbers:
- [ ] LP-88902-11 (Life insurance)
- [ ] POL-9910234-X (Auto insurance)
- [ ] TITL-882-901-B (Title insurance)

### Certificate Serial:
- [ ] 77-88-99-AA-BB-CC-00-11

### Notary License:
- [ ] WA-LIC-44592

### License Plate:
- [ ] WA-882-BBN

---

## 14. BIOMETRIC DATA (Mentioned but not detectable by regex)

- Iris scan hash
- Right-hand thumbprint
- Facial Recognition Hash: SHA-256: e3b0c442...
- Facial recognition hash FA-992-XXXX-01
- BIO-992-SEC-004

---

## Summary of Expected Detections

| Entity Type | Expected Count | Priority |
|-------------|----------------|----------|
| PERSON | 15+ | High |
| AGE | 4 | High |
| GENDER | 3+ | High |
| ETHNICITY | 4+ | High |
| PHONE_NUMBER | 3 | High |
| EMAIL_ADDRESS | 3+ | High |
| LOCATION | 10+ | High |
| ZIP_CODE | 5+ | High |
| US_SSN | 3 | High |
| US_BANK_NUMBER | 10+ | High |
| IP_ADDRESS | 12+ (9 IPv4, 1 IPv6) | High |
| COOKIE | 6+ | High |
| MEDICAL_LICENSE | 2+ | Medium |
| US_DRIVER_LICENSE | 1+ | Medium |
| US_PASSPORT | 1+ | Medium |

---

## Notes for Testing

### Challenges in This Document:
1. **Partial SSN:** "ending in -44-8902" - may not be detected
2. **Multiple formats:** Account numbers with different separators
3. **Context-heavy:** Many entities require context to distinguish from random numbers
4. **Overlapping data:** Same person mentioned multiple times
5. **Secondary person:** Julian Silva's data should also be detected
6. **Technical jargon:** Embedded in business language

### Success Criteria:
- **Minimum 80% detection rate** for high-priority entities
- **No false positives** for non-PII numbers (document IDs, dates, etc.)
- **Proper handling** of multiple occurrences of same entity
- **Context-aware scoring** should boost confidence for entities with context words

---

## Testing Approach

1. Run detection on sample_input.txt
2. Compare detected entities with this checklist
3. Calculate detection rate per entity type
4. Identify missed entities and analyze why
5. Adjust recognizer patterns if needed
6. Re-test and iterate
