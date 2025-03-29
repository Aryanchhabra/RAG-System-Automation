# AlgoRoot LLM + RAG Function Execution API

A sophisticated Python-based API service that leverages Large Language Models (LLM) and Retrieval-Augmented Generation (RAG) to dynamically execute system automation functions based on natural language prompts. This project demonstrates the power of combining LLM capabilities with RAG for intelligent function retrieval and execution.

## Overview

AlgoRoot is designed to bridge the gap between natural language commands and system automation. It allows users to execute various system functions using simple English prompts, making system automation more accessible and intuitive.

### Key Features

- **Natural Language Processing**: Understands and processes user commands in plain English
- **Intelligent Function Matching**: Uses RAG to match user prompts with appropriate system functions
- **Dynamic Code Generation**: Automatically generates and executes Python code for matched functions
- **Comprehensive Function Registry**: Supports various system operations including:
  - Application Control (Chrome, Calculator, Notepad, VS Code)
  - System Monitoring (CPU, RAM, Disk, Network)
  - File System Operations (List, Create, Delete)
  - Command Execution
  - Time and Date Operations
- **RESTful API**: Clean, well-documented API endpoints for easy integration
- **Error Handling**: Robust error handling and logging throughout the system
- **Session Management**: Maintains context across function executions

## Architecture

### Core Components

1. **Function Registry**
   - Central repository of available system functions
   - Each function includes metadata (description, category, parameters)
   - Handles function execution and result management

2. **RAG Service**
   - Implements Retrieval-Augmented Generation for function matching
   - Uses ChromaDB for vector storage and similarity search
   - Leverages Sentence Transformers for semantic understanding

3. **Code Generator**
   - Generates executable Python code for matched functions
   - Includes proper error handling and result formatting
   - Maintains code quality and documentation

4. **API Layer**
   - FastAPI-based RESTful endpoints
   - OpenAPI/Swagger documentation
   - Request/Response validation using Pydantic

### Data Flow

1. User sends a natural language prompt to the API
2. RAG service matches the prompt to the most appropriate function
3. Code generator creates executable code for the function
4. Function registry executes the code and returns results
5. API returns the execution status and results to the user

## API Documentation

### Endpoints

#### POST /api/v1/execute

Executes a function based on the provided natural language prompt.

**Request Body:**
```json
{
    "prompt": "Open calculator",
    "context": {}  // Optional context data
}
```

**Response:**
```json
{
    "function": "open_calculator",
    "code": "Generated Python code...",
    "status": "success",
    "error": null
}
```

### Example Usage

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/execute",
    json={
        "prompt": "Show CPU usage"
    }
)
print(response.json())
```

## Technical Stack

- **Python 3.9+**: Core programming language
- **FastAPI**: Modern web framework for building APIs
- **ChromaDB**: Vector database for semantic search
- **Sentence Transformers**: For text embeddings and similarity search
- **Pydantic**: Data validation and settings management
- **Loguru**: Advanced logging capabilities

## Project Structure

```
.
├── app/
│   ├── api/            # API endpoints and routes
│   ├── core/           # Core configuration and logging
│   ├── models/         # Data models and schemas
│   ├── services/       # Core business logic
│   └── utils/          # Utility functions
├── examples/           # Example usage scripts
├── tests/             # Test cases
└── requirements.txt   # Project dependencies
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 