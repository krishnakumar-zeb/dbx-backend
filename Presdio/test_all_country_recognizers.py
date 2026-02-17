"""
Comprehensive test for all country-specific PII recognizers.
Tests each new recognizer individually with realistic sample data,
then runs a full integration test per country using AnalyzerEngine.

Usage: python test_all_country_recognizers.py
"""

import sys
sys.path.insert(0, 'presidio-main/presidio-analyzer')

from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.predefined_recognizers import (
    # Canada
    CaPostalCodeRecognizer,
    CaSinRecognizer,
    CaBankRecognizer,
    CaDriverLicenseRecognizer,
    CaGstRecognizer,
    # Mexico
    MxCurpRecognizer,
    MxClabeRecognizer,
    MxPostalCodeRecognizer,
    MxRfcRecognizer,
    MxDriverLicenseRecognizer,
    # UK (new)
    UkPostcodeRecognizer,
    UkSortCodeRecognizer,
    UkDriverLicenseRecognizer,
    UkUtrRecognizer,
    # Germany
    DePostalCodeRecognizer,
    DePensionInsuranceRecognizer,
    DeDriverLicenseRecognizer,
    DeTaxNumberRecognizer,
    # France
    FrPostalCodeRecognizer,
    FrInseeRecognizer,
    FrDriverLicenseRecognizer,
    FrSpiRecognizer,
    # Saudi Arabia
    SaNationalIdRecognizer,
    SaPostalCodeRecognizer,
    SaTinRecognizer,
    # UAE
    AeEmiratesIdRecognizer,
    AePostalCodeRecognizer,
    AeDriverLicenseRecognizer,
    AeTrnRecognizer,
    # South Africa
    ZaIdRecognizer,
    ZaPostalCodeRecognizer,
    ZaDriverLicenseRecognizer,
    ZaTaxNumberRecognizer,
    # Japan
    JpPostalCodeRecognizer,
    JpMyNumberRecognizer,
    JpBankRecognizer,
    JpDriverLicenseRecognizer,
    JpCorporateNumberRecognizer,
    # India (new)
    InPinCodeRecognizer,
    InDriverLicenseRecognizer,
    InIfscRecognizer,
    # Australia (new)
    AuPostcodeRecognizer,
    AuBsbRecognizer,
    AuDriverLicenseRecognizer,
    # Singapore (new)
    SgPostalCodeRecognizer,
    SgPassportRecognizer,
    SgBankRecognizer,
    # Malaysia
    MyNricRecognizer,
    MyPostalCodeRecognizer,
    MyBankRecognizer,
    MyIncomeTaxRecognizer,
)


# ============================================================
# Tracking
# ============================================================
total_pass = 0
total_fail = 0


def check(recognizer, text, entity, expect_detect=True, min_results=1):
    """
    Run a single recognizer against text and verify detection.
    Returns (passed: bool, details: str).
    """
    global total_pass, total_fail
    results = recognizer.analyze(text, [entity])
    detected = len(results) >= min_results

    if detected == expect_detect:
        total_pass += 1
        icon = "✓"
    else:
        total_fail += 1
        icon = "✗"

    if results and expect_detect:
        for r in results:
            found = text[r.start:r.end]
            print(f"  {icon} '{text}'  →  Detected: '{found}' (score: {r.score:.2f})")
    elif not results and not expect_detect:
        print(f"  {icon} '{text}'  →  Correctly not detected")
    elif not results and expect_detect:
        print(f"  {icon} '{text}'  →  MISSED (expected detection)")
    else:
        found = text[results[0].start:results[0].end]
        print(f"  {icon} '{text}'  →  FALSE POSITIVE: '{found}' (expected no detection)")


