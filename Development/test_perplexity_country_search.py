"""
Test script for Perplexity Country Search
Tests country detection for various companies
"""
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env.example
load_dotenv()

from utility.PerplexityCountrySearch import PerplexityCountrySearch
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def test_country_detection():
    """Test country detection for various companies"""
    
    # Test companies from different countries
    test_cases = [
        ("Microsoft", None, "United States"),
        ("Royal Bank of Canada", None, "Canada"),
        ("Telmex", None, "Mexico"),
        ("BP", None, "United Kingdom"),
        ("Siemens", None, "Germany"),
        ("TotalEnergies", None, "France"),
        ("Emirates Airlines", None, "UAE"),
        ("Saudi Aramco", None, "Saudi Arabia"),
        ("Sasol", None, "South Africa"),
        ("Sony", None, "Japan"),
        ("Tata Consultancy Services", None, "India"),
        ("Qantas", None, "Australia"),
        ("Singapore Airlines", None, "Singapore"),
        ("Petronas", None, "Malaysia"),
    ]
    
    print("\n" + "="*80)
    print("PERPLEXITY COUNTRY SEARCH TEST")
    print("="*80 + "\n")
    
    # Check if API key is set
    api_key = os.getenv("PERPLEXITY_API_KEY")
    if not api_key or api_key == "your_perplexity_api_key_here":
        print("ERROR: PERPLEXITY_API_KEY not found in environment variables")
        print("\nPlease set PERPLEXITY_API_KEY in your .env file:")
        print("  PERPLEXITY_API_KEY=your_api_key_here")
        sys.exit(1)
    
    print(f"✓ API Key found: {api_key[:10]}...{api_key[-4:]}\n")
    
    # Initialize Perplexity Country Search
    try:
        perplexity = PerplexityCountrySearch()
        print(f"✓ Perplexity Country Search initialized")
        print(f"✓ Supported countries: {len(perplexity.get_supported_countries())}")
        print()
    except Exception as e:
        print(f"\n✗ Failed to initialize Perplexity Country Search: {str(e)}")
        print("\nMake sure PERPLEXITY_API_KEY is set in your .env file")
        return
    
    # Test each company
    results = []
    for company_name, context, expected_country in test_cases:
        print(f"\n{'─'*80}")
        print(f"Testing: {company_name}")
        print(f"Expected: {expected_country}")
        print(f"{'─'*80}")
        
        try:
            result = perplexity.search_prospect_country(company_name, context)
            
            detected = result.country or "Not detected"
            confidence = result.confidence
            matched = "✓" if result.matched_from_list else "✗"
            correct = "✓" if result.country == expected_country else "✗"
            
            print(f"\nDetected Country: {detected}")
            print(f"Confidence: {confidence}")
            print(f"Matched from list: {matched}")
            print(f"Correct: {correct}")
            
            if result.source:
                print(f"Source: {result.source}")
            
            if result.raw_answer:
                print(f"Raw answer: {result.raw_answer[:200]}...")
            
            results.append({
                "company": company_name,
                "expected": expected_country,
                "detected": detected,
                "confidence": confidence,
                "correct": result.country == expected_country
            })
            
        except Exception as e:
            print(f"\n✗ Error: {str(e)}")
            results.append({
                "company": company_name,
                "expected": expected_country,
                "detected": "Error",
                "confidence": "none",
                "correct": False
            })
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80 + "\n")
    
    correct_count = sum(1 for r in results if r["correct"])
    total_count = len(results)
    accuracy = (correct_count / total_count * 100) if total_count > 0 else 0
    
    print(f"Total Tests: {total_count}")
    print(f"Correct: {correct_count}")
    print(f"Incorrect: {total_count - correct_count}")
    print(f"Accuracy: {accuracy:.1f}%\n")
    
    # Detailed results table
    print(f"{'Company':<35} {'Expected':<20} {'Detected':<20} {'Confidence':<12} {'Result'}")
    print("─" * 100)
    
    for r in results:
        status = "✓" if r["correct"] else "✗"
        print(f"{r['company']:<35} {r['expected']:<20} {r['detected']:<20} {r['confidence']:<12} {status}")
    
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    test_country_detection()
