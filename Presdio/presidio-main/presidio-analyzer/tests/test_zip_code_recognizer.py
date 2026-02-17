import pytest

from presidio_analyzer.predefined_recognizers import ZipCodeRecognizer
from tests import assert_result


@pytest.fixture(scope="module")
def recognizer():
    return ZipCodeRecognizer()


@pytest.fixture(scope="module")
def entities():
    return ["ZIP_CODE"]


@pytest.mark.parametrize(
    "text, expected_len, expected_positions, expected_score_ranges",
    [
        # fmt: off
        # Valid 5-digit ZIP codes
        ("90210", 1, ((0, 5),), ((0.5, 0.5),),),
        ("My address is 10001", 1, ((14, 19),), ((0.5, 0.5),),),
        ("Send to 12345 please", 1, ((8, 13),), ((0.5, 0.5),),),
        
        # Valid ZIP+4 format
        ("90210-1234", 1, ((0, 10),), ((0.5, 0.5),),),
        ("Mail to 10001-5555", 1, ((8, 18),), ((0.5, 0.5),),),
        
        # Multiple ZIP codes
        ("From 90210 to 10001", 2, ((5, 10), (14, 19),), ((0.5, 0.5), (0.5, 0.5),),),
        ("90210-1234 and 10001-5555", 2, ((0, 10), (15, 25),), ((0.5, 0.5), (0.5, 0.5),),),
        
        # With context words (should boost score)
        ("ZIP code: 90210", 1, ((10, 15),), ((0.5, 1.0),),),
        ("Postal code 12345", 1, ((12, 17),), ((0.5, 1.0),),),
        
        # Invalid - all same digits
        ("00000", 0, (), (),),
        ("11111", 0, (), (),),
        
        # Invalid - starts with 00
        ("00123", 0, (), (),),
        ("00999", 0, (), (),),
        
        # Invalid - wrong length
        ("1234", 0, (), (),),
        ("123456", 0, (), (),),
        
        # Invalid - not a ZIP code context
        ("The year 12345 was long ago", 0, (), (),),
        
        # Edge cases
        ("", 0, (), (),),
        ("abcde", 0, (), (),),
        # fmt: on
    ],
)
def test_when_zip_codes_in_text_then_all_zip_codes_found(
    text,
    expected_len,
    expected_positions,
    expected_score_ranges,
    recognizer,
    entities,
):
    results = recognizer.analyze(text, entities)
    assert len(results) == expected_len
    for i, (res, (expected_start, expected_end), (expected_score_min, expected_score_max)) in enumerate(
        zip(results, expected_positions, expected_score_ranges)
    ):
        assert res.start == expected_start, f"Result {i}: Expected start {expected_start}, got {res.start}"
        assert res.end == expected_end, f"Result {i}: Expected end {expected_end}, got {res.end}"
        assert expected_score_min <= res.score <= expected_score_max, \
            f"Result {i}: Expected score between {expected_score_min} and {expected_score_max}, got {res.score}"
        assert res.entity_type == "ZIP_CODE"


def test_when_zip_code_with_context_then_score_is_higher(recognizer, entities):
    """Test that context words increase the confidence score."""
    text_without_context = "90210"
    text_with_context = "ZIP code: 90210"
    
    results_without = recognizer.analyze(text_without_context, entities)
    results_with = recognizer.analyze(text_with_context, entities)
    
    assert len(results_without) == 1
    assert len(results_with) == 1
    assert results_with[0].score > results_without[0].score


def test_when_invalid_zip_then_not_detected(recognizer, entities):
    """Test that invalid ZIP codes are properly rejected."""
    invalid_zips = [
        "00000",  # All zeros
        "11111",  # All same digit
        "00123",  # Starts with 00
        "1234",   # Too short
        "123456", # Too long (not ZIP+4 format)
    ]
    
    for invalid_zip in invalid_zips:
        results = recognizer.analyze(invalid_zip, entities)
        assert len(results) == 0, f"Invalid ZIP {invalid_zip} should not be detected"