# ============================================================
# CANADA
# ============================================================
def test_canada():
    print("\n" + "=" * 70)
    print("CANADA")
    print("=" * 70)

    # --- Postal Code ---
    print("\n--- CA Postal Code ---")
    rec = CaPostalCodeRecognizer()
    check(rec, "Address: Ottawa, ON K1A 0B1", "CA_POSTAL_CODE")
    check(rec, "Ship to V6B 3K9 Vancouver", "CA_POSTAL_CODE")
    check(rec, "Toronto M5V2T6 office", "CA_POSTAL_CODE")
    check(rec, "US ZIP 90210", "CA_POSTAL_CODE", expect_detect=False)
    check(rec, "Invalid D1A 0B1 code", "CA_POSTAL_CODE", expect_detect=False)

    # --- SIN ---
    print("\n--- CA Social Insurance Number ---")
    rec = CaSinRecognizer()
    check(rec, "SIN: 130-692-544", "CA_SIN")
    check(rec, "Social insurance number 972 487 086", "CA_SIN")
    check(rec, "Phone: 555-1234", "CA_SIN", expect_detect=False)

    # --- Bank Transit ---
    print("\n--- CA Bank Transit/Institution ---")
    rec = CaBankRecognizer()
    check(rec, "Transit: 12345-001", "CA_BANK_NUMBER")
    check(rec, "Bank routing 99999-123", "CA_BANK_NUMBER")
    check(rec, "Account 012345678", "CA_BANK_NUMBER")  # electronic format

    # --- Driver License ---
    print("\n--- CA Driver License ---")
    rec = CaDriverLicenseRecognizer()
    check(rec, "Ontario DL: A1234-56789-01234", "CA_DRIVER_LICENSE")
    check(rec, "Quebec licence B123456789012", "CA_DRIVER_LICENSE")  # 1 letter + 12 digits (Quebec)

    # --- GST/HST ---
    print("\n--- CA GST/HST Number ---")
    rec = CaGstRecognizer()
    check(rec, "GST number 123456789RT0001", "CA_GST_NUMBER")
    check(rec, "BN: 987654321RT1234", "CA_GST_NUMBER")
    check(rec, "Random 12345678RT001", "CA_GST_NUMBER", expect_detect=False)


# ============================================================
# MEXICO
# ============================================================
def test_mexico():
    print("\n" + "=" * 70)
    print("MEXICO")
    print("=" * 70)

    # --- CURP ---
    print("\n--- MX CURP ---")
    rec = MxCurpRecognizer()
    check(rec, "CURP: GARC850101HDFRRL09", "MX_CURP")
    check(rec, "Identificacion LOPM900215MDFRRN01", "MX_CURP")
    check(rec, "Invalid: garc850101hdfrrl09", "MX_CURP", expect_detect=False)

    # --- CLABE ---
    print("\n--- MX CLABE ---")
    rec = MxClabeRecognizer()
    check(rec, "CLABE: 012345678901234567", "MX_CLABE")
    check(rec, "Transfer to 002115016003269411", "MX_CLABE")
    check(rec, "Short 1234567890", "MX_CLABE", expect_detect=False)

    # --- Postal Code ---
    print("\n--- MX Postal Code ---")
    rec = MxPostalCodeRecognizer()
    check(rec, "C.P. 06600 Mexico City", "MX_POSTAL_CODE")
    check(rec, "Codigo postal 64000 Monterrey", "MX_POSTAL_CODE")
    check(rec, "CP 00100", "MX_POSTAL_CODE", expect_detect=False)  # too low

    # --- RFC ---
    print("\n--- MX RFC ---")
    rec = MxRfcRecognizer()
    check(rec, "RFC: GARC850101AB1", "MX_RFC")
    check(rec, "Fiscal LOPM900215XY2", "MX_RFC")
    check(rec, "Business RFC: ABC060101XY3", "MX_RFC")  # 3-letter business

    # --- Driver License ---
    print("\n--- MX Driver License ---")
    rec = MxDriverLicenseRecognizer()
    check(rec, "Licencia de conducir: ABC1234567", "MX_DRIVER_LICENSE")


