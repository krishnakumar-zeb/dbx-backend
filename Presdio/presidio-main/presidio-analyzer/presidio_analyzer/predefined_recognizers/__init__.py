"""Predefined recognizers package. Holds all the default recognizers."""

# NLP Engine recognizers
from presidio_analyzer.predefined_recognizers.nlp_engine_recognizers.transformers_recognizer import (  # noqa: E501
    TransformersRecognizer,
)

# Australia recognizers
from .country_specific.australia.au_abn_recognizer import AuAbnRecognizer
from .country_specific.australia.au_acn_recognizer import AuAcnRecognizer
from .country_specific.australia.au_bsb_recognizer import AuBsbRecognizer
from .country_specific.australia.au_driver_license_recognizer import AuDriverLicenseRecognizer
from .country_specific.australia.au_medicare_recognizer import AuMedicareRecognizer
from .country_specific.australia.au_postcode_recognizer import AuPostcodeRecognizer
from .country_specific.australia.au_tfn_recognizer import AuTfnRecognizer

# Canada recognizers
from .country_specific.canada.ca_bank_recognizer import CaBankRecognizer
from .country_specific.canada.ca_driver_license_recognizer import CaDriverLicenseRecognizer
from .country_specific.canada.ca_gst_recognizer import CaGstRecognizer
from .country_specific.canada.ca_postal_code_recognizer import CaPostalCodeRecognizer
from .country_specific.canada.ca_sin_recognizer import CaSinRecognizer

# Finland recognizers
from .country_specific.finland.fi_personal_identity_code_recognizer import (
    FiPersonalIdentityCodeRecognizer,
)
from .country_specific.india import (
    InVehicleRegistrationRecognizer,
)

# France recognizers
from .country_specific.france.fr_driver_license_recognizer import FrDriverLicenseRecognizer
from .country_specific.france.fr_insee_recognizer import FrInseeRecognizer
from .country_specific.france.fr_postal_code_recognizer import FrPostalCodeRecognizer
from .country_specific.france.fr_spi_recognizer import FrSpiRecognizer

# Germany recognizers
from .country_specific.germany.de_driver_license_recognizer import DeDriverLicenseRecognizer
from .country_specific.germany.de_pension_insurance_recognizer import DePensionInsuranceRecognizer
from .country_specific.germany.de_postal_code_recognizer import DePostalCodeRecognizer
from .country_specific.germany.de_tax_number_recognizer import DeTaxNumberRecognizer

# India recognizers
from .country_specific.india.in_aadhaar_recognizer import InAadhaarRecognizer
from .country_specific.india.in_driver_license_recognizer import InDriverLicenseRecognizer
from .country_specific.india.in_gstin_recognizer import InGstinRecognizer
from .country_specific.india.in_ifsc_recognizer import InIfscRecognizer
from .country_specific.india.in_pan_recognizer import InPanRecognizer
from .country_specific.india.in_passport_recognizer import InPassportRecognizer
from .country_specific.india.in_pin_code_recognizer import InPinCodeRecognizer
from .country_specific.india.in_voter_recognizer import InVoterRecognizer

# Italy recognizers
from .country_specific.italy.it_driver_license_recognizer import (
    ItDriverLicenseRecognizer,
)
from .country_specific.italy.it_fiscal_code_recognizer import ItFiscalCodeRecognizer
from .country_specific.italy.it_identity_card_recognizer import ItIdentityCardRecognizer
from .country_specific.italy.it_passport_recognizer import ItPassportRecognizer
from .country_specific.italy.it_vat_code import ItVatCodeRecognizer

# Japan recognizers
from .country_specific.japan.jp_bank_recognizer import JpBankRecognizer
from .country_specific.japan.jp_corporate_number_recognizer import JpCorporateNumberRecognizer
from .country_specific.japan.jp_driver_license_recognizer import JpDriverLicenseRecognizer
from .country_specific.japan.jp_my_number_recognizer import JpMyNumberRecognizer
from .country_specific.japan.jp_postal_code_recognizer import JpPostalCodeRecognizer

# Korea recognizers
from .country_specific.korea.kr_brn_recognizer import KrBrnRecognizer
from .country_specific.korea.kr_driver_license_recognizer import (
    KrDriverLicenseRecognizer,
)
from .country_specific.korea.kr_frn_recognizer import KrFrnRecognizer
from .country_specific.korea.kr_passport_recognizer import KrPassportRecognizer
from .country_specific.korea.kr_rrn_recognizer import KrRrnRecognizer

# Malaysia recognizers
from .country_specific.malaysia.my_bank_recognizer import MyBankRecognizer
from .country_specific.malaysia.my_income_tax_recognizer import MyIncomeTaxRecognizer
from .country_specific.malaysia.my_nric_recognizer import MyNricRecognizer
from .country_specific.malaysia.my_postal_code_recognizer import MyPostalCodeRecognizer

