"""
Test Tavily for Mexican companies
"""
import os
from dotenv import load_dotenv

load_dotenv()

from utility.TavilyCountrySearch import TavilyCountrySearch

def test_mexican_companies():
    companies = [
        "Cemex",
        "Telmex", 
        "América Móvil",
        "Pemex",
        "Grupo Bimbo"
    ]
    
    tavily = TavilyCountrySearch()
    
    for company in companies:
        print(f"\n{'='*80}")
        print(f"Testing: {company}")
        print(f"{'='*80}")
        
        try:
            result = tavily.search_prospect_country(prospect_name=company)
            
            detected = result.country or "NOT DETECTED"
            success = detected == "Mexico"
            
            print(f"Detected: {detected}")
            print(f"Confidence: {result.confidence}")
            
            if result.raw_answer:
                print(f"Answer: {result.raw_answer[:200]}")
            
            print(f"{'[SUCCESS]' if success else '[FAILED]'}")
            
        except Exception as e:
            print(f"[ERROR] {e}")

if __name__ == "__main__":
    test_mexican_companies()