# ============================================================
# UK
# ============================================================
def test_uk():
    print("\n" + "=" * 70)
    print("UNITED KINGDOM")
    print("=" * 70)

    # --- Postcode ---
    print("\n--- UK Postcode ---")
    rec = UkPostcodeRecognizer()
    check(rec, "Address: London SW1A 1AA", "UK_POSTCODE")
    check(rec, "Office at EC1A 1BB", "UK_POSTCODE")
    check(rec, "BBC W1A 0AX", "UK_POSTCODE")
    check(rec, "Manchester M1 1AE", "UK_POSTCODE")
    check(rec, "Birmingham B33 8TH", "UK_POSTCODE")

    # --- Sort Code ---
    print("\n--- UK Sort Code ---")
    rec = UkSortCodeRecognizer()
    check(rec, "Sort code: 12-34-56", "UK_SORT_CODE")
    check(rec, "Bank sort code 20 00 00", "UK_SORT_CODE")
    check(rec, "Code 123456", "UK_SORT_CODE", expect_detect=False)

    # --- Driver License ---
    print("\n--- UK Driving Licence ---")
    rec = UkDriverLicenseRecognizer()
    check(rec, "DVLA licence: SMITH901019JA9AA", "UK_DRIVER_LICENSE")

    # --- UTR / PAYE ---
    print("\n--- UK UTR / PAYE ---")
    rec = UkUtrRecognizer()
    check(rec, "PAYE reference: 123/AB12345", "UK_UTR")
    check(rec, "HMRC PAYE 456/XY789", "UK_UTR")
    check(rec, "UTR: 1234567890", "UK_UTR")


# ============================================================
# GERMANY
# ============================================================
def test_germany():
    print("\n" + "=" * 70)
    print("GERMANY")
    print("=" * 70)

    # --- Postal Code ---
    print("\n--- DE Postal Code ---")
    rec = DePostalCodeRecognizer()
    check(rec, "PLZ 10115 Berlin", "DE_POSTAL_CODE")
    check(rec, "Postleitzahl 80331 Munchen", "DE_POSTAL_CODE")
    check(rec, "Address 01067 Dresden", "DE_POSTAL_CODE")
    check(rec, "Invalid 00100", "DE_POSTAL_CODE", expect_detect=False)

    # --- Pension Insurance ---
    print("\n--- DE Pension Insurance Number ---")
    rec = DePensionInsuranceRecognizer()
    check(rec, "Rentenversicherung: 12010180A123", "DE_PENSION_INSURANCE")
    check(rec, "RVNR 65150690B456", "DE_PENSION_INSURANCE")

    # --- Driver License ---
    print("\n--- DE Driver License ---")
    rec = DeDriverLicenseRecognizer()
    check(rec, "Fuhrerschein B072RRE2E10", "DE_DRIVER_LICENSE")

    # --- Tax Number ---
    print("\n--- DE Tax Number ---")
    rec = DeTaxNumberRecognizer()
    check(rec, "Steuernummer: 11/123/12345", "DE_TAX_NUMBER")
    check(rec, "Tax number 111/456/67890", "DE_TAX_NUMBER")
    check(rec, "Invalid 1/123/12345", "DE_TAX_NUMBER", expect_detect=False)


# ============================================================
# FRANCE
# ============================================================
def test_france():
    print("\n" + "=" * 70)
    print("FRANCE")
    print("=" * 70)

    # --- Postal Code ---
    print("\n--- FR Postal Code ---")
    rec = FrPostalCodeRecognizer()
    check(rec, "Code postal 75001 Paris", "FR_POSTAL_CODE")
    check(rec, "Adresse 13001 Marseille", "FR_POSTAL_CODE")
    check(rec, "Cedex 69001 Lyon", "FR_POSTAL_CODE")

    # --- INSEE ---
    print("\n--- FR INSEE Number ---")
    rec = FrInseeRecognizer()
    check(rec, "INSEE: 185073512345678", "FR_INSEE")
    check(rec, "Securite sociale 285073512345678", "FR_INSEE")
    check(rec, "Invalid 385073512345678", "FR_INSEE", expect_detect=False)

    # --- SPI ---
    print("\n--- FR SPI Tax Number ---")
    rec = FrSpiRecognizer()
    check(rec, "Numero fiscal: 12 34 567 890 123", "FR_SPI")
    check(rec, "SPI 99 88 777 666 555", "FR_SPI")

    # --- Driver License ---
    print("\n--- FR Driver License ---")
    rec = FrDriverLicenseRecognizer()
    check(rec, "Permis de conduire: 12AB12345", "FR_DRIVER_LICENSE")  # old format
    check(rec, "Permis 123456789012", "FR_DRIVER_LICENSE")  # modern 12-digit