# Mexico recognizers
from .country_specific.mexico.mx_clabe_recognizer import MxClabeRecognizer
from .country_specific.mexico.mx_curp_recognizer import MxCurpRecognizer
from .country_specific.mexico.mx_driver_license_recognizer import MxDriverLicenseRecognizer
from .country_specific.mexico.mx_postal_code_recognizer import MxPostalCodeRecognizer
from .country_specific.mexico.mx_rfc_recognizer import MxRfcRecognizer

# Poland recognizers
from .country_specific.poland.pl_pesel_recognizer import PlPeselRecognizer

# Saudi Arabia recognizers
from .country_specific.saudi.sa_national_id_recognizer import SaNationalIdRecognizer
from .country_specific.saudi.sa_postal_code_recognizer import SaPostalCodeRecognizer
from .country_specific.saudi.sa_tin_recognizer import SaTinRecognizer

# Singapore recognizers
from .country_specific.singapore.sg_bank_recognizer import SgBankRecognizer
from .country_specific.singapore.sg_fin_recognizer import SgFinRecognizer
from .country_specific.singapore.sg_passport_recognizer import SgPassportRecognizer
from .country_specific.singapore.sg_postal_code_recognizer import SgPostalCodeRecognizer
from .country_specific.singapore.sg_uen_recognizer import SgUenRecognizer

# South Africa recognizers
from .country_specific.south_africa.za_driver_license_recognizer import ZaDriverLicenseRecognizer
from .country_specific.south_africa.za_id_recognizer import ZaIdRecognizer
from .country_specific.south_africa.za_postal_code_recognizer import ZaPostalCodeRecognizer
from .country_specific.south_africa.za_tax_number_recognizer import ZaTaxNumberRecognizer

# Spain recognizers
from .country_specific.spain.es_nie_recognizer import EsNieRecognizer
from .country_specific.spain.es_nif_recognizer import EsNifRecognizer

# Thai recognizers
from .country_specific.thai.th_tnin_recognizer import ThTninRecognizer

# UAE recognizers
from .country_specific.uae.ae_driver_license_recognizer import AeDriverLicenseRecognizer
from .country_specific.uae.ae_emirates_id_recognizer import AeEmiratesIdRecognizer
from .country_specific.uae.ae_postal_code_recognizer import AePostalCodeRecognizer
from .country_specific.uae.ae_trn_recognizer import AeTrnRecognizer

# UK recognizers
from .country_specific.uk.uk_driver_license_recognizer import UkDriverLicenseRecognizer
from .country_specific.uk.uk_nhs_recognizer import NhsRecognizer
from .country_specific.uk.uk_nino_recognizer import UkNinoRecognizer
from .country_specific.uk.uk_postcode_recognizer import UkPostcodeRecognizer
from .country_specific.uk.uk_sort_code_recognizer import UkSortCodeRecognizer
from .country_specific.uk.uk_utr_recognizer import UkUtrRecognizer

# US recognizers
from .country_specific.us.aba_routing_recognizer import AbaRoutingRecognizer
from .country_specific.us.medical_license_recognizer import MedicalLicenseRecognizer
from .country_specific.us.us_bank_recognizer import UsBankRecognizer
from .country_specific.us.us_driver_license_recognizer import UsLicenseRecognizer
from .country_specific.us.us_itin_recognizer import UsItinRecognizer
from .country_specific.us.us_mbi_recognizer import UsMbiRecognizer
from .country_specific.us.us_passport_recognizer import UsPassportRecognizer
from .country_specific.us.us_ssn_recognizer import UsSsnRecognizer

# Generic recognizers
from .generic.age_recognizer import AgeRecognizer
from .generic.certificate_recognizer import CertificateRecognizer
from .generic.cookie_recognizer import CookieRecognizer
from .generic.credit_card_recognizer import CreditCardRecognizer
from .generic.crypto_recognizer import CryptoRecognizer
from .generic.date_recognizer import DateRecognizer
from .generic.email_recognizer import EmailRecognizer
from .generic.ethnicity_recognizer import EthnicityRecognizer
from .generic.gender_recognizer import GenderRecognizer
from .generic.iban_recognizer import IbanRecognizer
from .generic.ip_recognizer import IpRecognizer
from .generic.mac_recognizer import MacAddressRecognizer
from .generic.phone_recognizer import PhoneRecognizer
from .generic.url_recognizer import UrlRecognizer
from .generic.zip_code_recognizer import ZipCodeRecognizer

# NER recognizers
from .ner.gliner_recognizer import GLiNERRecognizer

# NLP Engine recognizers
from .nlp_engine_recognizers.spacy_recognizer import SpacyRecognizer
from .nlp_engine_recognizers.stanza_recognizer import StanzaRecognizer
from .third_party.ahds_recognizer import AzureHealthDeidRecognizer

# Third-party recognizers
from .third_party.azure_ai_language import AzureAILanguageRecognizer
from .third_party.azure_openai_langextract_recognizer import (
    AzureOpenAILangExtractRecognizer,
)
from .third_party.basic_langextract_recognizer import BasicLangExtractRecognizer
from .third_party.langextract_recognizer import LangExtractRecognizer

