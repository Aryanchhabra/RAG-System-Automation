import requests
import json
import time
from datetime import datetime
import os
import sys

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print a beautiful header"""
    print("\n" + "="*50)
    print("           AlgoRoot Function Execution API")
    print("="*50 + "\n")

def print_menu():
    """Print the main menu"""
    print("\nAvailable Functions:")
    print("1. Application Control")
    print("   - Open Calculator")
    print("   - Open Chrome Browser")
    print("   - Open Notepad")
    print("   - Open VS Code")
    print("\n2. System Monitoring")
    print("   - Show System Information")
    print("   - Show CPU Usage")
    print("   - Show RAM Usage")
    print("   - Show Disk Usage")
    print("\n3. File System Operations")
    print("   - Create Directory")
    print("   - List Directory Contents")
    print("   - Delete File")
    print("\n4. Time and Date")
    print("   - Show Current Time")
    print("   - Show Current Date")
    print("\n5. Run All Examples")
    print("\n0. Exit")
    print("\n" + "="*50)

def execute_function(prompt, context=None):
    """Execute a function through the API"""
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/execute",
            json={"prompt": prompt, "context": context or {}}
        )
        return response.json()
    except Exception as e:
        print(f"Error executing function: {e}")
        return None

def print_result(result, title):
    """Print the result in a formatted way"""
    print("\n" + "="*50)
    print(f"           {title}")
    print("="*50)
    if result and result.get("status") == "success":
        print("\nFunction:", result.get("function"))
        print("\nResult:")
        print("-"*30)
        try:
            # Try to parse and pretty print JSON
            data = json.loads(result.get("code"))
            print(json.dumps(data, indent=2))
        except:
            # If not JSON, print as is
            print(result.get("code"))
        print("-"*30)
    else:
        print("\nError:", result.get("error", "Unknown error occurred"))
    print("\n" + "="*50)

def run_all_examples():
    """Run all example functions"""
    examples = [
        ("Opening Calculator", "Open calculator"),
        ("Getting System Information", "Show system information"),
        ("Creating a Directory", "Create directory named test_folder"),
        ("Listing Directory Contents", "List contents of current directory"),
        ("Getting Current Time", "What's the current time?"),
        ("Getting CPU Usage", "Show CPU usage"),
        ("Opening Chrome", "Open Chrome browser")
    ]
    
    for title, prompt in examples:
        clear_screen()
        print_header()
        print(f"\nExecuting: {title}")
        result = execute_function(prompt)
        print_result(result, title)
        time.sleep(2)

def main():
    while True:
        clear_screen()
        print_header()
        print_menu()
        
        choice = input("\nEnter your choice (0-5): ")
        
        if choice == "0":
            print("\nThank you for using AlgoRoot!")
            break
            
        elif choice == "5":
            run_all_examples()
            input("\nPress Enter to continue...")
            continue
            
        elif choice == "1":
            submenu = {
                "1": ("Open Calculator", "Open calculator"),
                "2": ("Open Chrome Browser", "Open Chrome browser"),
                "3": ("Open Notepad", "Open notepad"),
                "4": ("Open VS Code", "Open VS Code")
            }
        elif choice == "2":
            submenu = {
                "1": ("Show System Information", "Show system information"),
                "2": ("Show CPU Usage", "Show CPU usage"),
                "3": ("Show RAM Usage", "Show RAM usage"),
                "4": ("Show Disk Usage", "Show disk usage")
            }
        elif choice == "3":
            submenu = {
                "1": ("Create Directory", "Create directory named test_folder"),
                "2": ("List Directory Contents", "List contents of current directory"),
                "3": ("Delete File", "Delete file test.txt")
            }
        elif choice == "4":
            submenu = {
                "1": ("Show Current Time", "What's the current time?"),
                "2": ("Show Current Date", "What's the current date?")
            }
        else:
            print("\nInvalid choice. Please try again.")
            time.sleep(1)
            continue
            
        while True:
            clear_screen()
            print_header()
            print("\nAvailable Options:")
            for key, (title, _) in submenu.items():
                print(f"{key}. {title}")
            print("\n0. Back to Main Menu")
            
            subchoice = input("\nEnter your choice: ")
            
            if subchoice == "0":
                break
                
            if subchoice in submenu:
                title, prompt = submenu[subchoice]
                clear_screen()
                print_header()
                print(f"\nExecuting: {title}")
                result = execute_function(prompt)
                print_result(result, title)
                input("\nPress Enter to continue...")
                break
            else:
                print("\nInvalid choice. Please try again.")
                time.sleep(1)

if __name__ == "__main__":
    main() 