# ============================================================
# SAUDI ARABIA
# ============================================================
def test_saudi():
    print("\n" + "=" * 70)
    print("SAUDI ARABIA")
    print("=" * 70)

    # --- National ID ---
    print("\n--- SA National ID ---")
    rec = SaNationalIdRecognizer()
    check(rec, "National ID: 1234567890", "SA_NATIONAL_ID")
    check(rec, "Saudi ID 1098765432", "SA_NATIONAL_ID")
    check(rec, "Not a Saudi ID 3234567890", "SA_NATIONAL_ID", expect_detect=False)

    # --- Iqama ---
    print("\n--- SA Iqama ---")
    check(rec, "Iqama number: 2234567890", "SA_NATIONAL_ID")
    check(rec, "Resident ID 2098765432", "SA_NATIONAL_ID")

    # --- Postal Code ---
    print("\n--- SA Postal Code ---")
    rec = SaPostalCodeRecognizer()
    check(rec, "Postal code 12345 Riyadh", "SA_POSTAL_CODE")
    check(rec, "Address 23456-7890 Jeddah", "SA_POSTAL_CODE")

    # --- TIN/VAT ---
    print("\n--- SA TIN / VAT ID ---")
    rec = SaTinRecognizer()
    check(rec, "VAT: 300012345678901", "SA_TIN")
    check(rec, "TIN 312345678901234", "SA_TIN")
    check(rec, "Invalid 200012345678901", "SA_TIN", expect_detect=False)


# ============================================================
# UAE
# ============================================================
def test_uae():
    print("\n" + "=" * 70)
    print("UAE")
    print("=" * 70)

    # --- Emirates ID ---
    print("\n--- AE Emirates ID ---")
    rec = AeEmiratesIdRecognizer()
    check(rec, "Emirates ID: 784-1992-1234567-8", "AE_EMIRATES_ID")
    check(rec, "UAE ID 784-2000-9876543-1", "AE_EMIRATES_ID")
    check(rec, "Invalid 785-1992-1234567-8", "AE_EMIRATES_ID", expect_detect=False)

    # --- P.O. Box / Makani ---
    print("\n--- AE P.O. Box / Makani ---")
    rec = AePostalCodeRecognizer()
    check(rec, "P.O. Box 4567 Dubai", "AE_POSTAL_CODE")
    check(rec, "PO Box 123456 Abu Dhabi", "AE_POSTAL_CODE")
    check(rec, "Makani: 30032 95320", "AE_POSTAL_CODE")

    # --- TRN ---
    print("\n--- AE TRN ---")
    rec = AeTrnRecognizer()
    check(rec, "TRN: 100123456789012", "AE_TRN")
    check(rec, "Tax registration 100000000000001", "AE_TRN")
    check(rec, "Invalid 200123456789012", "AE_TRN", expect_detect=False)

    # --- Driver License ---
    print("\n--- AE Driver License ---")
    rec = AeDriverLicenseRecognizer()
    check(rec, "RTA driving license: 1234567", "AE_DRIVER_LICENSE")
    check(rec, "License number 123456789", "AE_DRIVER_LICENSE")


# ============================================================
# SOUTH AFRICA
# ============================================================
def test_south_africa():
    print("\n" + "=" * 70)
    print("SOUTH AFRICA")
    print("=" * 70)

    # --- ID Number ---
    print("\n--- ZA ID Number ---")
    rec = ZaIdRecognizer()
    check(rec, "SA ID: 9001015009087", "ZA_ID_NUMBER")
    check(rec, "Identity number 8502155001080", "ZA_ID_NUMBER")

    # --- Postal Code ---
    print("\n--- ZA Postal Code ---")
    rec = ZaPostalCodeRecognizer()
    check(rec, "Postal code 0001 Pretoria", "ZA_POSTAL_CODE")
    check(rec, "Address 8001 Cape Town", "ZA_POSTAL_CODE")

    # --- Tax Number ---
    print("\n--- ZA Tax Number ---")
    rec = ZaTaxNumberRecognizer()
    check(rec, "SARS tax number: 0123456789", "ZA_TAX_NUMBER")
    check(rec, "Tax 9876543210", "ZA_TAX_NUMBER")
    check(rec, "VAT number 4123456789", "ZA_TAX_NUMBER")
    check(rec, "Invalid 5123456789", "ZA_TAX_NUMBER", expect_detect=False)

    # --- Driver License ---
    print("\n--- ZA Driver License ---")
    rec = ZaDriverLicenseRecognizer()
    check(rec, "Driver licence: AB12CD34EF56", "ZA_DRIVER_LICENSE")


