from typing import Dict, List, Any, Tuple, TypedDict, Annotated, Literal, Optional
import json
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

# Import utility functions
from backend.utils import load_frame_data, extract_frame_elements, get_few_shot_prompts, get_language_specific_info

# Define state type
class AgentState(TypedDict):
    messages: List[Any]
    frame_data: Dict[str, Any]
    source_text: str
    source_language: Literal["English", "Japanese"]
    target_language: Literal["English", "Japanese"]
    frame_elements: List[Dict[str, Any]]
    translation_result: Optional[str]
    frame_analysis: Optional[Dict[str, Any]]

# Create LLM instance
def get_llm():
    import os
    from dotenv import load_dotenv
    import sys
    
    # Load environment variables
    load_dotenv()
    
    # Get model configuration
    model_name = os.getenv("DEFAULT_MODEL", "deepseek-chat")
    
    # Check if using DeepSeek or OpenAI
    if "deepseek" in model_name.lower():
        try:
            # Use the official import pattern for DeepSeek
            try:
                from langchain_deepseek import ChatDeepSeek
                print(f"Successfully imported ChatDeepSeek from langchain_deepseek")
                return ChatDeepSeek(
                    model=model_name,
                    temperature=0.1
                )
            except (ImportError, AttributeError) as e:
                print(f"Import attempt failed: {str(e)}")
                print(f"Installed packages in site-packages directory:")
                import os, sys
                site_packages = next((p for p in sys.path if p.endswith('site-packages')), None)
                if site_packages:
                    for pkg in os.listdir(site_packages):
                        if 'deepseek' in pkg.lower() or 'langchain' in pkg.lower():
                            print(f"  - {pkg}")
                
                raise ImportError(f"Could not import ChatDeepSeek from langchain_deepseek. Please install the package using: pip install langchain-deepseek. Error: {str(e)}")
        except ImportError as e:
            error_message = f"""
ERROR: DeepSeek integration not found. Please install the required packages:

    pip install langchain-deepseek
    pip install langchain-community

If you've already installed these packages and still see this error, 
you may need to check your Python environment or try:

    pip install --upgrade langchain-deepseek langchain-community

Error details: {str(e)}
"""
            print(error_message, file=sys.stderr)
            raise ImportError(error_message)
    else:
        # Using OpenAI
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError(
                "OpenAI API key not found. Please set OPENAI_API_KEY in your .env file, "
                "or change DEFAULT_MODEL to a DeepSeek model."
            )
        return ChatOpenAI(
            model=model_name,
            temperature=0.1
        )

# Create system prompt
def create_system_prompt(frame_data: Dict[str, Any]) -> str:
    frame_name = frame_data.get("frame_name", "")
    frame_description = frame_data.get("description", "")
    
    system_prompt = f"""You are a professional translation assistant based on Frame semantic understanding.
Your task is to perform high-quality translations between Japanese and English while maintaining consistency in the Frame semantic structure.

You will work with the following Frame:
- Frame name: {frame_name}
- Frame description: {frame_description}

During the translation process, you need to:
1. Identify Frame elements in the source text
2. Ensure the same Frame elements are preserved in the translated text
3. Consider the grammar and cultural aspects of the target language
4. Provide clear and natural translations

Remember, your goal is to create a translation that is both accurate and natural, while maintaining the Frame semantic structure of the original text.
"""
    return system_prompt

# Analyze Frame elements in the source text
def analyze_frame_elements(state: AgentState) -> AgentState:
    llm = get_llm()
    frame_data = state["frame_data"]
    source_text = state["source_text"]
    source_language = state["source_language"]
    frame_elements = state["frame_elements"]
    
    # Get few-shot prompts
    few_shot_prompts = get_few_shot_prompts(frame_data)
    
    # Build prompt
    frame_elements_str = "\n".join([f"- {el['name']}: {el['description']} ({el['type']} element)" for el in frame_elements])
    
    identification_example = ""
    if "identification_prompt" in few_shot_prompts and "expected_response" in few_shot_prompts:
        identification_example = f"""
Example:
Question: {few_shot_prompts['identification_prompt']}
Answer: {json.dumps(few_shot_prompts['expected_response'], ensure_ascii=False, indent=2)}
"""
    
    prompt = f"""Please analyze the following {source_language} text and identify the Frame elements.

Text: {source_text}

Frame elements:
{frame_elements_str}

{identification_example}

Please return the analysis results in JSON format, including each identified Frame element and its corresponding part in the text.
Return only JSON, without any additional explanation.
"""
    
    # Call LLM for analysis
    response = llm.invoke([HumanMessage(content=prompt)])
    
    # Parse JSON response
    try:
        frame_analysis = json.loads(response.content)
    except:
        # If parsing fails, try to extract JSON part
        import re
        json_match = re.search(r'```json\n(.*?)\n```', response.content, re.DOTALL)
        if json_match:
            frame_analysis = json.loads(json_match.group(1))
        else:
            frame_analysis = {"error": "Unable to parse analysis result", "raw_response": response.content}
    
    # Update state
    new_state = state.copy()
    new_state["frame_analysis"] = frame_analysis
    new_state["messages"] = state["messages"] + [
        HumanMessage(content=prompt),
        AIMessage(content=response.content)
    ]
    
    return new_state

