# Frame-based English-Japanese Translation Tool

A semantic understanding translation tool that leverages Frame semantics to provide high-quality translations between English and Japanese. This project demonstrates how to use large language models with frame understanding capabilities to maintain semantic consistency in translations.

## 🌟 Features

- **Frame-based Semantic Understanding**: Uses semantic frames to understand the structure of text
- **Multiple Frame Support**: Includes Commerce_buy, Travel_transportation, and easily extendable to other frames
- **Bidirectional Translation**: Supports translation between English and Japanese
- **Semantic Element Preservation**: Identifies and preserves frame elements during translation
- **Interactive UI**: User-friendly interface with frame selection, language selection, and visualization of frame analysis
- **Flexible Model Support**: Configurable to use either DeepSeek or OpenAI models

## 🏗️ Architecture

The system is built using a combination of LangGraph for agent workflow and Flask for the web interface:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Web Interface  │────▶│   Flask API     │────▶│  LangGraph      │
│  (HTML/JS/CSS)  │     │   Endpoints     │     │  Agent Workflow │
│                 │◀────│                 │◀────│                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                      │                        │
        │                      │                        │
        ▼                      ▼                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                      Semantic Frame Repository                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Agent Workflow

The translation process follows a two-step workflow:

1. **Frame Analysis**: The source text is analyzed to identify frame elements specific to the selected semantic frame
2. **Translation**: The text is translated while preserving the identified frame elements

This approach ensures that the semantic structure of the original text is maintained in the translation, regardless of which semantic frame is being used.

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- DeepSeek API key (or OpenAI API key as fallback)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/zhaosiheng1998/frame-translation-tool.git
   cd frame-translation-tool
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   
   Then edit the `.env` file to add your API keys:
   ```
   DEEPSEEK_API_KEY=your_deepseek_api_key_here
   # Uncomment if you want to use OpenAI
   # OPENAI_API_KEY=your_openai_api_key_here
   # DEFAULT_MODEL=gpt-4o
   ```

### Running the Application

Start the application:
```bash
python run.py
```

Then open your browser and navigate to:
```
http://localhost:5000
```

## 💡 Design Philosophy

This project demonstrates how to leverage frame semantics in natural language processing tasks. The key design principles include:

1. **Separation of Concerns**: The system is divided into backend (agent logic) and frontend (user interface) components.

2. **Modular Architecture**: The agent workflow is built using LangGraph, which allows for easy extension and modification.

3. **Frame-based Understanding**: By using the Commerce_buy frame as a foundation, the system can understand the semantic structure of text and preserve it during translation.

4. **Few-shot Learning**: The system uses examples from the frame definition to guide the language model in identifying frame elements and performing translations.

## 📊 Project Structure

```
├── backend/
│   ├── __init__.py
│   ├── agent.py        # LangGraph agent implementation
│   ├── app.py          # Flask application
│   └── utils.py        # Utility functions
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── script.js
│   └── templates/
│       └── index.html
├── frames/             # Semantic frame definitions
│   ├── commerce-buy-frame.json
│   ├── travel-transportation-frame.json
│   └── frame_format_guide.md
├── .env.example        # Example environment variables
├── requirements.txt    # Project dependencies
├── run.py              # Application entry point
└── README.md           # Project documentation
```

## 🔍 How It Works

1. **Frame Loading**: The system loads the Commerce_buy frame definition from a JSON file.
2. **User Input**: The user selects source and target languages and enters text to translate.
3. **Frame Analysis**: The system analyzes the source text to identify frame elements.
4. **Translation**: The system translates the text while preserving the identified frame elements.
5. **Result Display**: The translation and frame analysis are displayed to the user.

## 🛠️ Customization

### Using Different Frames

The system is designed to be easily extended with new semantic frames. To add a new frame:

1. Create a JSON file in the `frames/` directory following the format described in `frames/frame_format_guide.md`.
2. Name your file using the pattern `frame-name-frame.json` (e.g., `emotion-experience-frame.json`).
3. Restart the application - the new frame will be automatically detected and available in the dropdown menu.

### Frame Definition Format

Each frame is defined in a JSON file with the following key components:

- **Basic Information**: Frame name, ID, and description
- **Frame Elements**: Core and non-core elements with descriptions and semantic types
- **Lexical Units**: Words that evoke the frame
- **Example Sentences**: Annotated examples showing how the frame is used
- **Few-shot Prompts**: Examples for the LLM to learn from
- **Language-specific Variations**: Information about how the frame is expressed in different languages

For detailed guidelines on creating frame definitions, see `frames/frame_format_guide.md`.

### Example Frame Structure

```json
{
  "frame_name": "Frame_name",
  "frame_id": "FRXXXX",
  "description": "Description of the frame",
  "frame_elements": {
    "core_elements": [
      {
        "name": "Element_name",
        "description": "Element description",
        "semantic_type": "Type"
      }
    ],
    "non_core_elements": [...]
  },
  "lexical_units": [...],
  "example_sentences": [...],
  "few_shot_prompts": {...},
  "language_specific_variations": {...}
}
```

### Using Different Models

The system supports both DeepSeek and OpenAI models. To change the model:

1. Edit the `.env` file to set the `DEFAULT_MODEL` variable.
2. For OpenAI models, uncomment the `OPENAI_API_KEY` line and add your API key.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- This project uses semantic frames inspired by FrameNet.
- Built with LangGraph, LangChain, and Flask.
