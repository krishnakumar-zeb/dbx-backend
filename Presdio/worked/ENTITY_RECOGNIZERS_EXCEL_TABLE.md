# PII Entity Recognizers - Excel Reference Table

## Copy this table directly into Excel (Tab-separated format below)

---

| Entity Name | Tag | Method Used | Regex Patterns | Context Words | Code Snippet |
|-------------|-----|-------------|----------------|---------------|--------------|
| Name | PERSON | NLP-based (spaCy NER) | N/A (uses ML model) | N/A | `analyzer.analyze(text, ["PERSON"], language='en')` |
| Age | AGE | Regex + Context | `\b(?:age[ds]?|years?\s+old)\s*:?\s*(\d{1,3})\b` <br> `\b(\d{1,3})\s*(?:years?\s+old|yrs?\s+old|y\.?o\.?)\b` <br> `\b(\d{1,3})\s*(?:-|to)\s*(\d{1,3})\s*(?:years?\s+old|yrs?\s+old|y\.?o\.?)\b` | age, aged, years old, year old, yrs old, yr old, y.o, birthday, born, dob, date of birth | `recognizer = AgeRecognizer()` <br> `analyzer.registry.add_recognizer(recognizer)` |
| Gender | GENDER | Deny List | N/A (uses word list matching) | gender, sex, identify, identifies as, pronoun, pronouns | `recognizer = GenderRecognizer()` <br> `analyzer.registry.add_recognizer(recognizer)` |
| Ethnicity | ETHNICITY | Deny List (JSON) | N/A (uses word list matching) | ethnicity, ethnic, race, racial, heritage, ancestry, descent, origin, background, nationality | `recognizer = EthnicityRecognizer(ethnicity_json_path="ethnicities.json")` <br> `analyzer.registry.add_recognizer(recognizer)` |
| Phone Number | PHONE_NUMBER | Library (phonenumbers) | N/A (uses phonenumbers library) | phone, number, telephone, cell, cellphone, mobile, call | `analyzer.analyze(text, ["PHONE_NUMBER"], language='en')` |
| Email Address | EMAIL_ADDRESS | Regex + Validation | `\b((([!#$%&'*+\-/=?^_\`{|}~\w])|([!#$%&'*+\-/=?^_\`{|}~\w][!#$%&'*+\-/=?^_\`{|}~\.\w]{0,}[!#$%&'*+\-/=?^_\`{|}~\w]))[@]\w+([-.]\w+)*\.\w+([-.]\w+)*)\b` | email | `analyzer.analyze(text, ["EMAIL_ADDRESS"], language='en')` |
| Location (City/State) | LOCATION | NLP-based (spaCy NER) | N/A (uses ML model) | N/A | `analyzer.analyze(text, ["LOCATION"], language='en')` |
| ZIP Code | ZIP_CODE | Regex + Validation | `\b\d{5}(?:\-\d{4})?\b` | zip, zipcode, zip code, postal, postal code, postcode, mail, mailing | `recognizer = ZipCodeRecognizer()` <br> `analyzer.registry.add_recognizer(recognizer)` |
| Social Security Number | US_SSN | Regex + Validation | `\b([0-9]{5})-([0-9]{4})\b` <br> `\b([0-9]{3})-([0-9]{6})\b` <br> `\b(([0-9]{3})-([0-9]{2})-([0-9]{4}))\b` <br> `\b[0-9]{9}\b` <br> `\b([0-9]{3})[- .]([0-9]{2})[- .]([0-9]{4})\b` | social, security, ssn, ssns, ssid | `analyzer.analyze(text, ["US_SSN"], language='en')` |
| Bank Account Number | US_BANK_NUMBER | Regex + Context | `\b\d{4}-\d{4}-\d{4}\b` <br> `\b[0-9]{8,17}\b` | check, account, account#, acct, bank, save, debit | `analyzer.analyze(text, ["US_BANK_NUMBER"], language='en')` |
| IP Address | IP_ADDRESS | Regex + Validation | IPv4: `\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b` <br> IPv6: (complex pattern for all IPv6 formats) | ip, ipv4, ipv6 | `analyzer.analyze(text, ["IP_ADDRESS"], language='en')` |
| Cookie/Session ID | COOKIE | Regex + Context | `\b(?:session[_\s-]?id|sessionid|sess[_\s-]?id|sessid)\s*[=:]\s*([a-zA-Z0-9\-_]{16,})\b` <br> `\b(?:cookie|token|auth[_\s-]?token|access[_\s-]?token)\s*[=:]\s*([a-zA-Z0-9\-_\.]{16,})\b` <br> `\beyJ[a-zA-Z0-9\-_]+\.eyJ[a-zA-Z0-9\-_]+\.[a-zA-Z0-9\-_]+\b` <br> `\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b` | session, cookie, token, auth, authentication, authorization, bearer, access, refresh, csrf, xsrf, jwt, api key, apikey | `recognizer = CookieRecognizer()` <br> `analyzer.registry.add_recognizer(recognizer)` |
| Certificate/License Number | CERTIFICATE_NUMBER | Regex + Validation | `\b[A-Z]-?\d{8}\b` <br> `\b\d{9}\b` <br> `\b[A-Z]{2,4}-\d{5,7}-[A-Z0-9]{1,3}\b` <br> `\b[A-Z]{2,4}-\d{3,4}-[A-Z0-9]{2,6}-?\d{0,2}\b` <br> `\b[A-Z]{2,4}-\d{4,7}-?[A-Z0-9]?\b` <br> `\b\d{2}-\d{2}-\d{2}-[A-F0-9]{2}-[A-F0-9]{2}-[A-F0-9]{2}-\d{2}-\d{2}\b` <br> `\b[A-Z]{2}-\d{3}-[A-Z]{3}\b` | passport, license, licence, certificate, cert, id, identification, number, policy, medical, driver, pilot, professional, global entry, plate, serial, credential, permit | `recognizer = CertificateRecognizer()` <br> `analyzer.registry.add_recognizer(recognizer)` |

