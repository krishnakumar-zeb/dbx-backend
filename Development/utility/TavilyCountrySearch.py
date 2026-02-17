"""
Tavily Country Search Utility
Uses Tavily API to detect prospect's country from available information
"""
from typing import Optional, List
import requests
import os
import logging
from utility.exceptions import PIIException
from utility.models import (
    TavilySearchRequest,
    TavilySearchResponse,
    CountryDetectionResult
)

logger = logging.getLogger(__name__)

# Supported countries list
SUPPORTED_COUNTRIES = [
    "Canada",
    "Mexico",
    "United States",
    "United Kingdom",
    "Germany",
    "France",
    "UAE",
    "Saudi Arabia",
    "South Africa",
    "Japan",
    "India",
    "Australia",
    "Singapore",
    "Malaysia"
]


class TavilyCountrySearch:
    """Utility class for detecting prospect country using Tavily API"""
    
    def __init__(self):
        """Initialize Tavily Country Search"""
        self.api_key = os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise PIIException("TAVILY_API_KEY not found in environment variables", code=500)
        
        self.api_url = "https://api.tavily.com/search"
        self.supported_countries = SUPPORTED_COUNTRIES
    
    def search_prospect_country(
        self,
        prospect_name: str,
        additional_context: Optional[str] = None
    ) -> CountryDetectionResult:
        """
        Search for prospect's country using Tavily API
        
        Args:
            prospect_name: Name of the prospect/company
            additional_context: Additional context for better search results
            
        Returns:
            CountryDetectionResult with detected country and confidence
        """
        try:
            # Build search query
            query = self._build_search_query(prospect_name, additional_context)
            
            logger.info(f"Searching country for prospect: {prospect_name}")
            
            # Create search request
            search_request = TavilySearchRequest(
                query=query,
                search_depth="basic",
                max_results=5
            )
            
            # Execute Tavily search
            search_response = self._execute_tavily_search(search_request)
            
            # Extract country from results
            country_result = self._extract_country_from_results(
                search_response,
                prospect_name
            )
            
            logger.info(
                f"Country detection result for {prospect_name}: "
                f"{country_result.country} (confidence: {country_result.confidence})"
            )
            
            return country_result
            
        except Exception as e:
            logger.error(f"Error in country search: {str(e)}", exc_info=True)
            # Return result with no country found
            return CountryDetectionResult(
                country=None,
                confidence="none",
                source=None,
                matched_from_list=False
            )
    
    def _build_search_query(
        self,
        prospect_name: str,
        additional_context: Optional[str] = None
    ) -> str:
        """
        Build search query for country detection
        
        Args:
            prospect_name: Prospect name
            additional_context: Additional context
            
        Returns:
            Search query string
        """
        # Create country list string
        countries_str = ", ".join(self.supported_countries)
        
        # Build simpler, more direct query
        if additional_context:
            query = (
                f"Which country is {prospect_name} headquartered in? "
                f"Is it one of these countries: {countries_str}?"
                f"The country name should match the exact names in the given list if found to be the same"
            )
        else:
            query = (
                f"Which country is {prospect_name} headquartered in? "
                f"Is it one of these countries: {countries_str}?"
                f"The country name should match the exact names in the given list if found to be the same"
            )
        
        return query
    
    def _execute_tavily_search(
        self,
        search_request: TavilySearchRequest
    ) -> TavilySearchResponse:
        """
        Execute Tavily API search
        
        Args:
            search_request: Validated search request
            
        Returns:
            TavilySearchResponse with search results
        """
        try:
            logger.info(f"=== TAVILY API REQUEST ===")
            logger.info(f"Query: {search_request.query}")
            logger.info(f"Search Depth: {search_request.search_depth}")
            logger.info(f"Max Results: {search_request.max_results}")
            
            headers = {
                "Content-Type": "application/json"
            }
            
            payload = {
                "api_key": self.api_key,
                "query": search_request.query,
                "search_depth": search_request.search_depth,
                "max_results": search_request.max_results,
                "include_answer": True
            }
            
            if search_request.include_domains:
                payload["include_domains"] = search_request.include_domains
            
            if search_request.exclude_domains:
                payload["exclude_domains"] = search_request.exclude_domains
            
            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            response.raise_for_status()
            
            data = response.json()
            
            logger.info(f"=== TAVILY API RESPONSE ===")
            logger.info(f"Response Status: {response.status_code}")
            logger.info(f"Answer Provided: {'Yes' if data.get('answer') else 'No'}")
            if data.get('answer'):
                logger.info(f"Answer: {data.get('answer')}")
            logger.info(f"Number of Results: {len(data.get('results', []))}")
            
            # Log first few results for debugging
            for idx, result in enumerate(data.get('results', [])[:3]):
                logger.info(f"Result {idx+1}:")
                logger.info(f"  Title: {result.get('title', 'N/A')}")
                logger.info(f"  URL: {result.get('url', 'N/A')}")
                logger.info(f"  Content Preview: {result.get('content', 'N/A')[:150]}...")
            
            # Validate response with Pydantic
            return TavilySearchResponse(
                query=data.get("query", search_request.query),
                results=data.get("results", []),
                answer=data.get("answer"),
                images=data.get("images"),
                response_time=data.get("response_time")
            )
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Tavily API request failed: {str(e)}")
            raise PIIException(f"Tavily search failed: {str(e)}", code=503)
        except Exception as e:
            logger.error(f"Error executing Tavily search: {str(e)}")
            raise PIIException(f"Tavily search error: {str(e)}", code=500)
    
    def _extract_country_from_results(
        self,
        search_response: TavilySearchResponse,
        prospect_name: str
    ) -> CountryDetectionResult:
        """
        Extract country from Tavily search results
        Relies on Tavily's answer field first, then checks results as fallback
        
        Args:
            search_response: Tavily search response
            prospect_name: Prospect name for context
            
        Returns:
            CountryDetectionResult
        """
        detected_country = None
        confidence = "none"
        source = None
        raw_answer = None
        
        logger.info(f"=== PROCESSING TAVILY RESPONSE FOR: {prospect_name} ===")
        
        # First priority: Use Tavily's answer field
        if search_response.answer:
            raw_answer = search_response.answer
            logger.info(f"Processing Tavily answer: {raw_answer}")
            
            # Check if any supported country is mentioned in the answer
            detected_country = self._match_country_from_answer(raw_answer)
            
            if detected_country:
                confidence = "high"
                source = "tavily_answer"
                logger.info(f"✓ Country MATCHED from answer: {detected_country}")
            else:
                # Tavily provided an answer but no supported country found
                confidence = "low"
                logger.warning(f"✗ No supported country found in answer")
        else:
            logger.info(f"No answer fvily results for {prospect_name} (no answer or country not found in answer)")
            
            for idx, result in enumerate(search_response.results):
                # Check title first
                if result.get("title"):
                    country = self._match_country_from_answer(result["title"])
                    if country:
                        detected_country = country
                        confidence = "high" if idx == 0 else "medium"
                        source = result.get("url", "tavily_results")
                        raw_answer = result["title"]
                    logger.info(f"  Title: {result['title']}")
                    country = self._match_country_from_answer(result["title"])
                    if country:
                        detected_country = country
                        confidence = "high" if idx == 0 else "medium"
                        source = result.get("url", "tavily_results")
                        raw_answer = result["title"]
                        logger.info(f"  ✓ Country MATCHED from title: {detected_country}")
                        break
                    else:
                        logger.info(f"  ✗ No country match in title")
                
                # Check content if not found in title
                if result.get("content"):
                    content_preview = result["content"][:200]
                    logger.info(f"  Content preview: {content_preview}...")
                    country = self._match_country_from_answer(result["content"])
                    if country:
                        detected_country = country
        
        if not detected_country:
            logger.warning(f"=== FINAL RESULT: No country detected for {prospect_name} ===")
        else:
            logger.info(f"=== FINAL RESULT: {detected_country} (confidence: {confidence}) ===")
        
        # Validate if country is in supported list
        matched_from_list = detected_country in self.supported_countries if detected_country else False
        
        return CountryDetectionResult(
            country=detected_country,
            confidence=confidence,
            source=source,
            matched_from_list=matched_from_list,
            raw_answer=raw_answer
        )
    
    def _match_country_from_answer(self, answer: str) -> Optional[str]:
        """
        Match country from Tavily answer against supported countries list
        
        Args:
            answer: Tavily answer text
            
        Returns:
            Country name if found, None otherwise
        """
        if not answer:
            return None
        
        answer_lower = answer.lower()
        
        # Check each supported country (exact match or common variations)
        for country in self.supported_countries:
            country_lower = country.lower()
            
            # Direct match
            if country_lower in answer_lower:
                return country
            
            # Handle special cases and abbreviations only
            if country == "United States":
                if any(term in answer_lower for term in ["usa", "u.s.", " us ", " us.", "america", "american"]):
                    return country
            
            elif country == "United Kingdom":
                if any(term in answer_lower for term in ["uk", "u.k.", "britain", "great britain", "british"]):
                    return country
            
            elif country == "UAE":
                if any(term in answer_lower for term in ["uae", "u.a.e.", "united arab emirates", "emirates"]):
                    return country
            
            elif country == "Saudi Arabia":
                if any(term in answer_lower for term in ["saudi", "ksa"]):
                    return country
        
        return None
    
    def get_supported_countries(self) -> List[str]:
        """
        Get list of supported countries
        
        Returns:
            List of country names
        """
        return self.supported_countries.copy()


# Convenience function for quick country detection
def detect_prospect_country(
    prospect_name: str,
    additional_context: Optional[str] = None
) -> CountryDetectionResult:
    """
    Convenience function to detect prospect country
    
    Args:
        prospect_name: Name of the prospect/company
        additional_context: Additional context for search
        
    Returns:
        CountryDetectionResult
    """
    tavily_search = TavilyCountrySearch()
    return tavily_search.search_prospect_country(prospect_name, additional_context)
