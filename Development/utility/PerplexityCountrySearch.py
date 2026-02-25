"""
Perplexity Country Search Utility
Uses Perplexity API to detect prospect's country from available information
"""
from typing import Optional, List
import requests
import os
import logging
from utility.exceptions import PIIException
from utility.models import CountryDetectionResult

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


class PerplexityCountrySearch:
    """Utility class for detecting prospect country using Perplexity API"""
    
    def __init__(self):
        """Initialize Perplexity Country Search"""
        self.api_key = os.getenv("PERPLEXITY_API_KEY")
        if not self.api_key:
            raise PIIException("PERPLEXITY_API_KEY not found in environment variables", code=500)
        
        # Use Sonar API endpoint (chat completions with web search)
        self.api_url = "https://api.perplexity.ai/chat/completions"
        self.model = os.getenv("PERPLEXITY_MODEL", "sonar-pro")
        self.supported_countries = SUPPORTED_COUNTRIES
    
    def search_prospect_country(
        self,
        prospect_name: str,
        additional_context: Optional[str] = None
    ) -> CountryDetectionResult:
        """
        Search for prospect's country using Perplexity API
        
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
            
            # Execute Perplexity search
            search_response = self._execute_perplexity_search(query)
            
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
        
        # Build query
        query = (
            f"Which country is {prospect_name} headquartered in? "
            f"Is it one of these countries: {countries_str}? "
            f"The country name should match the exact names in the given list if found to be the same"
        )
        
        return query
    
    def _execute_perplexity_search(self, query: str) -> dict:
        """
        Execute Perplexity Sonar API search
        
        Args:
            query: Search query
            
        Returns:
            Dictionary with search results
        """
        try:
            logger.info(f"=== PERPLEXITY SONAR API REQUEST ===")
            logger.info(f"Model: {self.model}")
            logger.info(f"Query: {query}")
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that identifies company headquarters locations. Respond with only the country name from the provided list."
                    },
                    {
                        "role": "user",
                        "content": query
                    }
                ],
                "temperature": 0.1,  # Low temperature for more deterministic results
                "max_tokens": 100    # Short response needed
            }
            
            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            response.raise_for_status()
            
            data = response.json()
            
            logger.info(f"=== PERPLEXITY SONAR API RESPONSE ===")
            logger.info(f"Response Status: {response.status_code}")
            
            # Extract the answer from the response
            if data.get('choices') and len(data['choices']) > 0:
                answer = data['choices'][0].get('message', {}).get('content', '')
                logger.info(f"Perplexity Answer: {answer}")
                
                # Log citations if available
                citations = data.get('citations', [])
                if citations:
                    logger.info(f"Citations: {citations}")
                
                # Return in a format similar to search results
                return {
                    'answer': answer,
                    'citations': citations
                }
            else:
                logger.warning("No answer in Perplexity response")
                return {'answer': None, 'citations': []}
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Perplexity API request failed: {str(e)}")
            raise PIIException(f"Perplexity search failed: {str(e)}", code=503)
        except Exception as e:
            logger.error(f"Error executing Perplexity search: {str(e)}")
            raise PIIException(f"Perplexity search error: {str(e)}", code=500)
    
    def _extract_country_from_results(
        self,
        search_response: dict,
        prospect_name: str
    ) -> CountryDetectionResult:
        """
        Extract country from Perplexity Sonar API response
        Uses the AI-generated answer directly
        
        Args:
            search_response: Perplexity search response
            prospect_name: Prospect name for context
            
        Returns:
            CountryDetectionResult
        """
        detected_country = None
        confidence = "none"
        source = None
        raw_answer = None
        
        logger.info(f"=== PROCESSING PERPLEXITY RESPONSE FOR: {prospect_name} ===")
        
        # Get the answer from Sonar API
        answer = search_response.get('answer')
        citations = search_response.get('citations', [])
        
        if not answer:
            logger.warning(f"No answer from Perplexity for {prospect_name}")
            return CountryDetectionResult(
                country=None,
                confidence="none",
                source=None,
                matched_from_list=False
            )
        
        logger.info(f"Raw Perplexity Answer: '{answer}'")
        raw_answer = answer
        
        # Extract country from the answer
        detected_country = self._match_country_from_text(answer)
        
        if detected_country:
            confidence = "high"
            source = citations[0] if citations else "perplexity_sonar"
            logger.info(f"✓ COUNTRY MATCHED: {detected_country}")
            logger.info(f"  Confidence: {confidence}")
            logger.info(f"  Source: {source}")
        else:
            confidence = "low"
            logger.warning(f"✗ NO SUPPORTED COUNTRY FOUND in answer: '{answer}'")
        
        logger.info(f"=== FINAL RESULT FOR {prospect_name}: {detected_country or 'NOT DETECTED'} ===")
        logger.info("")  # Empty line for readability
        
        # Validate if country is in supported list
        matched_from_list = detected_country in self.supported_countries if detected_country else False
        
        return CountryDetectionResult(
            country=detected_country,
            confidence=confidence,
            source=source,
            matched_from_list=matched_from_list,
            raw_answer=raw_answer
        )
    
    def _match_country_from_text(self, text: str) -> Optional[str]:
        """
        Match country from text against supported countries list
        
        Args:
            text: Text to search for country
            
        Returns:
            Country name if found, None otherwise
        """
        if not text:
            return None
        
        text_lower = text.lower()
        
        # Check each supported country (exact match or common variations)
        for country in self.supported_countries:
            country_lower = country.lower()
            
            # Direct match
            if country_lower in text_lower:
                return country
            
            # Handle special cases and abbreviations
            if country == "United States":
                if any(term in text_lower for term in ["usa", "u.s.", " us ", " us.", "america", "american"]):
                    return country
            
            elif country == "United Kingdom":
                if any(term in text_lower for term in ["uk", "u.k.", "britain", "great britain", "british"]):
                    return country
            
            elif country == "UAE":
                if any(term in text_lower for term in ["uae", "u.a.e.", "united arab emirates", "emirates"]):
                    return country
            
            elif country == "Saudi Arabia":
                if any(term in text_lower for term in ["saudi", "ksa"]):
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
    perplexity_search = PerplexityCountrySearch()
    return perplexity_search.search_prospect_country(prospect_name, additional_context)
