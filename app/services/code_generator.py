from typing import Dict, Any
from loguru import logger

class CodeGenerator:
    @staticmethod
    def generate_code(function_name: str, context: Dict[str, Any]) -> str:
        """
        Generate executable Python code for a function.
        
        Args:
            function_name: Name of the function to execute
            context: Function metadata and context
            
        Returns:
            The actual result of the function execution
        """
        try:
            # Import necessary modules
            imports = CodeGenerator._generate_imports(function_name)
            
            # Get the function call
            function_call = CodeGenerator._generate_function_call(function_name, context)
            
            # Generate the complete code
            code = f"""
{imports}

{CodeGenerator._generate_docstring(function_name, context)}

def main():
    try:
        # Execute the function
        result = {function_call}
        
        # Handle the result
        if result is not None:
            if isinstance(result, (dict, list)):
                print(json.dumps(result, indent=2))
            else:
                print(f"Result: {result}")
        else:
            print("Function executed successfully.")
            
    except Exception as e:
        print(f"Error executing {function_name}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
"""
            return code
            
        except Exception as e:
            logger.error(f"Error generating code: {e}")
            raise

    @staticmethod
    def _generate_imports(function_name: str) -> str:
        """Generate necessary imports based on function name"""
        imports = [
            "import os",
            "import sys",
            "from typing import Any, Dict",
            "import json"
        ]
        
        # Add specific imports based on function name
        if "time" in function_name or "date" in function_name:
            imports.append("from datetime import datetime")
        if "system" in function_name or "cpu" in function_name or "ram" in function_name:
            imports.append("import psutil")
            imports.append("import platform")
            
        return "\n".join(imports)

    @staticmethod
    def _generate_function_call(function_name: str, context: Dict[str, Any]) -> str:
        """Generate the function call with proper parameters"""
        if "time" in function_name:
            return "datetime.now().strftime('%H:%M:%S')"
        elif "date" in function_name:
            return "datetime.now().strftime('%Y-%m-%d')"
        elif "system" in function_name:
            return """
{
    'system': platform.system(),
    'release': platform.release(),
    'version': platform.version(),
    'machine': platform.machine(),
    'processor': platform.processor()
}"""
        elif "cpu" in function_name:
            return "psutil.cpu_percent(interval=1)"
        elif "ram" in function_name:
            return "psutil.virtual_memory().percent"
        elif "disk" in function_name:
            return "psutil.disk_usage('/').percent"
        elif "network" in function_name:
            return """
{
    'interfaces': [netiface.ifaddrs(iface) for iface in netiface.interfaces()]
}"""
        else:
            return f"{function_name}()"

    @staticmethod
    def _generate_docstring(function_name: str, context: Dict[str, Any]) -> str:
        """Generate a docstring for the function"""
        return f'''"""
Generated code for function: {function_name}
Description: {context.get('description', 'No description available')}
Category: {context.get('category', 'No category available')}
Parameters: {', '.join(context.get('parameters', {}).keys()) if context.get('parameters') else 'None'}
Examples: {', '.join(context.get('examples', [])) if context.get('examples') else 'None'}
"""''' 