# ============================================================
# JAPAN
# ============================================================
def test_japan():
    print("\n" + "=" * 70)
    print("JAPAN")
    print("=" * 70)

    # --- Postal Code ---
    print("\n--- JP Postal Code ---")
    rec = JpPostalCodeRecognizer()
    check(rec, "Postal code 100-0001 Tokyo", "JP_POSTAL_CODE")
    check(rec, "Address 530-0001 Osaka", "JP_POSTAL_CODE")
    check(rec, "Invalid 1000001", "JP_POSTAL_CODE", expect_detect=False)

    # --- My Number ---
    print("\n--- JP My Number ---")
    rec = JpMyNumberRecognizer()
    check(rec, "My Number: 1234-5678-9012", "JP_MY_NUMBER")
    check(rec, "Individual number 1234 5678 9012", "JP_MY_NUMBER")
    check(rec, "No separators 123456789012", "JP_MY_NUMBER")  # continuous (weak)

    # --- Bank Zengin ---
    print("\n--- JP Bank Number (Zengin) ---")
    rec = JpBankRecognizer()
    check(rec, "Bank code: 0001-001", "JP_BANK_NUMBER")
    check(rec, "Branch 9999-999", "JP_BANK_NUMBER")

    # --- Driver License ---
    print("\n--- JP Driver License ---")
    rec = JpDriverLicenseRecognizer()
    check(rec, "License number: 123456789012", "JP_DRIVER_LICENSE")

    # --- Corporate Number ---
    print("\n--- JP Corporate Number ---")
    rec = JpCorporateNumberRecognizer()
    check(rec, "Corporate number: 1234567890123", "JP_CORPORATE_NUMBER")
    check(rec, "Short 123456789012", "JP_CORPORATE_NUMBER", expect_detect=False)


# ============================================================
# INDIA (new recognizers)
# ============================================================
def test_india_new():
    print("\n" + "=" * 70)
    print("INDIA (new recognizers)")
    print("=" * 70)

    # --- PIN Code ---
    print("\n--- IN PIN Code ---")
    rec = InPinCodeRecognizer()
    check(rec, "PIN code: 110 001 New Delhi", "IN_PIN_CODE")
    check(rec, "Pincode 400001 Mumbai", "IN_PIN_CODE")
    check(rec, "Address 560001 Bangalore", "IN_PIN_CODE")
    check(rec, "Invalid 010001", "IN_PIN_CODE", expect_detect=False)

    # --- IFSC ---
    print("\n--- IN IFSC Code ---")
    rec = InIfscRecognizer()
    check(rec, "IFSC: SBIN0001234", "IN_IFSC")
    check(rec, "Bank IFSC HDFC0000001", "IN_IFSC")
    check(rec, "NEFT transfer ICIC0002345", "IN_IFSC")
    check(rec, "Invalid sbin0001234", "IN_IFSC", expect_detect=False)

    # --- Driver License ---
    print("\n--- IN Driver License ---")
    rec = InDriverLicenseRecognizer()
    check(rec, "DL: KA0120120000001", "IN_DRIVER_LICENSE")
    check(rec, "Driving licence MH0220150000001", "IN_DRIVER_LICENSE")


# ============================================================
# AUSTRALIA (new recognizers)
# ============================================================
def test_australia_new():
    print("\n" + "=" * 70)
    print("AUSTRALIA (new recognizers)")
    print("=" * 70)

    # --- Postcode ---
    print("\n--- AU Postcode ---")
    rec = AuPostcodeRecognizer()
    check(rec, "Postcode 2000 Sydney NSW", "AU_POSTCODE")
    check(rec, "Address 3000 Melbourne VIC", "AU_POSTCODE")
    check(rec, "Darwin 0800 NT", "AU_POSTCODE")
    check(rec, "Invalid 8000", "AU_POSTCODE", expect_detect=False)

    # --- BSB ---
    print("\n--- AU BSB ---")
    rec = AuBsbRecognizer()
    check(rec, "BSB: 062-000 Commonwealth Bank", "AU_BSB")
    check(rec, "Bank BSB 033 000 Westpac", "AU_BSB")

    # --- Driver Licence ---
    print("\n--- AU Driver Licence ---")
    rec = AuDriverLicenseRecognizer()
    check(rec, "Driver licence number: 12345678", "AU_DRIVER_LICENSE")
    check(rec, "NSW licence 123456789", "AU_DRIVER_LICENSE")


