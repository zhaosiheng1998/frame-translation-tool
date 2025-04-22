# Semantic Frame Format Guide

This document provides guidelines for creating semantic frame definitions in JSON format for use with the Frame-based Translation Tool.

## Overview

Semantic frames represent structured knowledge about situations, events, or concepts. Each frame defines a set of frame elements (participants, props, and other conceptual roles) that are involved in the scenario described by the frame.

## JSON Structure

Frame definitions should be saved as JSON files with the following structure:

```json
{
  "frame_name": "Frame_name",
  "frame_id": "FRXXXX",
  "description": "A clear description of the frame concept.",
  "frame_elements": {
    "core_elements": [
      {
        "name": "Element_name",
        "description": "Element description",
        "semantic_type": "Type"
      }
    ],
    "non_core_elements": [
      {
        "name": "Element_name",
        "description": "Element description",
        "semantic_type": "Type"
      }
    ]
  },
  "lexical_units": [
    {
      "lemma": "word",
      "pos": "POS",
      "definition": "Definition"
    }
  ],
  "frame_relations": [
    {
      "relation_type": "Type",
      "related_frame": "Related_frame"
    }
  ],
  "example_sentences": [
    {
      "text": "Example sentence with [Element] annotations.",
      "annotation": {
        "Element": "text span",
        "lexical_unit": "word"
      }
    }
  ],
  "few_shot_prompts": {
    "identification_prompt": "Prompt for element identification",
    "expected_response": {
      "Element": "expected annotation"
    },
    "generation_prompt": "Prompt for sentence generation",
    "expected_generation": "Expected generated sentence",
    "translation_prompt": "Prompt for translation",
    "expected_translation": {
      "Language1": "Translation in language 1",
      "Language2": "Translation in language 2"
    },
    "frame_inference_prompt": "Prompt for inference",
    "expected_inference": {
      "inferred_elements": {
        "Element": "inferred value"
      },
      "reasoning": "Explanation of inference"
    }
  },
  "language_specific_variations": {
    "Language1": {
      "lexical_units": ["word1", "word2"],
      "grammatical_notes": "Notes on grammar",
      "cultural_notes": "Notes on cultural aspects"
    }
  }
}
```

## Field Descriptions

### Required Fields

- **frame_name**: The name of the frame, using CamelCase with underscores (e.g., "Commerce_buy").
- **frame_id**: A unique identifier for the frame, typically "FR" followed by a four-digit number.
- **description**: A clear, concise description of the concept represented by the frame.
- **frame_elements**: Contains two sub-objects:
  - **core_elements**: Array of essential elements that must be present for the frame to be evoked.
  - **non_core_elements**: Array of optional elements that provide additional information.

### Frame Element Structure

Each frame element (both core and non-core) should include:

- **name**: The name of the element, typically a noun.
- **description**: A clear description of the role this element plays in the frame.
- **semantic_type**: The semantic category of the element (e.g., "Sentient", "Entity", "Location", "Time", "State", "Asset", "Quantity").

### Optional Fields

- **lexical_units**: Words or phrases that evoke the frame, each with:
  - **lemma**: The base form of the word.
  - **pos**: Part of speech (e.g., "V" for verb, "N" for noun).
  - **definition**: A definition of the word in the context of the frame.

- **frame_relations**: Relationships to other frames, each with:
  - **relation_type**: Type of relationship (e.g., "Inherits from", "Perspective on", "Precedes").
  - **related_frame**: The name of the related frame.

- **example_sentences**: Examples showing how the frame is used in sentences, each with:
  - **text**: The example sentence, with frame elements marked in brackets.
  - **annotation**: Object mapping element names to text spans.

- **few_shot_prompts**: Prompts and expected responses for various tasks:
  - **identification_prompt**: Prompt for identifying frame elements.
  - **expected_response**: Expected annotation for the identification prompt.
  - **generation_prompt**: Prompt for generating sentences using the frame.
  - **expected_generation**: Example of a generated sentence.
  - **translation_prompt**: Prompt for translation preserving frame elements.
  - **expected_translation**: Examples of translations in different languages.
  - **frame_inference_prompt**: Prompt for inferring implicit frame elements.
  - **expected_inference**: Expected inference results and reasoning.

- **language_specific_variations**: Information about how the frame is expressed in different languages, each with:
  - **lexical_units**: Words or phrases that evoke the frame in that language.
  - **grammatical_notes**: Notes on grammar specific to that language.
  - **cultural_notes**: Notes on cultural aspects relevant to the frame.

## Best Practices

1. **Be Comprehensive**: Include all relevant frame elements, even if they might seem obvious.
2. **Be Clear**: Write clear, concise descriptions that avoid ambiguity.
3. **Be Consistent**: Use consistent terminology and formatting across all frame definitions.
4. **Provide Examples**: Include diverse examples that show different ways the frame can be used.
5. **Consider Languages**: Include language-specific information for all target languages.
6. **Include Few-Shot Prompts**: These are crucial for guiding the language model in understanding and using the frame.

## Example

See `commerce-buy-frame.json` for a complete example of a well-structured frame definition.

## File Naming

Name your frame definition files using the pattern `frame-name-frame.json`, where "frame-name" is the lowercase, hyphenated version of the frame name (e.g., "commerce-buy-frame.json" for the "Commerce_buy" frame).
