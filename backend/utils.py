import json
import os
from typing import Dict, List, Any, Optional

def load_frame_data(frame_path: str) -> Dict[str, Any]:
    """
    Load Frame data
    
    Args:
        frame_path: Path to the Frame JSON file
        
    Returns:
        Loaded Frame data
    """
    with open(frame_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_frame_elements(frame_data: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Extract all Frame elements from Frame data
    
    Args:
        frame_data: Loaded Frame data
        
    Returns:
        List of Frame elements
    """
    elements = []
    
    # Add core elements
    for element in frame_data.get("frame_elements", {}).get("core_elements", []):
        elements.append({
            "name": element["name"],
            "description": element["description"],
            "type": "core"
        })
    
    # Add non-core elements
    for element in frame_data.get("frame_elements", {}).get("non_core_elements", []):
        elements.append({
            "name": element["name"],
            "description": element["description"],
            "type": "non_core"
        })
    
    return elements

def get_frame_examples(frame_data: Dict[str, Any], language: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Get example sentences for the Frame
    
    Args:
        frame_data: Loaded Frame data
        language: Specified language (if any)
        
    Returns:
        List of example sentences
    """
    examples = frame_data.get("example_sentences", [])
    
    # If language is specified, try to get language-specific examples
    if language and language in frame_data.get("language_specific_variations", {}):
        language_examples = frame_data["language_specific_variations"][language].get("examples", [])
        if language_examples:
            examples = language_examples
    
    return examples

def get_few_shot_prompts(frame_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get Few-shot prompts
    
    Args:
        frame_data: Loaded Frame data
        
    Returns:
        Few-shot prompts
    """
    return frame_data.get("few_shot_prompts", {})

def get_language_specific_info(frame_data: Dict[str, Any], language: str) -> Dict[str, Any]:
    """
    Get language-specific information
    
    Args:
        frame_data: Loaded Frame data
        language: Language code
        
    Returns:
        Language-specific information
    """
    return frame_data.get("language_specific_variations", {}).get(language, {})
