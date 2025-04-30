# Atria's AI Agentic System

An intelligent meeting assistant that processes meeting notes and generates insightful questions using multiple specialized AI agents.

## Project Overview

This system uses a multi-agent approach to analyze meeting notes and conduct intelligent conversations about meetings. It employs several specialized nodes (agents) that work together in a pipeline to process information and generate insights.

## Node Architecture

### 1. QA Agent Node
- **Purpose**: Handles initial conversation and meeting notes processing
- **Functionality**:
  - Generates contextual questions based on conversation
  - Processes user responses
  - Maintains conversation flow
  - Extracts key information from meeting notes
- **Input**: User responses or meeting notes
- **Output**: Structured meeting information and follow-up questions

### 2. Intelligent Agent Node
- **Purpose**: Generates insightful questions from meeting content
- **Functionality**:
  - Analyzes meeting notes and extracted information
  - Identifies information gaps
  - Generates 5-8 strategic questions
  - Focuses on strategic goals, challenges, and action items
- **Input**: Processed meeting notes and conversation history
- **Output**: List of generated questions

### 3. Reflection Agent Node
- **Purpose**: Improves question quality through critical analysis
- **Functionality**:
  - Reviews generated questions
  - Provides feedback on clarity and relevance
  - Suggests improvements
  - Refines question formulation
- **Input**: Questions from Intelligent Agent
- **Output**: Refined questions and feedback

### 4. Classification Tool Node
- **Purpose**: Categorizes questions based on available information
- **Functionality**:
  - Analyzes questions against meeting notes
  - Identifies answered vs. unanswered questions
  - Uses keyword matching and LLM for complex cases
- **Input**: Refined questions and meeting context
- **Output**: Categorized lists of answered/unanswered questions

### 5. Question Answer Manager Node
- **Purpose**: Handles collection of answers for remaining questions
- **Functionality**:
  - Manages sequential Q&A process
  - Stores user responses
  - Combines previous and new answers
  - Generates final Q&A summary
- **Input**: Unanswered questions
- **Output**: Complete Q&A pairs

## Features
- Interactive chat interface
- Meeting notes analysis
- Intelligent question generation
- Question refinement and classification
- Comprehensive Q&A management
- Progress tracking
- Final summary generation

## Usage
1. Choose between Q&A mode or Meeting Notes mode
2. Follow the guided process for your chosen mode
3. Provide responses to questions as prompted
4. Review the final analysis and Q&A summary

## Technical Stack
- Streamlit for UI
- LangChain for LLM integration
- GPT-4 for natural language processing
- Python for backend logic

## Project Structure
```
d:\umer\Atria Workflow LG 🤖\
├── st-ui.py          # Streamlit user interface
├── apple.py          # Core agent logic and node implementations
└── README.md         # Project documentation
```

## State Management
The system maintains state across different nodes using an integrated state structure that tracks:
- Conversation history
- Meeting details
- Generated questions
- Question classifications
- User responses
- Processing status

## Future Improvements
- Enhanced question generation
- Better context understanding
- More sophisticated answer matching
- Expanded meeting notes analysis
- Additional customization options