---

## Tab-Separated Format (Copy below for Excel)

```
Entity Name	Tag	Method Used	Regex Patterns	Context Words	Code Snippet
Name	PERSON	NLP-based (spaCy NER)	N/A (uses ML model)	N/A	analyzer.analyze(text, ["PERSON"], language='en')
Age	AGE	Regex + Context	\b(?:age[ds]?|years?\s+old)\s*:?\s*(\d{1,3})\b | \b(\d{1,3})\s*(?:years?\s+old|yrs?\s+old|y\.?o\.?)\b | \b(\d{1,3})\s*(?:-|to)\s*(\d{1,3})\s*(?:years?\s+old|yrs?\s+old|y\.?o\.?)\b	age, aged, years old, year old, yrs old, yr old, y.o, birthday, born, dob, date of birth	recognizer = AgeRecognizer() | analyzer.registry.add_recognizer(recognizer)
Gender	GENDER	Deny List	N/A (uses word list: male, female, non-binary, transgender, etc.)	gender, sex, identify, identifies as, pronoun, pronouns	recognizer = GenderRecognizer() | analyzer.registry.add_recognizer(recognizer)
Ethnicity	ETHNICITY	Deny List (JSON)	N/A (uses 1000+ ethnicity terms from JSON)	ethnicity, ethnic, race, racial, heritage, ancestry, descent, origin, background, nationality	recognizer = EthnicityRecognizer(ethnicity_json_path="ethnicities.json") | analyzer.registry.add_recognizer(recognizer)
Phone Number	PHONE_NUMBER	Library (phonenumbers)	N/A (uses phonenumbers library for validation)	phone, number, telephone, cell, cellphone, mobile, call	analyzer.analyze(text, ["PHONE_NUMBER"], language='en')
Email Address	EMAIL_ADDRESS	Regex + Validation	\b((([!#$%&'*+\-/=?^_`{|}~\w])|([!#$%&'*+\-/=?^_`{|}~\w][!#$%&'*+\-/=?^_`{|}~\.\w]{0,}[!#$%&'*+\-/=?^_`{|}~\w]))[@]\w+([-.]\w+)*\.\w+([-.]\w+)*)\b	email	analyzer.analyze(text, ["EMAIL_ADDRESS"], language='en')
Location (City/State)	LOCATION	NLP-based (spaCy NER)	N/A (uses ML model for GPE and LOC)	N/A	analyzer.analyze(text, ["LOCATION"], language='en')
ZIP Code	ZIP_CODE	Regex + Validation	\b\d{5}(?:\-\d{4})?\b	zip, zipcode, zip code, postal, postal code, postcode, mail, mailing	recognizer = ZipCodeRecognizer() | analyzer.registry.add_recognizer(recognizer)
Social Security Number	US_SSN	Regex + Validation	\b([0-9]{5})-([0-9]{4})\b | \b([0-9]{3})-([0-9]{6})\b | \b(([0-9]{3})-([0-9]{2})-([0-9]{4}))\b | \b[0-9]{9}\b | \b([0-9]{3})[- .]([0-9]{2})[- .]([0-9]{4})\b	social, security, ssn, ssns, ssid	analyzer.analyze(text, ["US_SSN"], language='en')
Bank Account Number	US_BANK_NUMBER	Regex + Context	\b\d{4}-\d{4}-\d{4}\b | \b[0-9]{8,17}\b	check, account, account#, acct, bank, save, debit	analyzer.analyze(text, ["US_BANK_NUMBER"], language='en')
IP Address	IP_ADDRESS	Regex + Validation	IPv4: \b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b | IPv6: (complex pattern)	ip, ipv4, ipv6	analyzer.analyze(text, ["IP_ADDRESS"], language='en')
Cookie/Session ID	COOKIE	Regex + Context	\b(?:session[_\s-]?id|sessionid|sess[_\s-]?id|sessid)\s*[=:]\s*([a-zA-Z0-9\-_]{16,})\b | \b(?:cookie|token|auth[_\s-]?token|access[_\s-]?token)\s*[=:]\s*([a-zA-Z0-9\-_\.]{16,})\b | \beyJ[a-zA-Z0-9\-_]+\.eyJ[a-zA-Z0-9\-_]+\.[a-zA-Z0-9\-_]+\b | \b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b	session, cookie, token, auth, authentication, authorization, bearer, access, refresh, csrf, xsrf, jwt, api key, apikey	recognizer = CookieRecognizer() | analyzer.registry.add_recognizer(recognizer)
Certificate/License Number	CERTIFICATE_NUMBER	Regex + Validation	\b[A-Z]-?\d{8}\b | \b\d{9}\b | \b[A-Z]{2,4}-\d{5,7}-[A-Z0-9]{1,3}\b | \b[A-Z]{2,4}-\d{3,4}-[A-Z0-9]{2,6}-?\d{0,2}\b | \b[A-Z]{2,4}-\d{4,7}-?[A-Z0-9]?\b | \b\d{2}-\d{2}-\d{2}-[A-F0-9]{2}-[A-F0-9]{2}-[A-F0-9]{2}-\d{2}-\d{2}\b | \b[A-Z]{2}-\d{3}-[A-Z]{3}\b	passport, license, licence, certificate, cert, id, identification, number, policy, medical, driver, pilot, professional, global entry, plate, serial, credential, permit	recognizer = CertificateRecognizer() | analyzer.registry.add_recognizer(recognizer)
```

---

## CSV Format (Alternative - easier for Excel import)

Save the content below as a `.csv` file and open in Excel:

```csv
"Entity Name","Tag","Method Used","Regex Patterns","Context Words","Code Snippet"
"Name","PERSON","NLP-based (spaCy NER)","N/A (uses ML model)","N/A","analyzer.analyze(text, [""PERSON""], language='en')"
"Age","AGE","Regex + Context","\b(?:age[ds]?|years?\s+old)\s*:?\s*(\d{1,3})\b | \b(\d{1,3})\s*(?:years?\s+old|yrs?\s+old|y\.?o\.?)\b | \b(\d{1,3})\s*(?:-|to)\s*(\d{1,3})\s*(?:years?\s+old|yrs?\s+old|y\.?o\.?)\b","age, aged, years old, year old, yrs old, yr old, y.o, birthday, born, dob, date of birth","recognizer = AgeRecognizer() | analyzer.registry.add_recognizer(recognizer)"
"Gender","GENDER","Deny List","N/A (uses word list: male, female, non-binary, transgender, etc.)","gender, sex, identify, identifies as, pronoun, pronouns","recognizer = GenderRecognizer() | analyzer.registry.add_recognizer(recognizer)"
"Ethnicity","ETHNICITY","Deny List (JSON)","N/A (uses 1000+ ethnicity terms from JSON)","ethnicity, ethnic, race, racial, heritage, ancestry, descent, origin, background, nationality","recognizer = EthnicityRecognizer(ethnicity_json_path=""ethnicities.json"") | analyzer.registry.add_recognizer(recognizer)"
"Phone Number","PHONE_NUMBER","Library (phonenumbers)","N/A (uses phonenumbers library for validation)","phone, number, telephone, cell, cellphone, mobile, call","analyzer.analyze(text, [""PHONE_NUMBER""], language='en')"
"Email Address","EMAIL_ADDRESS","Regex + Validation","\b((([!#$%&'*+\-/=?^_`{|}~\w])|([!#$%&'*+\-/=?^_`{|}~\w][!#$%&'*+\-/=?^_`{|}~\.\w]{0,}[!#$%&'*+\-/=?^_`{|}~\w]))[@]\w+([-.]\w+)*\.\w+([-.]\w+)*)\b","email","analyzer.analyze(text, [""EMAIL_ADDRESS""], language='en')"
"Location (City/State)","LOCATION","NLP-based (spaCy NER)","N/A (uses ML model for GPE and LOC)","N/A","analyzer.analyze(text, [""LOCATION""], language='en')"
"ZIP Code","ZIP_CODE","Regex + Validation","\b\d{5}(?:\-\d{4})?\b","zip, zipcode, zip code, postal, postal code, postcode, mail, mailing","recognizer = ZipCodeRecognizer() | analyzer.registry.add_recognizer(recognizer)"
"Social Security Number","US_SSN","Regex + Validation","\b([0-9]{5})-([0-9]{4})\b | \b([0-9]{3})-([0-9]{6})\b | \b(([0-9]{3})-([0-9]{2})-([0-9]{4}))\b | \b[0-9]{9}\b | \b([0-9]{3})[- .]([0-9]{2})[- .]([0-9]{4})\b","social, security, ssn, ssns, ssid","analyzer.analyze(text, [""US_SSN""], language='en')"
"Bank Account Number","US_BANK_NUMBER","Regex + Context","\b\d{4}-\d{4}-\d{4}\b | \b[0-9]{8,17}\b","check, account, account#, acct, bank, save, debit","analyzer.analyze(text, [""US_BANK_NUMBER""], language='en')"
"IP Address","IP_ADDRESS","Regex + Validation","IPv4: \b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b | IPv6: (complex pattern)","ip, ipv4, ipv6","analyzer.analyze(text, [""IP_ADDRESS""], language='en')"
"Cookie/Session ID","COOKIE","Regex + Context","\b(?:session[_\s-]?id|sessionid|sess[_\s-]?id|sessid)\s*[=:]\s*([a-zA-Z0-9\-_]{16,})\b | \b(?:cookie|token|auth[_\s-]?token|access[_\s-]?token)\s*[=:]\s*([a-zA-Z0-9\-_\.]{16,})\b | \beyJ[a-zA-Z0-9\-_]+\.eyJ[a-zA-Z0-9\-_]+\.[a-zA-Z0-9\-_]+\b | \b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b","session, cookie, token, auth, authentication, authorization, bearer, access, refresh, csrf, xsrf, jwt, api key, apikey","recognizer = CookieRecognizer() | analyzer.registry.add_recognizer(recognizer)"
"Certificate/License Number","CERTIFICATE_NUMBER","Regex + Validation","\b[A-Z]-?\d{8}\b | \b\d{9}\b | \b[A-Z]{2,4}-\d{5,7}-[A-Z0-9]{1,3}\b | \b[A-Z]{2,4}-\d{3,4}-[A-Z0-9]{2,6}-?\d{0,2}\b | \b[A-Z]{2,4}-\d{4,7}-?[A-Z0-9]?\b | \b\d{2}-\d{2}-\d{2}-[A-F0-9]{2}-[A-F0-9]{2}-[A-F0-9]{2}-\d{2}-\d{2}\b | \b[A-Z]{2}-\d{3}-[A-Z]{3}\b","passport, license, licence, certificate, cert, id, identification, number, policy, medical, driver, pilot, professional, global entry, plate, serial, credential, permit","recognizer = CertificateRecognizer() | analyzer.registry.add_recognizer(recognizer)"
```

---

## Quick Reference - Pattern Examples

| Entity | Example Pattern | Matches |
|--------|----------------|---------|
| AGE | `\b(\d{1,3})\s*years?\s+old\b` | "25 years old", "30 year old" |
| ZIP_CODE | `\b\d{5}(?:\-\d{4})?\b` | "90210", "90210-1234" |
| US_SSN | `\b([0-9]{3})-([0-9]{2})-([0-9]{4})\b` | "123-45-6789" |
| US_BANK_NUMBER | `\b\d{4}-\d{4}-\d{4}\b` | "1234-5678-9012" |
| IP_ADDRESS (IPv4) | `\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.` (repeated 4 times) | "192.168.1.1" |
| COOKIE | `\b(?:session_id)\s*=\s*([a-zA-Z0-9\-_]{16,})\b` | "session_id=abc123..." |
| CERTIFICATE_NUMBER | `\b[A-Z]-?\d{8}\b` | "A-99823411", "M12345678" |

---

## Instructions for Excel Import

### Method 1: Copy-Paste from Markdown Table
1. Select the markdown table above (starting from header row)
2. Copy (Ctrl+C)
3. Paste into Excel (Ctrl+V)
4. Excel will auto-format the table

### Method 2: Use Tab-Separated Format
1. Copy the "Tab-Separated Format" section
2. Paste into Excel
3. Data will automatically align to columns

### Method 3: Import CSV
1. Copy the CSV format section
2. Save as `recognizers.csv`
3. Open in Excel using File > Open
4. Excel will parse the CSV automatically

---

## Column Descriptions

- **Entity Name**: Human-readable name of the PII entity
- **Tag**: XML-style tag used in anonymization (e.g., `<PERSON>`)
- **Method Used**: Detection technique (NLP, Regex, Library, Deny List)
- **Regex Patterns**: Regular expressions used for pattern matching (separated by `|`)
- **Context Words**: Words that boost confidence when found near entity (comma-separated)
- **Code Snippet**: Python code to initialize and use the recognizer
