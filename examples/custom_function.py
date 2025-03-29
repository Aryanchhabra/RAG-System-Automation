import requests
import json

def register_custom_function():
    """Example of registering a custom function"""
    
    # Example custom function that calculates Fibonacci numbers
    function_code = """
def fibonacci(n: int) -> int:
    \"\"\"Calculate the nth Fibonacci number\"\"\"
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
"""
    
    # Prepare the function registration request
    function_data = {
        "name": "fibonacci",
        "code": function_code,
        "description": "Calculate the nth Fibonacci number",
        "category": "Mathematics",
        "parameters": {
            "n": "The position in the Fibonacci sequence (0-based)"
        },
        "examples": [
            "Calculate the 10th Fibonacci number",
            "What is the 5th Fibonacci number?",
            "Find fibonacci(7)"
        ]
    }
    
    # Register the function
    response = requests.post(
        "http://localhost:8000/api/v1/register-function",
        json=function_data
    )
    
    if response.status_code == 200:
        print("Successfully registered custom function!")
        return True
    else:
        print(f"Error registering function: {response.text}")
        return False

def test_custom_function():
    """Test the registered custom function"""
    
    # Test prompts
    prompts = [
        "Calculate the 10th Fibonacci number",
        "What is the 5th Fibonacci number?",
        "Find fibonacci(7)"
    ]
    
    for prompt in prompts:
        response = requests.post(
            "http://localhost:8000/api/v1/execute",
            json={"prompt": prompt}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"\nPrompt: {prompt}")
            print(f"Result: {json.dumps(result, indent=2)}")
        else:
            print(f"\nError executing function: {response.text}")

def main():
    """Main function to demonstrate custom function usage"""
    print("Registering custom function...")
    if register_custom_function():
        print("\nTesting custom function...")
        test_custom_function()
    else:
        print("Failed to register custom function. Please check the API server is running.")

if __name__ == "__main__":
    main() 