"""India-specific recognizers."""

from .in_aadhaar_recognizer import InAadhaarRecognizer
from .in_driver_license_recognizer import InDriverLicenseRecognizer
from .in_gstin_recognizer import InGstinRecognizer
from .in_ifsc_recognizer import InIfscRecognizer
from .in_pan_recognizer import InPanRecognizer
from .in_passport_recognizer import InPassportRecognizer
from .in_pin_code_recognizer import InPinCodeRecognizer
from .in_vehicle_registration_recognizer import InVehicleRegistrationRecognizer
from .in_voter_recognizer import InVoterRecognizer

__all__ = [
    "InAadhaarRecognizer",
    "InDriverLicenseRecognizer",
    "InGstinRecognizer",
    "InIfscRecognizer",
    "InPanRecognizer",
    "InPinCodeRecognizer",
    "InVoterRecognizer",
    "InVehicleRegistrationRecognizer",
    "InPassportRecognizer",
]