# ============================================================
# SINGAPORE (new recognizers)
# ============================================================
def test_singapore_new():
    print("\n" + "=" * 70)
    print("SINGAPORE (new recognizers)")
    print("=" * 70)

    # --- Postal Code ---
    print("\n--- SG Postal Code ---")
    rec = SgPostalCodeRecognizer()
    check(rec, "Singapore postal code 018956", "SG_POSTAL_CODE")
    check(rec, "Block 520123 Toa Payoh", "SG_POSTAL_CODE")
    check(rec, "Invalid 830001", "SG_POSTAL_CODE", expect_detect=False)

    # --- Passport ---
    print("\n--- SG Passport ---")
    rec = SgPassportRecognizer()
    check(rec, "Passport: E1234567A", "SG_PASSPORT")
    check(rec, "Travel document K9876543Z", "SG_PASSPORT")
    check(rec, "Invalid A1234567B", "SG_PASSPORT", expect_detect=False)

    # --- Bank Account ---
    print("\n--- SG Bank Account ---")
    rec = SgBankRecognizer()
    check(rec, "DBS account: 0123456789", "SG_BANK_NUMBER")
    check(rec, "POSB account 123456789", "SG_BANK_NUMBER")


# ============================================================
# MALAYSIA
# ============================================================
def test_malaysia():
    print("\n" + "=" * 70)
    print("MALAYSIA")
    print("=" * 70)

    # --- NRIC / MyKad ---
    print("\n--- MY NRIC / MyKad ---")
    rec = MyNricRecognizer()
    check(rec, "NRIC: 900101-14-1234", "MY_NRIC")
    check(rec, "MyKad 850215 08 5678", "MY_NRIC")
    check(rec, "IC number 901231141234", "MY_NRIC")  # continuous 12-digit

    # --- Postal Code ---
    print("\n--- MY Postal Code ---")
    rec = MyPostalCodeRecognizer()
    check(rec, "Poskod 50000 Kuala Lumpur", "MY_POSTAL_CODE")
    check(rec, "Postal code 88000 Kota Kinabalu", "MY_POSTAL_CODE")

    # --- Bank Account ---
    print("\n--- MY Bank Account ---")
    rec = MyBankRecognizer()
    check(rec, "Maybank account: 123456789012", "MY_BANK_NUMBER")
    check(rec, "CIMB bank 12345678901234", "MY_BANK_NUMBER")

    # --- Income Tax ---
    print("\n--- MY Income Tax Number ---")
    rec = MyIncomeTaxRecognizer()
    check(rec, "LHDN tax number: IG12345678901", "MY_INCOME_TAX")
    check(rec, "Income tax SG1234567890", "MY_INCOME_TAX")
    check(rec, "Tax C12345678901", "MY_INCOME_TAX")
    check(rec, "Invalid XX12345678901", "MY_INCOME_TAX", expect_detect=False)


