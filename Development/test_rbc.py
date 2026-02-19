"""
Test Tavily for Royal Bank of Canada
"""
import os
from dotenv import load_dotenv

load_dotenv()

from utility.TavilyCountrySearch import TavilyCountrySearch

def test_rbc():
    print("=" * 80)
    print("Testing: Royal Bank of Canada")
    print("Website: https://www.rbcroyalbank.com")
    print("=" * 80)
    
    try:
        tavily = TavilyCountrySearch()
        
        result = tavily.search_prospect_country(
            prospect_name="Royal Bank of Canada"
        )
        
        print(f"\nDetected Country: {result.country or 'NOT DETECTED'}")
        print(f"Confidence: {result.confidence}")
        print(f"In Supported List: {result.matched_from_list}")
        print(f"Source: {result.source or 'N/A'}")
        
        if result.raw_answer:
            print(f"\nTavily Answer:")
            print(f"{result.raw_answer}")
        
        if result.country == "Canada":
            print(f"\n[SUCCESS] Correctly detected Canada")
        else:
            print(f"\n[FAILED] Expected Canada, got {result.country or 'NOT DETECTED'}")
            
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_rbc()
