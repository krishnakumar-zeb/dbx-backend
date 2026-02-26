"""
NLP Engine Configuration for Presidio
Configures which NLP model to use for Named Entity Recognition (NER)
"""
from presidio_analyzer.nlp_engine import NlpEngineProvider
import logging

logger = logging.getLogger(__name__)


def get_nlp_engine(engine_type: str = "spacy"):
    """
    Get configured NLP engine for Presidio
    
    Args:
        engine_type: Type of NLP engine to use
            - "spacy": Use spaCy models (default: en_core_web_lg)
            - "spacy_small": Use small spaCy model (en_core_web_sm) - faster but less accurate
    
    Returns:
        Configured NLP engine
    """
    
    if engine_type == "spacy":
        # Use spaCy large model (default Presidio behavior)
        nlp_configuration = {
            "nlp_engine_name": "spacy",
            "models": [
                {
                    "lang_code": "en",
                    "model_name": "en_core_web_lg"
                }
            ],
        }
        logger.info("Using spaCy NLP engine with model: en_core_web_lg")
        
    elif engine_type == "spacy_small":
        # Use spaCy small model (faster, less accurate)
        nlp_configuration = {
            "nlp_engine_name": "spacy",
            "models": [
                {
                    "lang_code": "en",
                    "model_name": "en_core_web_sm"
                }
            ],
        }
        logger.info("Using spaCy NLP engine with model: en_core_web_sm")
        
    else:
        raise ValueError(f"Unknown engine_type: {engine_type}. Use 'spacy' or 'spacy_small'")
    
    # Create NLP engine provider
    provider = NlpEngineProvider(nlp_configuration=nlp_configuration)
    nlp_engine = provider.create_engine()
    
    return nlp_engine


def get_current_model_info(nlp_engine):
    """
    Get information about the currently loaded NLP model
    
    Args:
        nlp_engine: NLP engine instance
        
    Returns:
        Dictionary with model information
    """
    info = {
        "engine_type": nlp_engine.__class__.__name__,
        "models": {}
    }
    
    # Get model information based on engine type
    if hasattr(nlp_engine, 'nlp'):
        # spaCy engine
        for lang_code, nlp in nlp_engine.nlp.items():
            info["models"][lang_code] = {
                "model_name": nlp.meta.get("name", "unknown"),
                "version": nlp.meta.get("version", "unknown"),
                "description": nlp.meta.get("description", ""),
            }
    elif hasattr(nlp_engine, 'models'):
        # Transformers engine
        for model_config in nlp_engine.models:
            lang_code = model_config.get("lang_code", "unknown")
            model_name = model_config.get("model_name", {})
            if isinstance(model_name, dict):
                info["models"][lang_code] = {
                    "spacy_model": model_name.get("spacy", "unknown"),
                    "transformers_model": model_name.get("transformers", "unknown"),
                }
            else:
                info["models"][lang_code] = {
                    "model_name": model_name
                }
    
    return info
