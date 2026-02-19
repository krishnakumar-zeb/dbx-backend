"""
Custom recognizers for entities not supported by Presidio's default installation.
These recognizers are imported from the custom Presidio folder and registered programmatically.
"""
from typing import List
from presidio_analyzer import EntityRecognizer
import logging

logger = logging.getLogger(__name__)


def get_custom_recognizers() -> List[EntityRecognizer]:
    """
    Get all custom recognizers to be registered with Presidio.
    
    This function imports recognizer classes from the custom Presidio folder
    and instantiates them for registration.
    
    Returns:
        List of EntityRecognizer instances to be added to the registry
    """
    custom_recognizers = []
    
    try:
        # ============================================================
        # UNITED STATES RECOGNIZERS (Built-in but need explicit loading)
        # ============================================================
        from presidio_analyzer.predefined_recognizers.country_specific.us import (
            UsSsnRecognizer,
            UsItinRecognizer,
            UsPassportRecognizer,
            UsLicenseRecognizer,  # ⚠️ Correct name is UsLicenseRecognizer, not UsDriverLicenseRecognizer
            UsBankRecognizer,
        )
        from presidio_analyzer.predefined_recognizers import ZipCodeRecognizer  # US Zip Code
        
        custom_recognizers.extend([
            UsSsnRecognizer(supported_language="en"),
            UsItinRecognizer(supported_language="en"),
            UsPassportRecognizer(supported_language="en"),
            UsLicenseRecognizer(supported_language="en"),
            UsBankRecognizer(supported_language="en"),
            ZipCodeRecognizer(),  # US-specific postal code
        ])
        logger.info("Loaded United States recognizers")
    except ImportError as e:
        logger.warning(f"Could not load United States recognizers: {e}")
    
    try:
        # ============================================================
        # MEXICO RECOGNIZERS (Custom - not in default Presidio)
        # ============================================================
        from presidio_analyzer.predefined_recognizers.country_specific.mexico import (
            MxCurpRecognizer,
            MxRfcRecognizer,
            MxDriverLicenseRecognizer,
            MxPostalCodeRecognizer,
            MxClabeRecognizer,
        )
        custom_recognizers.extend([
            MxCurpRecognizer(supported_language="en"),
            MxRfcRecognizer(supported_language="en"),
            MxDriverLicenseRecognizer(supported_language="en"),
            MxPostalCodeRecognizer(supported_language="en"),
            MxClabeRecognizer(supported_language="en"),
        ])
        logger.info("Loaded Mexico recognizers")
    except ImportError as e:
        logger.warning(f"Could not load Mexico recognizers: {e}")
    
    try:
        # ============================================================
        # CANADA RECOGNIZERS (Custom - not in default Presidio)
        # ============================================================
        from presidio_analyzer.predefined_recognizers.country_specific.canada import (
            CaSinRecognizer,
            CaBankRecognizer,
            CaDriverLicenseRecognizer,
            CaPostalCodeRecognizer,
            CaGstRecognizer,
        )
        custom_recognizers.extend([
            CaSinRecognizer(supported_language="en"),
            CaBankRecognizer(supported_language="en"),
            CaDriverLicenseRecognizer(supported_language="en"),
            CaPostalCodeRecognizer(supported_language="en"),
            CaGstRecognizer(supported_language="en"),
        ])
        logger.info("Loaded Canada recognizers")
    except ImportError as e:
        logger.warning(f"Could not load Canada recognizers: {e}")
    
    try:
        # ============================================================
        # UK RECOGNIZERS (Enable disabled ones)
        # ============================================================
        from presidio_analyzer.predefined_recognizers.country_specific.uk import (
            UkNinoRecognizer,
            UkDriverLicenseRecognizer,
            NhsRecognizer,  # ⚠️ Correct name is NhsRecognizer, not UkNhsRecognizer
            UkPostcodeRecognizer,
            UkSortCodeRecognizer,
            UkUtrRecognizer,
        )
        custom_recognizers.extend([
            UkNinoRecognizer(supported_language="en"),
            UkDriverLicenseRecognizer(supported_language="en"),
            NhsRecognizer(supported_language="en"),
            UkPostcodeRecognizer(supported_language="en"),
            UkSortCodeRecognizer(supported_language="en"),
            UkUtrRecognizer(supported_language="en"),
        ])
        logger.info("Loaded UK recognizers")
    except ImportError as e:
        logger.warning(f"Could not load UK recognizers: {e}")
    
    try:
        # ============================================================
        # GERMANY RECOGNIZERS
        # ============================================================
        from presidio_analyzer.predefined_recognizers.country_specific.germany import (
            DeDriverLicenseRecognizer,
            DeTaxNumberRecognizer,
            DePostalCodeRecognizer,
            DePensionInsuranceRecognizer,
        )
        custom_recognizers.extend([
            DeDriverLicenseRecognizer(supported_language="en"),
            DeTaxNumberRecognizer(supported_language="en"),
            DePostalCodeRecognizer(supported_language="en"),
            DePensionInsuranceRecognizer(supported_language="en"),
        ])
        logger.info("Loaded Germany recognizers")
    except ImportError as e:
        logger.warning(f"Could not load Germany recognizers: {e}")
    
    try:
        # ============================================================
        # FRANCE RECOGNIZERS
        # ============================================================
        from presidio_analyzer.predefined_recognizers.country_specific.france import (
            FrInseeRecognizer,
            FrDriverLicenseRecognizer,
            FrPostalCodeRecognizer,
            FrSpiRecognizer,
        )
        custom_recognizers.extend([
            FrInseeRecognizer(supported_language="en"),
            FrDriverLicenseRecognizer(supported_language="en"),
            FrPostalCodeRecognizer(supported_language="en"),
            FrSpiRecognizer(supported_language="en"),
        ])
        logger.info("Loaded France recognizers")
    except ImportError as e:
        logger.warning(f"Could not load France recognizers: {e}")
    
    try:
        # ============================================================
        # UAE RECOGNIZERS (Custom - not in default Presidio)
        # ============================================================
        from presidio_analyzer.predefined_recognizers.country_specific.uae import (
            AeEmiratesIdRecognizer,
            AeTrnRecognizer,
            AeDriverLicenseRecognizer,
            AePostalCodeRecognizer,
        )
        custom_recognizers.extend([
            AeEmiratesIdRecognizer(supported_language="en"),
            AeTrnRecognizer(supported_language="en"),
            AeDriverLicenseRecognizer(supported_language="en"),
            AePostalCodeRecognizer(supported_language="en"),
        ])
        logger.info("Loaded UAE recognizers")
    except ImportError as e:
        logger.warning(f"Could not load UAE recognizers: {e}")
    
    try:
        # ============================================================
        # SAUDI ARABIA RECOGNIZERS
        # ============================================================
        from presidio_analyzer.predefined_recognizers.country_specific.saudi import (
            SaNationalIdRecognizer,
            SaPostalCodeRecognizer,
            SaTinRecognizer,
        )
        custom_recognizers.extend([
            SaNationalIdRecognizer(supported_language="en"),
            SaPostalCodeRecognizer(supported_language="en"),
            SaTinRecognizer(supported_language="en"),
        ])
        logger.info("Loaded Saudi Arabia recognizers")
    except ImportError as e:
        logger.warning(f"Could not load Saudi Arabia recognizers: {e}")
    
    try:
        # ============================================================
        # SOUTH AFRICA RECOGNIZERS
        # ============================================================
        from presidio_analyzer.predefined_recognizers.country_specific.south_africa import (
            ZaIdRecognizer,
            ZaTaxNumberRecognizer,
            ZaDriverLicenseRecognizer,
            ZaPostalCodeRecognizer,
        )
        custom_recognizers.extend([
            ZaIdRecognizer(supported_language="en"),
            ZaTaxNumberRecognizer(supported_language="en"),
            ZaDriverLicenseRecognizer(supported_language="en"),
            ZaPostalCodeRecognizer(supported_language="en"),
        ])
        logger.info("Loaded South Africa recognizers")
    except ImportError as e:
        logger.warning(f"Could not load South Africa recognizers: {e}")
    
    try:
        # ============================================================
        # JAPAN RECOGNIZERS
        # ============================================================
        from presidio_analyzer.predefined_recognizers.country_specific.japan import (
            JpMyNumberRecognizer,
            JpDriverLicenseRecognizer,
            JpBankRecognizer,
            JpPostalCodeRecognizer,
            JpCorporateNumberRecognizer,
        )
        custom_recognizers.extend([
            JpMyNumberRecognizer(supported_language="en"),
            JpDriverLicenseRecognizer(supported_language="en"),
            JpBankRecognizer(supported_language="en"),
            JpPostalCodeRecognizer(supported_language="en"),
            JpCorporateNumberRecognizer(supported_language="en"),
        ])
        logger.info("Loaded Japan recognizers")
    except ImportError as e:
        logger.warning(f"Could not load Japan recognizers: {e}")
    
    try:
        # ============================================================
        # INDIA RECOGNIZERS (Enable disabled ones)
        # ============================================================
        from presidio_analyzer.predefined_recognizers.country_specific.india import (
            InAadhaarRecognizer,
            InPanRecognizer,
            #InPassportRecognizer,
            InDriverLicenseRecognizer,
            #InVoterRecognizer,
            InPinCodeRecognizer,
            InIfscRecognizer,
        )
        custom_recognizers.extend([
            InAadhaarRecognizer(supported_language="en"),
            InPanRecognizer(supported_language="en"),
            #InPassportRecognizer(supported_language="en"),
            InDriverLicenseRecognizer(supported_language="en"),
            #InVoterRecognizer(supported_language="en"),
            InPinCodeRecognizer(supported_language="en"),
            InIfscRecognizer(supported_language="en"),
        ])
        logger.info("Loaded India recognizers")
    except ImportError as e:
        logger.warning(f"Could not load India recognizers: {e}")
    
    try:
        # ============================================================
        # AUSTRALIA RECOGNIZERS (Enable disabled ones)
        # ============================================================
        from presidio_analyzer.predefined_recognizers.country_specific.australia import (
            AuTfnRecognizer,
            AuMedicareRecognizer,
            AuDriverLicenseRecognizer,
            AuPostcodeRecognizer,
            AuAbnRecognizer,
            AuBsbRecognizer,
        )
        custom_recognizers.extend([
            AuTfnRecognizer(supported_language="en"),
            AuMedicareRecognizer(supported_language="en"),
            AuDriverLicenseRecognizer(supported_language="en"),
            AuPostcodeRecognizer(supported_language="en"),
            AuAbnRecognizer(supported_language="en"),
            AuBsbRecognizer(supported_language="en"),
        ])
        logger.info("Loaded Australia recognizers")
    except ImportError as e:
        logger.warning(f"Could not load Australia recognizers: {e}")
    
    try:
        # ============================================================
        # SINGAPORE RECOGNIZERS (Enable disabled ones)
        # ============================================================
        from presidio_analyzer.predefined_recognizers.country_specific.singapore import (
            SgFinRecognizer,
            SgUenRecognizer,
            SgPassportRecognizer,
            SgBankRecognizer,
            SgPostalCodeRecognizer,
        )
        custom_recognizers.extend([
            SgFinRecognizer(supported_language="en"),
            SgUenRecognizer(supported_language="en"),
            SgPassportRecognizer(supported_language="en"),
            SgBankRecognizer(supported_language="en"),
            SgPostalCodeRecognizer(supported_language="en"),
        ])
        logger.info("Loaded Singapore recognizers")
    except ImportError as e:
        logger.warning(f"Could not load Singapore recognizers: {e}")
    
    try:
        # ============================================================
        # MALAYSIA RECOGNIZERS
        # ============================================================
        from presidio_analyzer.predefined_recognizers.country_specific.malaysia import (
            MyNricRecognizer,
            MyIncomeTaxRecognizer,
            MyBankRecognizer,
            MyPostalCodeRecognizer,
        )
        custom_recognizers.extend([
            MyNricRecognizer(supported_language="en"),
            MyIncomeTaxRecognizer(supported_language="en"),
            MyBankRecognizer(supported_language="en"),
            MyPostalCodeRecognizer(supported_language="en"),
        ])
        logger.info("Loaded Malaysia recognizers")
    except ImportError as e:
        logger.warning(f"Could not load Malaysia recognizers: {e}")
    
    try:
        # ============================================================
        # GENERIC RECOGNIZERS (Common entities across all countries)
        # ============================================================
        import os
        from presidio_analyzer.predefined_recognizers import (
            EmailRecognizer,
            PhoneRecognizer,
            IpRecognizer,
            SpacyRecognizer,
            AgeRecognizer,
            EthnicityRecognizer,
            CookieRecognizer,
            GenderRecognizer,
            CertificateRecognizer,
            IbanRecognizer,
            # NOTE: ZipCodeRecognizer is US-specific, not generic!
            # Each country has its own postal code recognizer
        )
        
        # Path to ethnicities.json file
        ethnicities_path = os.path.join(
            os.path.dirname(__file__), 
            "..", "..", "Presdio", "ethnicities.json"
        )
        
        # Add common entity recognizers
        custom_recognizers.extend([
            EmailRecognizer(),           # EMAIL_ADDRESS
            PhoneRecognizer(),           # PHONE_NUMBER
            IpRecognizer(),              # IP_ADDRESS
            SpacyRecognizer(),           # PERSON, LOCATION (NER-based)
            AgeRecognizer(),             # AGE
            GenderRecognizer(),          # GENDER
            CookieRecognizer(),          # COOKIE
            CertificateRecognizer(),     # CERTIFICATE_NUMBER
            IbanRecognizer(),            # IBAN_CODE
        ])
        
        # Add EthnicityRecognizer with JSON file if it exists
        if os.path.exists(ethnicities_path):
            custom_recognizers.append(
                EthnicityRecognizer(ethnicity_json_path=ethnicities_path)
            )
            logger.info(f"Loaded EthnicityRecognizer with JSON: {ethnicities_path}")
        else:
            custom_recognizers.append(EthnicityRecognizer())
            logger.warning(f"EthnicityRecognizer loaded without JSON (file not found: {ethnicities_path})")
        
        logger.info("Loaded generic recognizers (Email, Phone, IP, Spacy/NER, Age, Gender, Ethnicity, Cookie, Certificate, IBAN)")
    except ImportError as e:
        logger.warning(f"Could not load generic recognizers: {e}")
    
    logger.info(f"Total custom recognizers loaded: {len(custom_recognizers)}")
    return custom_recognizers
