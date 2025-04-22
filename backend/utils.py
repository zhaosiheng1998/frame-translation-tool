import json
import os
import glob
from typing import Dict, List, Any, Optional, Tuple

def load_frame_data(frame_path: str) -> Dict[str, Any]:
    """
    Load Frame data from a specific file
    
    Args:
        frame_path: Path to the Frame JSON file
        
    Returns:
        Loaded Frame data
    """
    with open(frame_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def list_available_frames() -> List[Dict[str, str]]:
    """
    List all available frames in the frames directory
    
    Returns:
        List of dictionaries containing frame information (id, name, path)
    """
    frames_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frames')
    frame_files = glob.glob(os.path.join(frames_dir, '*-frame.json'))
    
    frames = []
    for frame_file in frame_files:
        try:
            frame_data = load_frame_data(frame_file)
            frames.append({
                'id': frame_data.get('frame_id', ''),
                'name': frame_data.get('frame_name', ''),
                'path': frame_file,
                'description': frame_data.get('description', '')[:100] + '...' if len(frame_data.get('description', '')) > 100 else frame_data.get('description', '')
            })
        except Exception as e:
            print(f"Error loading frame file {frame_file}: {str(e)}")
    
    return frames

def get_frame_by_name(frame_name: str) -> Tuple[Dict[str, Any], str]:
    """
    Get frame data by frame name
    
    Args:
        frame_name: Name of the frame to find
        
    Returns:
        Tuple of (frame data, frame path)
        
    Raises:
        ValueError: If frame not found
    """
    frames = list_available_frames()
    for frame in frames:
        if frame['name'].lower() == frame_name.lower():
            frame_path = frame['path']
            frame_data = load_frame_data(frame_path)
            return frame_data, frame_path
    
    raise ValueError(f"Frame '{frame_name}' not found")

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
