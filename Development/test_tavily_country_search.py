"""
Test script for Tavily Country Search
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utility.TavilyCountrySearch import (
    TavilyCountrySearch,
    detect_prospect_country,
    SUPPORTED_COUNTRIES
)


def test_country_search():
    """Test country search functionality"""
    
    print("=" * 80)
    print("TAVILY COUNTRY SEARCH TEST")
    print("=" * 80)
    
    # Display supported countries
    print("\nSupported Countries:")
    for idx, country in enumerate(SUPPORTED_COUNTRIES, 1):
        print(f"  {idx}. {country}")
    
    print("\n" + "=" * 80)
    
    # Test cases
    test_cases = [
        {
            "prospect_name": "Microsoft",
            "additional_context": "Technology company"
        },
        {
            "prospect_name": "Toyota",
            "additional_context": "Automotive manufacturer"
        },
        {
            "prospect_name": "Siemens",
            "additional_context": None
        },
        {
            "prospect_name": "Tata Consultancy Services",
            "additional_context": "IT services company"
        },
        {
            "prospect_name": "Emirates Airlines",
            "additional_context": "Airline company"
        }
    ]
    
    # Initialize Tavily search
    try:
        tavily_search = TavilyCountrySearch()
        print("\n✓ Tavily Country Search initialized successfully")
    except Exception as e:
        print(f"\n✗ Failed to initialize Tavily Country Search: {str(e)}")
        print("\nMake sure TAVILY_API_KEY is set in your .env file")
        return
    
    # Run test cases
    print("\n" + "=" * 80)
    print("RUNNING TEST CASES")
    print("=" * 80)
    
    for idx, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {idx}:")
        print(f"  Prospect: {test_case['prospect_name']}")
        if test_case['additional_context']:
            print(f"  Context: {test_case['additional_context']}")
        
        try:
            result = tavily_search.search_prospect_country(
                prospect_name=test_case['prospect_name'],
                additional_context=test_case['additional_context']
            )
            
            print(f"\n  Results:")
            print(f"    Country: {result.country or 'Not detected'}")
            print(f"    Confidence: {result.confidence}")
            print(f"    Source: {result.source or 'N/A'}")
            print(f"    In Supported List: {'Yes' if result.matched_from_list else 'No'}")
            if result.raw_answer:
                # Show more of the raw answer for debugging
                answer_preview = result.raw_answer[:300] if len(result.raw_answer) > 300 else result.raw_answer
                print(f"    Tavily Response: {answer_preview}")
                if len(result.raw_answer) > 300:
                    print(f"    ... (truncated, full length: {len(result.raw_answer)} chars)")
            else:
                print(f"    Tavily Response: No answer provided")
            
            if result.country and result.matched_from_list:
                print(f"    ✓ Successfully detected supported country")
            elif result.country and not result.matched_from_list:
                print(f"    ⚠ Country detected but not in supported list")
            else:
                print(f"    ✗ Country not detected")
                
        except Exception as e:
            print(f"    ✗ Error: {str(e)}")
            import traceback
            traceback.print_exc()
        
        print("-" * 80)
    
    print("\n" + "=" * 80)
    print("TEST COMPLETED")
    print("=" * 80)


def test_convenience_function():
    """Test convenience function"""
    print("\n\nTesting convenience function...")
    
    try:
        result = detect_prospect_country("Apple Inc", "Technology company")
        print(f"\nResult for Apple Inc:")
        print(f"  Country: {result.country}")
        print(f"  Confidence: {result.confidence}")
        print(f"  Matched: {result.matched_from_list}")
        if result.raw_answer:
            print(f"  Tavily Answer: {result.raw_answer}")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    # Check if API key is set
    if not os.getenv("TAVILY_API_KEY"):
        print("ERROR: TAVILY_API_KEY not found in environment variables")
        print("\nPlease set TAVILY_API_KEY in your .env file:")
        print("  TAVILY_API_KEY=your_api_key_here")
        sys.exit(1)
    
    # Run tests
    test_country_search()
    test_convenience_function()
