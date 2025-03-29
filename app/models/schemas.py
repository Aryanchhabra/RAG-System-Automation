from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class ExecuteRequest(BaseModel):
    prompt: str = Field(
        ...,
        description="Natural language prompt describing the function to execute",
        examples=[
            "Open calculator",
            "Show CPU usage",
            "What's the current time?",
            "List files in current directory",
            "Open Chrome browser"
        ]
    )
    context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional context data for function execution"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "Open calculator",
                "context": None
            }
        }

class ExecuteResponse(BaseModel):
    function: str = Field(
        ...,
        description="Name of the executed function"
    )
    code: str = Field(
        ...,
        description="Generated Python code for the function execution"
    )
    status: str = Field(
        ...,
        description="Execution status (success/error)"
    )
    error: Optional[str] = Field(
        None,
        description="Error message if execution failed"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "function": "open_calculator",
                "code": '''import os\nimport sys\nfrom typing import Any, Dict\n\n"""\nGenerated code for function: open_calculator\nDescription: Opens the system calculator\nCategory: Application Control\nParameters: None\nExamples: Open calculator, Launch calculator, Start calculator\n"""\n\ndef main():\n    try:\n        result = open_calculator()\n        if result is not None:\n            print(json.dumps(result, indent=2))\n        else:\n            print("Function open_calculator executed successfully.")\n    except Exception as e:\n        print(f"Error executing open_calculator: {e}")\n        sys.exit(1)\n\nif __name__ == "__main__":\n    main()''',
                "status": "success",
                "error": None
            }
        }

class FunctionMetadata(BaseModel):
    name: str = Field(..., description="Name of the function")
    description: str = Field(..., description="Description of what the function does")
    category: str = Field(..., description="Category of the function (e.g., 'Application Control', 'System Monitoring')")
    parameters: Optional[Dict[str, Any]] = Field(default=None, description="Function parameters if any")
    examples: Optional[List[str]] = Field(default=None, description="Example prompts that would trigger this function") 