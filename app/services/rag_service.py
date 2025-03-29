import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import os
from app.core.config import settings
from app.services.function_registry import function_registry
from loguru import logger
from datetime import datetime

class RAGService:
    def __init__(self):
        self.client = chromadb.Client(Settings(
            persist_directory=settings.CHROMA_DB_PATH,
            anonymized_telemetry=False
        ))
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL)
        self.collection = self.client.get_or_create_collection("function_metadata")
        self.session_history = []  # Store chat history
        self._initialize_vector_store()

    def _initialize_vector_store(self):
        """Initialize the vector store with function metadata"""
        try:
            # First, delete the existing collection if it exists
            try:
                self.client.delete_collection("function_metadata")
                logger.info("Deleted existing collection")
            except:
                pass
            
            # Create a new collection
            self.collection = self.client.create_collection("function_metadata")
            
            # Get all function metadata
            metadata = function_registry.get_all_metadata()
            
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

            # Add documents to the collection
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Successfully initialized vector store with {len(documents)} functions")
            
        except Exception as e:
            logger.error(f"Error initializing vector store: {e}")
            raise

    def add_to_history(self, prompt: str, function_name: str, result: str):
        """Add interaction to session history"""
        self.session_history.append({
            "prompt": prompt,
            "function": function_name,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })
        # Keep only last 10 interactions
        if len(self.session_history) > 10:
            self.session_history.pop(0)

    def get_relevant_history(self, current_prompt: str) -> str:
        """Get relevant context from session history"""
        if not self.session_history:
            return ""

        # Convert history to text for context
        history_text = "\n".join([
            f"Previous interaction: {item['prompt']} -> {item['function']}"
            for item in self.session_history[-3:]  # Use last 3 interactions
        ])
        return f"Previous interactions:\n{history_text}\n\nCurrent prompt: {current_prompt}"

    def retrieve_functions(self, query: str, n_results: int = None) -> List[Dict[str, Any]]:
        """
        Retrieve the most relevant functions for a given query
        """
        try:
            if n_results is None:
                n_results = settings.MAX_RETRIEVAL_RESULTS

            # Get relevant context from history
            context = self.get_relevant_history(query)

            # Query the vector store with context
            results = self.collection.query(
                query_texts=[context],
                n_results=n_results
            )

            # Process results
            retrieved_functions = []
            query_lower = query.lower()
            
            for i in range(len(results['ids'][0])):
                func_name = results['ids'][0][i]
                metadata = results['metadatas'][0][i]
                distance = results['distances'][0][i]
                
                # Get function metadata for additional context
                func_metadata = function_registry.get_metadata(func_name)
                
                # Calculate base relevance score
                relevance_score = 1 - distance
                
                # Check for exact matches in examples
                if any(example.lower() == query_lower for example in func_metadata.examples):
                    relevance_score = 1.0
                
                # Check for partial matches in examples
                elif any(example.lower() in query_lower for example in func_metadata.examples):
                    relevance_score += 0.3
                
                # Check for function name matches
                elif func_name.replace('_', ' ').lower() in query_lower:
                    relevance_score += 0.2
                
                # Check for description matches
                elif func_metadata.description.lower() in query_lower:
                    relevance_score += 0.1
                
                # Category-specific boosts
                if func_metadata.category == "System Monitoring" and any(word in query_lower for word in ["show", "get", "check", "display", "monitor", "system"]):
                    relevance_score += 0.5
                
                elif func_metadata.category == "Application Control" and any(word in query_lower for word in ["open", "launch", "start", "run", "execute"]):
                    relevance_score += 0.5
                
                retrieved_functions.append({
                    "name": func_name,
                    "metadata": metadata,
                    "relevance_score": relevance_score,
                    "category": func_metadata.category,
                    "description": func_metadata.description,
                    "parameters": func_metadata.parameters,
                    "examples": func_metadata.examples
                })

            # Sort by relevance score
            retrieved_functions.sort(key=lambda x: x["relevance_score"], reverse=True)
            
            logger.info(f"Retrieved {len(retrieved_functions)} functions for query: {query}")
            return retrieved_functions

        except Exception as e:
            logger.error(f"Error retrieving functions: {e}")
            raise

    def get_best_match(self, query: str) -> Dict[str, Any]:
        """
        Get the best matching function for a given query
        """
        results = self.retrieve_functions(query, n_results=5)  # Get top 5 matches
        
        if not results:
            return None
            
        query_lower = query.lower()
        
        # First, try exact matches in examples
        for result in results:
            if any(example.lower() == query_lower for example in result["examples"]):
                return result
        
        # Then, try partial matches in examples
        for result in results:
            if any(example.lower() in query_lower for example in result["examples"]):
                return result
        
        # For system monitoring queries, prefer system info function
        if any(word in query_lower for word in ["show", "get", "check", "display", "monitor", "system"]):
            for result in results:
                if result["name"] == "get_system_info":
                    return result
        
        # For application control queries, prefer specific apps
        if any(word in query_lower for word in ["open", "launch", "start", "run", "execute"]):
            for result in results:
                if result["category"] == "Application Control":
                    return result
        
        # If still no match, return the highest scoring result
        return results[0]

    def extract_parameters(self, query: str, function_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract parameters from the query based on function metadata
        """
        params = {}
        if function_metadata.get("parameters"):
            # Simple parameter extraction based on keywords
            for param_name in function_metadata["parameters"]:
                if param_name in query.lower():
                    # Extract the value after the parameter name
                    try:
                        value = query.split(param_name)[1].split()[0]
                        params[param_name] = value
                    except:
                        pass
        return params 