PREDEFINED_RECOGNIZERS = [
    "AgeRecognizer",
    "CertificateRecognizer",
    "CookieRecognizer",
    "PhoneRecognizer",
    "CreditCardRecognizer",
    "CryptoRecognizer",
    "DateRecognizer",
    "EmailRecognizer",
    "EthnicityRecognizer",
    "GenderRecognizer",
    "IpRecognizer",
    "IbanRecognizer",
    "MedicalLicenseRecognizer",
    "UrlRecognizer",
    "ZipCodeRecognizer",
]

NLP_RECOGNIZERS = {
    "spacy": SpacyRecognizer,
    "stanza": StanzaRecognizer,
    "transformers": TransformersRecognizer,
}

__all__ = [
    # US
    "AbaRoutingRecognizer",
    "MedicalLicenseRecognizer",
    "UsBankRecognizer",
    "UsItinRecognizer",
    "UsLicenseRecognizer",
    "UsMbiRecognizer",
    "UsPassportRecognizer",
    "UsSsnRecognizer",
    # Canada
    "CaBankRecognizer",
    "CaDriverLicenseRecognizer",
    "CaGstRecognizer",
    "CaPostalCodeRecognizer",
    "CaSinRecognizer",
    # Mexico
    "MxClabeRecognizer",
    "MxCurpRecognizer",
    "MxDriverLicenseRecognizer",
    "MxPostalCodeRecognizer",
    "MxRfcRecognizer",
    # UK
    "NhsRecognizer",
    "UkDriverLicenseRecognizer",
    "UkNinoRecognizer",
    "UkPostcodeRecognizer",
    "UkSortCodeRecognizer",
    "UkUtrRecognizer",
    # Germany
    "DeDriverLicenseRecognizer",
    "DePensionInsuranceRecognizer",
    "DePostalCodeRecognizer",
    "DeTaxNumberRecognizer",
    # France
    "FrDriverLicenseRecognizer",
    "FrInseeRecognizer",
    "FrPostalCodeRecognizer",
    "FrSpiRecognizer",
    # Saudi Arabia
    "SaNationalIdRecognizer",
    "SaPostalCodeRecognizer",
    "SaTinRecognizer",
    # UAE
    "AeDriverLicenseRecognizer",
    "AeEmiratesIdRecognizer",
    "AePostalCodeRecognizer",
    "AeTrnRecognizer",
    # South Africa
    "ZaDriverLicenseRecognizer",
    "ZaIdRecognizer",
    "ZaPostalCodeRecognizer",
    "ZaTaxNumberRecognizer",
    # Japan
    "JpBankRecognizer",
    "JpCorporateNumberRecognizer",
    "JpDriverLicenseRecognizer",
    "JpMyNumberRecognizer",
    "JpPostalCodeRecognizer",
    # India
    "InAadhaarRecognizer",
    "InDriverLicenseRecognizer",
    "InGstinRecognizer",
    "InIfscRecognizer",
    "InPanRecognizer",
    "InPassportRecognizer",
    "InPinCodeRecognizer",
    "InVehicleRegistrationRecognizer",
    "InVoterRecognizer",
    # Australia
    "AuAbnRecognizer",
    "AuAcnRecognizer",
    "AuBsbRecognizer",
    "AuDriverLicenseRecognizer",
    "AuMedicareRecognizer",
    "AuPostcodeRecognizer",
    "AuTfnRecognizer",
    # Singapore
    "SgBankRecognizer",
    "SgFinRecognizer",
    "SgPassportRecognizer",
    "SgPostalCodeRecognizer",
    "SgUenRecognizer",
    # Malaysia
    "MyBankRecognizer",
    "MyIncomeTaxRecognizer",
    "MyNricRecognizer",
    "MyPostalCodeRecognizer",
    # Generic
    "AgeRecognizer",
    "CertificateRecognizer",
    "CookieRecognizer",
    "CreditCardRecognizer",
    "CryptoRecognizer",
    "DateRecognizer",
    "EmailRecognizer",
    "EthnicityRecognizer",
    "GenderRecognizer",
    "IbanRecognizer",
    "IpRecognizer",
    "MacAddressRecognizer",
    "PhoneRecognizer",
    "UrlRecognizer",
    "ZipCodeRecognizer",
    # Other existing
    "EsNifRecognizer",
    "EsNieRecognizer",
    "FiPersonalIdentityCodeRecognizer",
    "ItDriverLicenseRecognizer",
    "ItFiscalCodeRecognizer",
    "ItVatCodeRecognizer",
    "ItIdentityCardRecognizer",
    "ItPassportRecognizer",
    "KrBrnRecognizer",
    "KrRrnRecognizer",
    "KrDriverLicenseRecognizer",
    "KrFrnRecognizer",
    "KrPassportRecognizer",
    "PlPeselRecognizer",
    "ThTninRecognizer",
    # NLP/NER
    "SpacyRecognizer",
    "StanzaRecognizer",
    "TransformersRecognizer",
    "GLiNERRecognizer",
    "NLP_RECOGNIZERS",
    # Third-party
    "AzureAILanguageRecognizer",
    "AzureHealthDeidRecognizer",
    "LangExtractRecognizer",
    "AzureOpenAILangExtractRecognizer",
    "BasicLangExtractRecognizer",
]