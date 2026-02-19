"""
Test Tavily Country Detection for AMER Companies
Run from: dbx-backend/Development/
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

from utility.TavilyCountrySearch import TavilyCountrySearch

def test_amer_companies():
    """Test Tavily detection for AMER region companies"""
    
    print("=" * 80)
    print("TAVILY COUNTRY DETECTION TEST - AMER REGION")
    print("=" * 80)
    
    test_cases = [
        {"company": "Shopify", "expected": "Canada"},
        {"company": "Cemex", "expected": "Mexico"},
        {"company": "Microsoft", "expected": "United States"}
    ]
    
    if not os.getenv("TAVILY_API_KEY"):
        print("\n[ERROR] TAVILY_API_KEY not found in environment")
        return
    
    try:
        tavily = TavilyCountrySearch()
        print("\n[OK] Tavily initialized\n")
    except Exception as e:
        print(f"\n[ERROR] Failed to initialize: {e}")
        return
    
    results = []
    
    for test in test_cases:
        print(f"\n{'='*80}")
        print(f"Testing: {test['company']} (Expected: {test['expected']})")
        print(f"{'='*80}")
        
        try:
            result = tavily.search_prospect_country(prospect_name=test['company'])
            
            detected = result.country or "NOT DETECTED"
            success = detected == test['expected']
            
            print(f"Detected: {detected}")
            print(f"Confidence: {result.confidence}")
            print(f"Matched: {result.matched_from_list}")
            
            if result.raw_answer:
                print(f"Answer: {result.raw_answer[:300]}")
            
            print(f"\n{'[SUCCESS]' if success else '[FAILED]'}")
            
            results.append({
                'company': test['company'],
                'expected': test['expected'],
                'detected': detected,
                'success': success
            })
            
        except Exception as e:
            print(f"\n[ERROR] {e}")
            results.append({
                'company': test['company'],
                'expected': test['expected'],
                'detected': 'ERROR',
                'success': False
            })
    
    print(f"\n\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    
    for r in results:
        status = "[OK]" if r['success'] else "[FAIL]"
        print(f"{status} {r['company']:15} | Expected: {r['expected']:15} | Detected: {r['detected']}")
    
    success_count = sum(1 for r in results if r['success'])
    print(f"\nSuccess Rate: {success_count}/{len(results)}")


if __name__ == "__main__":
    test_amer_companies()
