from fastapi import APIRouter, HTTPException
from app.models.schemas import ExecuteRequest, ExecuteResponse
from app.services.function_registry import function_registry
from app.services.rag_service import RAGService
from loguru import logger
from pydantic import BaseModel
from typing import Dict, Any, Callable
import inspect
import importlib.util
import tempfile
import os
import json

router = APIRouter()
rag_service = RAGService()

@router.post(
    "/execute",
    response_model=ExecuteResponse,
    summary="Execute Function",
    description="""
    Executes a function based on the natural language prompt provided.
    
    The API will:
    1. Parse the natural language prompt
    2. Match it to the most appropriate function using context from previous interactions
    3. Execute the function and return results
    
    Available function categories:
    - Application Control (open calculator, chrome, notepad, etc.)
    - System Monitoring (CPU usage, RAM usage, system info)
    - File System Operations (list directory, create directory)
    - Command Execution
    - Time and Date Operations
    """,
    response_description="Returns the executed function details and status",
)
async def execute_function(request: ExecuteRequest):
    """
    Execute a function based on the provided prompt.
    
    Example prompts:
    - "Open calculator"
    - "Show CPU usage"
    - "What's the current time?"
    - "List files in current directory"
    - "Open Chrome browser"
    """
    try:
        # Find the most relevant function using RAG with context
        function_match = rag_service.get_best_match(request.prompt)
        if not function_match:
            raise HTTPException(status_code=404, detail="No matching function found for the given prompt")

        # Execute the function
        try:
            function_name = function_match["name"]
            result = function_registry.execute(function_name)
            
            # Add to session history
            rag_service.add_to_history(request.prompt, function_name, result)
            
            # Parse the result
            try:
                result_json = json.loads(result)
                if "error" in result_json:
                    return ExecuteResponse(
                        function=function_name,
                        code=result,
                        status="error",
                        error=result_json["error"]
                    )
                elif "value" in result_json:
                    return ExecuteResponse(
                        function=function_name,
                        code=result,
                        status="success",
                        error=None
                    )
                else:
                    return ExecuteResponse(
                        function=function_name,
                        code=result,
                        status="success",
                        error=None
                    )
            except json.JSONDecodeError:
                # If result is not JSON, wrap it in a value field
                return ExecuteResponse(
                    function=function_name,
                    code=json.dumps({"value": result}, indent=2),
                    status="success",
                    error=None
                )
            
        except Exception as e:
            logger.error(f"Error executing function {function_name}: {str(e)}")
            return ExecuteResponse(
                function=function_name,
                code=json.dumps({"error": str(e)}, indent=2),
                status="error",
                error=str(e)
            )

    except Exception as e:
        logger.error(f"Error in execute_function: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

class CustomFunction(BaseModel):
    name: str
    code: str
    description: str
    category: str = "Custom"
    parameters: Dict[str, Any] = None
    examples: list = None

@router.post("/register-function")
async def register_function(function: CustomFunction):
    """
    Register a custom user-defined function.
    
    Args:
        function: CustomFunction object containing:
            - name: Name of the function
            - code: Python code for the function
            - description: Description of what the function does
            - category: Category of the function (default: "Custom")
            - parameters: Dictionary of parameter names and descriptions
            - examples: List of example prompts
    """
    try:
        # Create a temporary file to store the function code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(function.code)
            temp_path = f.name

        # Import the function from the temporary file
        spec = importlib.util.spec_from_file_location("custom_function", temp_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Get the function object
        func = getattr(module, function.name)
        
        # Validate the function
        if not callable(func):
            raise ValueError(f"'{function.name}' is not a callable function")
        
        # Register the function
        function_registry.register_custom_function(
            name=function.name,
            func=func,
            description=function.description,
            category=function.category,
            parameters=function.parameters,
            examples=function.examples
        )

        # Clean up the temporary file
        os.unlink(temp_path)

        return {"message": f"Successfully registered function: {function.name}"}

    except Exception as e:
        logger.error(f"Error registering custom function: {e}")
        raise HTTPException(status_code=400, detail=str(e)) 