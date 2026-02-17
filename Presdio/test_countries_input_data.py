"""
Test all country-specific PII recognizers against real sample data
from text_countries_input_data.txt.

Each recognizer is tested individually against the exact data points
from the input file to verify detection works correctly.

Usage: python test_countries_input_data.py
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
    # UK
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
    # India
    InPinCodeRecognizer,
    InDriverLicenseRecognizer,
    InIfscRecognizer,
    # Australia
    AuPostcodeRecognizer,
    AuBsbRecognizer,
    AuDriverLicenseRecognizer,
    # Singapore
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


def check(recognizer, text, entity, label=""):
    """
    Run a single recognizer against text and report detection.
    """
    global total_pass, total_fail
    results = recognizer.analyze(text, [entity])

    if results:
        total_pass += 1
        for r in results:
            found = text[r.start:r.end]
            print(f"  ✓ [{label}] Detected: '{found}' (score: {r.score:.2f})")
    else:
        total_fail += 1
        print(f"  ✗ [{label}] MISSED in: '{text[:80]}...'")


# ============================================================
# Read input data file
# ============================================================
with open("text_countries_input_data.txt", "r", encoding="utf-8") as f:
    full_text = f.read()

# Split into country sections
sections = {}
current_country = None
current_lines = []
for line in full_text.split("\n"):
    stripped = line.strip()
    if stripped in ("Canada:", "Mexico:", "UNITED KINGDOM:", "GERMANY",
                    "FRANCE", "SAUDI ARABIA", "UNITED ARAB EMIRATES",
                    "SOUTH AFRICA", "JAPAN", "INDIA", "AUSTRALIA",
                    "SINGAPORE", "MALAYSIA"):
        if current_country:
            sections[current_country] = "\n".join(current_lines)
        current_country = stripped.rstrip(":")
        current_lines = []
    else:
        current_lines.append(line)
if current_country:
    sections[current_country] = "\n".join(current_lines)


# ============================================================
# CANADA
# ============================================================
def test_canada():
    print("\n" + "=" * 70)
    print("CANADA")
    print("=" * 70)
    text = sections["Canada"]

    print("\n--- CA Postal Code ---")
    rec = CaPostalCodeRecognizer()
    check(rec, text, "CA_POSTAL_CODE", "M5V 3A8")

    print("\n--- CA SIN ---")
    rec = CaSinRecognizer()
    check(rec, text, "CA_SIN", "130454283")

    print("\n--- CA Bank Transit ---")
    rec = CaBankRecognizer()
    check(rec, text, "CA_BANK_NUMBER", "24567-004")

    print("\n--- CA Driver License ---")
    rec = CaDriverLicenseRecognizer()
    check(rec, text, "CA_DRIVER_LICENSE", "T2847-95034-61289")

    print("\n--- CA GST/HST ---")
    rec = CaGstRecognizer()
    check(rec, text, "CA_GST_NUMBER", "845672139RT0001")


# ============================================================
# MEXICO
# ============================================================
def test_mexico():
    print("\n" + "=" * 70)
    print("MEXICO")
    print("=" * 70)
    text = sections["Mexico"]

    print("\n--- MX CURP ---")
    rec = MxCurpRecognizer()
    check(rec, text, "MX_CURP", "HEGC950722HJCLRR09")

    print("\n--- MX CLABE ---")
    rec = MxClabeRecognizer()
    check(rec, text, "MX_CLABE", "012180001234567890")

    print("\n--- MX Postal Code ---")
    rec = MxPostalCodeRecognizer()
    check(rec, text, "MX_POSTAL_CODE", "44100")

    print("\n--- MX RFC ---")
    rec = MxRfcRecognizer()
    check(rec, text, "MX_RFC", "HEGC950722AB3")

    print("\n--- MX Driver License ---")
    rec = MxDriverLicenseRecognizer()
    check(rec, text, "MX_DRIVER_LICENSE", "G04587392")


# ============================================================
# UNITED KINGDOM
# ============================================================
def test_uk():
    print("\n" + "=" * 70)
    print("UNITED KINGDOM")
    print("=" * 70)
    text = sections["UNITED KINGDOM"]

    print("\n--- UK Postcode ---")
    rec = UkPostcodeRecognizer()
    check(rec, text, "UK_POSTCODE", "M1 4BT")

    print("\n--- UK Sort Code ---")
    rec = UkSortCodeRecognizer()
    check(rec, text, "UK_SORT_CODE", "20-45-67")

    print("\n--- UK Driver License ---")
    rec = UkDriverLicenseRecognizer()
    check(rec, text, "UK_DRIVER_LICENSE", "BENNE811086OJ9IK")

    print("\n--- UK UTR / PAYE ---")
    rec = UkUtrRecognizer()
    check(rec, text, "UK_UTR", "1234567890 / 123/AB45678")


# ============================================================
# GERMANY
# ============================================================
def test_germany():
    print("\n" + "=" * 70)
    print("GERMANY")
    print("=" * 70)
    text = sections["GERMANY"]

    print("\n--- DE Postal Code ---")
    rec = DePostalCodeRecognizer()
    check(rec, text, "DE_POSTAL_CODE", "80331")

    print("\n--- DE Pension Insurance ---")
    rec = DePensionInsuranceRecognizer()
    check(rec, text, "DE_PENSION_INSURANCE", "12 140487 S 123")

    print("\n--- DE Driver License ---")
    rec = DeDriverLicenseRecognizer()
    check(rec, text, "DE_DRIVER_LICENSE", "S9876543210")

    print("\n--- DE Tax Number ---")
    rec = DeTaxNumberRecognizer()
    check(rec, text, "DE_TAX_NUMBER", "123/456/78901")


# ============================================================
# FRANCE
# ============================================================
def test_france():
    print("\n" + "=" * 70)
    print("FRANCE")
    print("=" * 70)
    text = sections["FRANCE"]

    print("\n--- FR Postal Code ---")
    rec = FrPostalCodeRecognizer()
    check(rec, text, "FR_POSTAL_CODE", "69001")

    print("\n--- FR INSEE ---")
    rec = FrInseeRecognizer()
    check(rec, text, "FR_INSEE", "1 78 09 69 123 456 78")

    print("\n--- FR Driver License ---")
    rec = FrDriverLicenseRecognizer()
    check(rec, text, "FR_DRIVER_LICENSE", "780903123456")

    print("\n--- FR SPI ---")
    rec = FrSpiRecognizer()
    check(rec, text, "FR_SPI", "0123456789012")


# ============================================================
# SAUDI ARABIA
# ============================================================
def test_saudi():
    print("\n" + "=" * 70)
    print("SAUDI ARABIA")
    print("=" * 70)
    text = sections["SAUDI ARABIA"]

    print("\n--- SA National ID ---")
    rec = SaNationalIdRecognizer()
    check(rec, text, "SA_NATIONAL_ID", "1012345678")

    print("\n--- SA Postal Code ---")
    rec = SaPostalCodeRecognizer()
    check(rec, text, "SA_POSTAL_CODE", "11564")

    print("\n--- SA TIN / VAT ---")
    rec = SaTinRecognizer()
    check(rec, text, "SA_TIN", "300123456789003 / 310123456700003")


# ============================================================
# UAE
# ============================================================
def test_uae():
    print("\n" + "=" * 70)
    print("UAE")
    print("=" * 70)
    text = sections["UNITED ARAB EMIRATES"]

    print("\n--- AE Emirates ID ---")
    rec = AeEmiratesIdRecognizer()
    check(rec, text, "AE_EMIRATES_ID", "784-1995-1234567-8")

    print("\n--- AE P.O. Box / Makani ---")
    rec = AePostalCodeRecognizer()
    check(rec, text, "AE_POSTAL_CODE", "P.O. Box 54321 / Makani 2584123456")

    print("\n--- AE TRN ---")
    rec = AeTrnRecognizer()
    check(rec, text, "AE_TRN", "100123456700003")

    print("\n--- AE Driver License ---")
    rec = AeDriverLicenseRecognizer()
    check(rec, text, "AE_DRIVER_LICENSE", "1234567")


# ============================================================
# SOUTH AFRICA
# ============================================================
def test_south_africa():
    print("\n" + "=" * 70)
    print("SOUTH AFRICA")
    print("=" * 70)
    text = sections["SOUTH AFRICA"]

    print("\n--- ZA ID Number ---")
    rec = ZaIdRecognizer()
    check(rec, text, "ZA_ID_NUMBER", "8506165123084")

    print("\n--- ZA Postal Code ---")
    rec = ZaPostalCodeRecognizer()
    check(rec, text, "ZA_POSTAL_CODE", "2001")

    print("\n--- ZA Tax Number ---")
    rec = ZaTaxNumberRecognizer()
    check(rec, text, "ZA_TAX_NUMBER", "0123456789")

    print("\n--- ZA Driver License ---")
    rec = ZaDriverLicenseRecognizer()
    check(rec, text, "ZA_DRIVER_LICENSE", "01234567890")


# ============================================================
# JAPAN
# ============================================================
def test_japan():
    print("\n" + "=" * 70)
    print("JAPAN")
    print("=" * 70)
    text = sections["JAPAN"]

    print("\n--- JP Postal Code ---")
    rec = JpPostalCodeRecognizer()
    check(rec, text, "JP_POSTAL_CODE", "150-0042")

    print("\n--- JP My Number ---")
    rec = JpMyNumberRecognizer()
    check(rec, text, "JP_MY_NUMBER", "123456789012")

    print("\n--- JP Bank ---")
    rec = JpBankRecognizer()
    check(rec, text, "JP_BANK_NUMBER", "0001-234")

    print("\n--- JP Driver License ---")
    rec = JpDriverLicenseRecognizer()
    check(rec, text, "JP_DRIVER_LICENSE", "123456789012")

    print("\n--- JP Corporate Number ---")
    rec = JpCorporateNumberRecognizer()
    check(rec, text, "JP_CORPORATE_NUMBER", "1234567890123")


# ============================================================
# INDIA
# ============================================================
def test_india():
    print("\n" + "=" * 70)
    print("INDIA")
    print("=" * 70)
    text = sections["INDIA"]

    print("\n--- IN PIN Code ---")
    rec = InPinCodeRecognizer()
    check(rec, text, "IN_PIN_CODE", "560001")

    print("\n--- IN IFSC ---")
    rec = InIfscRecognizer()
    check(rec, text, "IN_IFSC", "SBIN0001234")

    print("\n--- IN Driver License ---")
    rec = InDriverLicenseRecognizer()
    check(rec, text, "IN_DRIVER_LICENSE", "KA0120160012345")


# ============================================================
# AUSTRALIA
# ============================================================
def test_australia():
    print("\n" + "=" * 70)
    print("AUSTRALIA")
    print("=" * 70)
    text = sections["AUSTRALIA"]

    print("\n--- AU Postcode ---")
    rec = AuPostcodeRecognizer()
    check(rec, text, "AU_POSTCODE", "2000")

    print("\n--- AU BSB ---")
    rec = AuBsbRecognizer()
    check(rec, text, "AU_BSB", "062-000")

    print("\n--- AU Driver Licence ---")
    rec = AuDriverLicenseRecognizer()
    check(rec, text, "AU_DRIVER_LICENSE", "12345678")


# ============================================================
# SINGAPORE
# ============================================================
def test_singapore():
    print("\n" + "=" * 70)
    print("SINGAPORE")
    print("=" * 70)
    text = sections["SINGAPORE"]

    print("\n--- SG Postal Code ---")
    rec = SgPostalCodeRecognizer()
    check(rec, text, "SG_POSTAL_CODE", "520123")

    print("\n--- SG Passport ---")
    rec = SgPassportRecognizer()
    check(rec, text, "SG_PASSPORT", "E1234567K")

    print("\n--- SG Bank Account ---")
    rec = SgBankRecognizer()
    check(rec, text, "SG_BANK_NUMBER", "123-456789-001")


# ============================================================
# MALAYSIA
# ============================================================
def test_malaysia():
    print("\n" + "=" * 70)
    print("MALAYSIA")
    print("=" * 70)
    text = sections["MALAYSIA"]

    print("\n--- MY NRIC / MyKad ---")
    rec = MyNricRecognizer()
    check(rec, text, "MY_NRIC", "880710-14-5678")

    print("\n--- MY Postal Code ---")
    rec = MyPostalCodeRecognizer()
    check(rec, text, "MY_POSTAL_CODE", "50450")

    print("\n--- MY Bank Account ---")
    rec = MyBankRecognizer()
    check(rec, text, "MY_BANK_NUMBER", "1234567890123456")

    print("\n--- MY Income Tax ---")
    rec = MyIncomeTaxRecognizer()
    check(rec, text, "MY_INCOME_TAX", "SG12345678901")


# ============================================================
# MAIN
# ============================================================
def main():
    print("=" * 70)
    print("  PII RECOGNIZER TEST — INPUT DATA FILE")
    print("  Source: text_countries_input_data.txt")
    print("=" * 70)

    test_canada()
    test_mexico()
    test_uk()
    test_germany()
    test_france()
    test_saudi()
    test_uae()
    test_south_africa()
    test_japan()
    test_india()
    test_australia()
    test_singapore()
    test_malaysia()

    # Summary
    print("\n" + "=" * 70)
    print(f"RESULTS: {total_pass} passed, {total_fail} failed "
          f"out of {total_pass + total_fail} tests")
    print("=" * 70)

    if total_fail == 0:
        print("✅ ALL TESTS PASSED!")
    else:
        print(f"⚠ {total_fail} TESTS FAILED — review output above")

    return total_fail


if __name__ == "__main__":
    sys.exit(main())