# ============================================================
# FULL INTEGRATION TEST — AnalyzerEngine with all recognizers
# ============================================================
def test_integration_all_countries():
    """
    Register every new recognizer into a single AnalyzerEngine and
    run it against a multi-country sample document.
    """
    print("\n" + "=" * 70)
    print("INTEGRATION TEST — ALL COUNTRIES IN ONE ANALYZER")
    print("=" * 70)

    analyzer = AnalyzerEngine()

    # Register all new recognizers
    new_recognizers = [
        # Canada
        CaPostalCodeRecognizer(),
        CaSinRecognizer(),
        CaBankRecognizer(),
        CaDriverLicenseRecognizer(),
        CaGstRecognizer(),
        # Mexico
        MxCurpRecognizer(),
        MxClabeRecognizer(),
        MxPostalCodeRecognizer(),
        MxRfcRecognizer(),
        MxDriverLicenseRecognizer(),
        # UK
        UkPostcodeRecognizer(),
        UkSortCodeRecognizer(),
        UkDriverLicenseRecognizer(),
        UkUtrRecognizer(),
        # Germany
        DePostalCodeRecognizer(),
        DePensionInsuranceRecognizer(),
        DeDriverLicenseRecognizer(),
        DeTaxNumberRecognizer(),
        # France
        FrPostalCodeRecognizer(),
        FrInseeRecognizer(),
        FrDriverLicenseRecognizer(),
        FrSpiRecognizer(),
        # Saudi Arabia
        SaNationalIdRecognizer(),
        SaPostalCodeRecognizer(),
        SaTinRecognizer(),
        # UAE
        AeEmiratesIdRecognizer(),
        AePostalCodeRecognizer(),
        AeDriverLicenseRecognizer(),
        AeTrnRecognizer(),
        # South Africa
        ZaIdRecognizer(),
        ZaPostalCodeRecognizer(),
        ZaDriverLicenseRecognizer(),
        ZaTaxNumberRecognizer(),
        # Japan
        JpPostalCodeRecognizer(),
        JpMyNumberRecognizer(),
        JpBankRecognizer(),
        JpDriverLicenseRecognizer(),
        JpCorporateNumberRecognizer(),
        # India
        InPinCodeRecognizer(),
        InDriverLicenseRecognizer(),
        InIfscRecognizer(),
        # Australia
        AuPostcodeRecognizer(),
        AuBsbRecognizer(),
        AuDriverLicenseRecognizer(),
        # Singapore
        SgPostalCodeRecognizer(),
        SgPassportRecognizer(),
        SgBankRecognizer(),
        # Malaysia
        MyNricRecognizer(),
        MyPostalCodeRecognizer(),
        MyBankRecognizer(),
        MyIncomeTaxRecognizer(),
    ]

    for rec in new_recognizers:
        analyzer.registry.add_recognizer(rec)

    print(f"\nRegistered {len(new_recognizers)} new recognizers into AnalyzerEngine")

    # Multi-country sample document
    sample_text = """
    === CANADA ===
    Employee: Jean Tremblay
    SIN: 130-692-544
    Address: 100 Wellington St, Ottawa ON K1A 0B1
    Bank Transit: 12345-001
    Ontario DL: A1234-56789-01234
    GST/HST: 123456789RT0001

    === MEXICO ===
    Empleado: Carlos Garcia
    CURP: GARC850101HDFRRL09
    RFC: GARC850101AB1
    CLABE: 012345678901234567
    Direccion: Av Reforma 500, CDMX, C.P. 06600

    === UNITED KINGDOM ===
    Staff: James Wilson
    NI Number: AB 12 34 56 C
    Address: 10 Downing St, London SW1A 1AA
    Sort Code: 20-00-00
    PAYE: 123/AB12345
    Driving Licence: SMITH901019JA9AA

    === GERMANY ===
    Mitarbeiter: Hans Mueller
    Rentenversicherung: 12010180A123
    Steuernummer: 11/123/12345
    Adresse: Friedrichstr 100, 10115 Berlin
    Fuhrerschein: B072RRE2E10

    === FRANCE ===
    Employe: Pierre Dupont
    INSEE: 185073512345678
    SPI: 12 34 567 890 123
    Adresse: 1 Rue de Rivoli, 75001 Paris
    Permis: 12AB12345

    === SAUDI ARABIA ===
    National ID: 1234567890
    Iqama: 2234567890
    VAT: 300012345678901
    Address: Riyadh 12345

    === UAE ===
    Emirates ID: 784-1992-1234567-8
    TRN: 100123456789012
    Address: P.O. Box 4567, Dubai
    Makani: 30032 95320

    === SOUTH AFRICA ===
    SA ID: 9001015009087
    Tax Number: 0123456789
    Address: Pretoria 0001
    Driver Licence: AB12CD34EF56

    === JAPAN ===
    My Number: 1234-5678-9012
    Bank: 0001-001
    Address: 100-0001 Tokyo
    Corporate Number: 1234567890123

    === INDIA ===
    PIN Code: 110 001 New Delhi
    IFSC: SBIN0001234
    DL: KA0120120000001

    === AUSTRALIA ===
    Postcode: 2000 Sydney
    BSB: 062-000
    Driver Licence: 12345678

    === SINGAPORE ===
    Postal Code: 018956
    Passport: E1234567A
    Account: 0123456789

    === MALAYSIA ===
    NRIC: 900101-14-1234
    Poskod: 50000 KL
    Tax: IG12345678901
    """

    # All new entity types
    entities = [
        # Canada
        "CA_POSTAL_CODE", "CA_SIN", "CA_BANK_NUMBER",
        "CA_DRIVER_LICENSE", "CA_GST_NUMBER",
        # Mexico
        "MX_CURP", "MX_CLABE", "MX_POSTAL_CODE", "MX_RFC",
        "MX_DRIVER_LICENSE",
        # UK
        "UK_POSTCODE", "UK_SORT_CODE", "UK_DRIVER_LICENSE", "UK_UTR",
        # Germany
        "DE_POSTAL_CODE", "DE_PENSION_INSURANCE",
        "DE_DRIVER_LICENSE", "DE_TAX_NUMBER",
        # France
        "FR_POSTAL_CODE", "FR_INSEE", "FR_DRIVER_LICENSE", "FR_SPI",
        # Saudi
        "SA_NATIONAL_ID", "SA_POSTAL_CODE", "SA_TIN",
        # UAE
        "AE_EMIRATES_ID", "AE_POSTAL_CODE", "AE_DRIVER_LICENSE", "AE_TRN",
        # South Africa
        "ZA_ID_NUMBER", "ZA_POSTAL_CODE", "ZA_DRIVER_LICENSE", "ZA_TAX_NUMBER",
        # Japan
        "JP_POSTAL_CODE", "JP_MY_NUMBER", "JP_BANK_NUMBER",
        "JP_DRIVER_LICENSE", "JP_CORPORATE_NUMBER",
        # India
        "IN_PIN_CODE", "IN_DRIVER_LICENSE", "IN_IFSC",
        # Australia
        "AU_POSTCODE", "AU_BSB", "AU_DRIVER_LICENSE",
        # Singapore
        "SG_POSTAL_CODE", "SG_PASSPORT", "SG_BANK_NUMBER",
        # Malaysia
        "MY_NRIC", "MY_POSTAL_CODE", "MY_BANK_NUMBER", "MY_INCOME_TAX",
    ]

    results = analyzer.analyze(
        text=sample_text,
        entities=entities,
        language='en',
    )

    # Group by entity type
    by_type = {}
    for r in results:
        by_type.setdefault(r.entity_type, []).append(r)

    print(f"\nDetected {len(results)} entities across {len(by_type)} types:\n")
    for etype in sorted(by_type.keys()):
        items = by_type[etype]
        print(f"  {etype}:")
        for r in items:
            text_found = sample_text[r.start:r.end].strip()
            display = text_found if len(text_found) <= 40 else text_found[:37] + "..."
            print(f"    '{display}' (score: {r.score:.2f})")

    # Check coverage — which entity types were detected
    detected_types = set(by_type.keys())
    expected_types = set(entities)
    missing = expected_types - detected_types
    if missing:
        print(f"\n⚠ Entity types NOT detected in sample: {sorted(missing)}")
    else:
        print(f"\n✓ All {len(expected_types)} entity types detected at least once!")

    return results


# ============================================================
# MAIN
# ============================================================
def main():
    print("=" * 70)
    print("  COMPREHENSIVE PII RECOGNIZER TEST — ALL COUNTRIES")
    print("=" * 70)

    # Individual recognizer tests
    test_canada()
    test_mexico()
    test_uk()
    test_germany()
    test_france()
    test_saudi()
    test_uae()
    test_south_africa()
    test_japan()
    test_india_new()
    test_australia_new()
    test_singapore_new()
    test_malaysia()

    # Summary of individual tests
    print("\n" + "=" * 70)
    print(f"INDIVIDUAL TESTS: {total_pass} passed, {total_fail} failed")
    print("=" * 70)

    # Integration test
    test_integration_all_countries()

    # Final summary
    print("\n" + "=" * 70)
    if total_fail == 0:
        print("✅ ALL TESTS PASSED!")
    else:
        print(f"⚠ {total_fail} TESTS FAILED — review output above")
    print("=" * 70)

    return total_fail


if __name__ == "__main__":
    sys.exit(main())