# Perform translation
def translate_text(state: AgentState) -> AgentState:
    llm = get_llm()
    frame_data = state["frame_data"]
    source_text = state["source_text"]
    source_language = state["source_language"]
    target_language = state["target_language"]
    frame_analysis = state["frame_analysis"]
    
    # Get target language specific information
    target_language_code = "Japanese" if target_language == "Japanese" else "English"
    language_info = get_language_specific_info(frame_data, target_language_code)
    
    # Get few-shot translation examples
    few_shot_prompts = get_few_shot_prompts(frame_data)
    translation_example = ""
    if "translation_prompt" in few_shot_prompts and "expected_translation" in few_shot_prompts:
        # Format the expected translation to avoid direct JSON output
        expected_translations = few_shot_prompts['expected_translation']
        formatted_examples = []
        
        for lang, translation in expected_translations.items():
            formatted_examples.append(f"{lang}: {translation}")
        
        translation_example = f"""
Translation example:
Original: {few_shot_prompts['translation_prompt']}
Translation examples:
{chr(10).join(formatted_examples)}
"""
    
    # Build language specific information
    language_specific_info = ""
    if language_info:
        lexical_units = language_info.get("lexical_units", [])
        grammatical_notes = language_info.get("grammatical_notes", "")
        cultural_notes = language_info.get("cultural_notes", "")
        
        language_specific_info = f"""
Target language ({target_language}) specific information:
- Lexical units: {', '.join(lexical_units) if lexical_units else 'No specific information'}
- Grammatical notes: {grammatical_notes if grammatical_notes else 'No specific information'}
- Cultural notes: {cultural_notes if cultural_notes else 'No specific information'}
"""
    
    # Build prompt
    frame_analysis_str = json.dumps(frame_analysis, ensure_ascii=False, indent=2)
    
    prompt = f"""Please translate the following {source_language} text to {target_language}, while maintaining consistency of Frame elements.

Source text: {source_text}

Frame analysis results:
{frame_analysis_str}

{language_specific_info}

{translation_example}

Please provide an accurate and natural translation, ensuring all Frame elements from the original text are preserved. Also, follow the grammar and cultural conventions of the target language.

IMPORTANT: Return ONLY the translation result as plain text, without any JSON formatting, without any additional explanation, and without annotations or markup.
"""
    
    # Call LLM for translation
    response = llm.invoke([HumanMessage(content=prompt)])
    
    # Update state
    new_state = state.copy()
    new_state["translation_result"] = response.content.strip()
    new_state["messages"] = state["messages"] + [
        HumanMessage(content=prompt),
        AIMessage(content=response.content)
    ]
    
    return new_state

# Create workflow graph
def create_workflow(frame_path: str):
    # Load Frame data
    frame_data = load_frame_data(frame_path)
    frame_elements = extract_frame_elements(frame_data)
    
    # Create workflow graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("analyze_frame", analyze_frame_elements)
    workflow.add_node("translate", translate_text)
    
    # Set edges
    workflow.add_edge("analyze_frame", "translate")
    workflow.add_edge("translate", END)
    
    # Set entry point
    workflow.set_entry_point("analyze_frame")
    
    # Compile workflow
    return workflow.compile()

# Execute translation
def run_translation(
    source_text: str,
    source_language: Literal["English", "Japanese"],
    target_language: Literal["English", "Japanese"],
    frame_path: str
) -> Dict[str, Any]:
    # Load Frame data
    frame_data = load_frame_data(frame_path)
    frame_elements = extract_frame_elements(frame_data)
    
    # Create workflow
    app = create_workflow(frame_path)
    
    # Create initial state
    initial_state = {
        "messages": [SystemMessage(content=create_system_prompt(frame_data))],
        "frame_data": frame_data,
        "source_text": source_text,
        "source_language": source_language,
        "target_language": target_language,
        "frame_elements": frame_elements,
        "translation_result": None,
        "frame_analysis": None
    }
    
    # Execute workflow
    result = app.invoke(initial_state)
    
    # Return results
    return {
        "source_text": source_text,
        "source_language": source_language,
        "target_language": target_language,
        "translation": result["translation_result"],
        "frame_analysis": result["frame_analysis"]
    }
