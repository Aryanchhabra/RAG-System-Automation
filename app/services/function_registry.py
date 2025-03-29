import os
import webbrowser
import psutil
import subprocess
import platform
import json
from datetime import datetime
from typing import Dict, Any, Callable
from app.models.schemas import FunctionMetadata
from loguru import logger

class FunctionRegistry:
    def __init__(self):
        self.functions: Dict[str, Callable] = {}
        self.metadata: Dict[str, FunctionMetadata] = {}
        self._register_functions()

    def execute(self, function_name: str, **kwargs) -> Any:
        """
        Execute a registered function by name.
        
        Args:
            function_name: Name of the function to execute
            **kwargs: Arguments to pass to the function
            
        Returns:
            The result of the function execution
            
        Raises:
            KeyError: If the function is not registered
            Exception: Any exception raised by the function execution
        """
        if function_name not in self.functions:
            raise KeyError(f"Function '{function_name}' not found in registry")
        
        try:
            func = self.functions[function_name]
            result = func(**kwargs)
            
            # Format the result based on its type
            if isinstance(result, (dict, list)):
                return json.dumps(result, indent=2)
            elif isinstance(result, (int, float)):
                return f"{result:.2f}%"
            else:
                return str(result)
                
        except Exception as e:
            logger.error(f"Error executing function {function_name}: {str(e)}")
            raise

    def _register_functions(self):
        # Application Control Functions
        self.register_function(
            name="open_chrome",
            func=self._open_chrome,
            description="Opens Google Chrome browser",
            category="Application Control",
            examples=["Open Chrome", "Launch Google Chrome", "Start Chrome browser"]
        )

        self.register_function(
            name="open_calculator",
            func=self._open_calculator,
            description="Opens the system calculator",
            category="Application Control",
            examples=["Open calculator", "Launch calculator", "Start calculator"]
        )

        self.register_function(
            name="open_notepad",
            func=self._open_notepad,
            description="Opens Notepad text editor",
            category="Application Control",
            examples=["Open notepad", "Launch notepad", "Start notepad"]
        )

        self.register_function(
            name="open_vscode",
            func=self._open_vscode,
            description="Opens Visual Studio Code",
            category="Application Control",
            examples=["Open VS Code", "Launch VS Code", "Start VS Code"]
        )

        # System Monitoring Functions
        self.register_function(
            name="get_system_info",
            func=self._get_system_info,
            description="Gets detailed system information",
            category="System Monitoring",
            examples=["Show system info", "Get system details", "Check system information"]
        )

        self.register_function(
            name="get_cpu_usage",
            func=self._get_cpu_usage,
            description="Gets the current CPU usage percentage",
            category="System Monitoring",
            examples=["Show CPU usage", "Get CPU utilization", "Check CPU load"]
        )

        self.register_function(
            name="get_ram_usage",
            func=self._get_ram_usage,
            description="Gets the current RAM usage percentage",
            category="System Monitoring",
            examples=["Show RAM usage", "Get memory utilization", "Check RAM load"]
        )

        self.register_function(
            name="get_disk_usage",
            func=self._get_disk_usage,
            description="Gets the current disk usage percentage",
            category="System Monitoring",
            examples=["Show disk usage", "Get disk utilization", "Check disk space"]
        )

        self.register_function(
            name="get_network_info",
            func=self._get_network_info,
            description="Gets network interface information",
            category="System Monitoring",
            examples=["Show network info", "Get network details", "Check network status"]
        )

        # File System Functions
        self.register_function(
            name="list_directory",
            func=self._list_directory,
            description="Lists contents of a directory",
            category="File System",
            parameters={"path": "The directory path to list"},
            examples=["List directory", "Show folder contents", "List files"]
        )

        self.register_function(
            name="create_directory",
            func=self._create_directory,
            description="Creates a new directory",
            category="File System",
            parameters={"path": "The path where the directory should be created"},
            examples=["Create directory", "Make new folder", "Create folder"]
        )

        self.register_function(
            name="delete_file",
            func=self._delete_file,
            description="Deletes a file",
            category="File System",
            parameters={"path": "The path of the file to delete"},
            examples=["Delete file", "Remove file", "Erase file"]
        )

        # Command Execution Functions
        self.register_function(
            name="run_command",
            func=self._run_command,
            description="Runs a shell command",
            category="Command Execution",
            parameters={"command": "The shell command to execute"},
            examples=["Run command", "Execute command", "Run shell command"]
        )

        self.register_function(
            name="get_process_list",
            func=self._get_process_list,
            description="Lists all running processes",
            category="Command Execution",
            examples=["Show processes", "List running processes", "Check processes"]
        )

        # Time and Date Functions
        self.register_function(
            name="get_current_time",
            func=self._get_current_time,
            description="Gets the current system time",
            category="Time and Date",
            examples=["Show current time", "Get time", "Check time"]
        )

        self.register_function(
            name="get_current_date",
            func=self._get_current_date,
            description="Gets the current system date",
            category="Time and Date",
            examples=["Show current date", "Get date", "Check date"]
        )

    def register_function(
        self,
        name: str,
        func: Callable,
        description: str,
        category: str,
        parameters: Dict[str, Any] = None,
        examples: list = None
    ):
        self.functions[name] = func
        self.metadata[name] = FunctionMetadata(
            name=name,
            description=description,
            category=category,
            parameters=parameters,
            examples=examples
        )

    # Application Control Functions
    def _open_chrome(self):
        webbrowser.open("https://www.google.com")
        logger.info("Chrome browser opened successfully")

    def _open_calculator(self):
        if os.name == 'nt':  # Windows
            os.system("calc")
        else:  # Linux/Mac
            subprocess.Popen(["gnome-calculator"])
        logger.info("Calculator opened successfully")

    def _open_notepad(self):
        if os.name == 'nt':  # Windows
            os.system("notepad")
        else:  # Linux/Mac
            subprocess.Popen(["gedit"])
        logger.info("Notepad opened successfully")

    def _open_vscode(self):
        if os.name == 'nt':  # Windows
            os.system("code")
        else:  # Linux/Mac
            subprocess.Popen(["code"])
        logger.info("VS Code opened successfully")

    # System Monitoring Functions
    def _get_system_info(self):
        """Get detailed system information"""
        try:
            info = {
                'system': platform.system(),
                'release': platform.release(),
                'version': platform.version(),
                'machine': platform.machine(),
                'processor': platform.processor(),
                'cpu_count': psutil.cpu_count(),
                'memory_total': f"{psutil.virtual_memory().total / (1024**3):.2f} GB",
                'disk_total': f"{psutil.disk_usage('/').total / (1024**3):.2f} GB"
            }
            return json.dumps(info, indent=2)
        except Exception as e:
            logger.error(f"Error getting system info: {e}")
            raise

    def _get_cpu_usage(self):
        """Get current CPU usage percentage"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            info = {
                'cpu_percent': f"{cpu_percent:.2f}%",
                'cpu_count': cpu_count,
                'cpu_freq': f"{cpu_freq.current:.2f} MHz" if cpu_freq else "N/A"
            }
            return json.dumps(info, indent=2)
        except Exception as e:
            logger.error(f"Error getting CPU usage: {e}")
            raise

    def _get_ram_usage(self):
        """Get current RAM usage percentage"""
        try:
            memory = psutil.virtual_memory()
            info = {
                'total': f"{memory.total / (1024**3):.2f} GB",
                'available': f"{memory.available / (1024**3):.2f} GB",
                'used': f"{memory.used / (1024**3):.2f} GB",
                'percent': f"{memory.percent:.2f}%"
            }
            return json.dumps(info, indent=2)
        except Exception as e:
            logger.error(f"Error getting RAM usage: {e}")
            raise

    def _get_disk_usage(self):
        """Get current disk usage percentage"""
        try:
            disk = psutil.disk_usage('/')
            info = {
                'total': f"{disk.total / (1024**3):.2f} GB",
                'used': f"{disk.used / (1024**3):.2f} GB",
                'free': f"{disk.free / (1024**3):.2f} GB",
                'percent': f"{disk.percent:.2f}%"
            }
            return json.dumps(info, indent=2)
        except Exception as e:
            logger.error(f"Error getting disk usage: {e}")
            raise

    def _get_network_info(self):
        """Get network interface information"""
        try:
            interfaces = {}
            for iface, addrs in psutil.net_if_addrs().items():
                interfaces[iface] = []
                for addr in addrs:
                    interfaces[iface].append({
                        'address': addr.address,
                        'netmask': addr.netmask,
                        'family': str(addr.family)
                    })
            return json.dumps(interfaces, indent=2)
        except Exception as e:
            logger.error(f"Error getting network info: {e}")
            raise

    # File System Functions
    def _list_directory(self, path: str = "."):
        try:
            return os.listdir(path)
        except Exception as e:
            logger.error(f"Error listing directory: {e}")
            raise

    def _create_directory(self, path: str = None):
        """
        Creates a new directory.
        If path is not provided, creates a default 'test_folder' directory.
        """
        try:
            if path is None:
                path = "test_folder"
            os.makedirs(path, exist_ok=True)
            logger.info(f"Directory created successfully: {path}")
            return f"Directory '{path}' created successfully"
        except Exception as e:
            logger.error(f"Error creating directory: {e}")
            raise

    def _delete_file(self, path: str):
        try:
            os.remove(path)
            logger.info(f"File deleted successfully: {path}")
            return True
        except Exception as e:
            logger.error(f"Error deleting file: {e}")
            raise

    # Command Execution Functions
    def _run_command(self, command: str):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            logger.error(f"Error running command: {e}")
            raise

    def _get_process_list(self):
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return json.dumps(processes, indent=2)

    # Time and Date Functions
    def _get_current_time(self):
        """Get current system time"""
        try:
            now = datetime.now()
            info = {
                'time': now.strftime('%H:%M:%S'),
                'timezone': now.astimezone().tzinfo.tzname(None)
            }
            return json.dumps(info, indent=2)
        except Exception as e:
            logger.error(f"Error getting current time: {e}")
            raise

    def _get_current_date(self):
        """Get current system date"""
        try:
            now = datetime.now()
            info = {
                'date': now.strftime('%Y-%m-%d'),
                'day_of_week': now.strftime('%A'),
                'timezone': now.astimezone().tzinfo.tzname(None)
            }
            return json.dumps(info, indent=2)
        except Exception as e:
            logger.error(f"Error getting current date: {e}")
            raise

    def get_function(self, name: str) -> Callable:
        return self.functions.get(name)

    def get_metadata(self, name: str) -> FunctionMetadata:
        return self.metadata.get(name)

    def get_all_metadata(self) -> Dict[str, FunctionMetadata]:
        return self.metadata

    def register_custom_function(
        self,
        name: str,
        func: Callable,
        description: str,
        category: str = "Custom",
        parameters: Dict[str, Any] = None,
        examples: list = None
    ):
        """
        Register a custom user-defined function.
        
        Args:
            name: Name of the function
            func: The function to register
            description: Description of what the function does
            category: Category of the function (default: "Custom")
            parameters: Dictionary of parameter names and descriptions
            examples: List of example prompts
        """
        try:
            # Validate function name
            if name in self.functions:
                raise ValueError(f"Function '{name}' already exists")
            
            # Register the function
            self.register_function(
                name=name,
                func=func,
                description=description,
                category=category,
                parameters=parameters,
                examples=examples
            )
            
            # Update vector store with new function
            self._update_vector_store()
            
            logger.info(f"Successfully registered custom function: {name}")
            return True
            
        except Exception as e:
            logger.error(f"Error registering custom function: {e}")
            raise

    def _update_vector_store(self):
        """Update the vector store with all registered functions"""
        try:
            # Get all function metadata
            metadata = self.get_all_metadata()
            
            # Prepare documents for embedding
            documents = []
            metadatas = []
            ids = []
            
            for func_name, func_metadata in metadata.items():
                # Create a rich text description combining all metadata
                doc = f"""
                Function: {func_metadata.name}
                Description: {func_metadata.description}
                Category: {func_metadata.category}
                Examples: {', '.join(func_metadata.examples or [])}
                Parameters: {', '.join(func_metadata.parameters.keys()) if func_metadata.parameters else 'None'}
                """
                
                documents.append(doc)
                
                # Format metadata as strings to comply with ChromaDB requirements
                metadatas.append({
                    "name": str(func_metadata.name),
                    "category": str(func_metadata.category),
                    "description": str(func_metadata.description),
                    "parameters": str(func_metadata.parameters.keys()) if func_metadata.parameters else "None",
                    "examples": str(func_metadata.examples) if func_metadata.examples else "None"
                })
                ids.append(func_name)

            # Update the collection
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info("Successfully updated vector store")
            
        except Exception as e:
            logger.error(f"Error updating vector store: {e}")
            raise

# Create a singleton instance
function_registry = FunctionRegistry() 