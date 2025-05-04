from mcp.server.fastmcp import FastMCP, Context
from typing import List, Optional, Dict, Any
from datetime import datetime
import yaml
import json
import os
import sys
import signal
from pydantic import BaseModel  # Add this import

# Define input model here
class SearchInput(BaseModel):
    query: str

BASE_MEMORY_DIR = "memory"

# Get absolute path to config file
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)  # Go up one level from modules to S9
CONFIG_PATH = os.path.join(ROOT_DIR, "config", "profiles.yaml")

# Load config
try:
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)
        MEMORY_CONFIG = config.get("memory", {}).get("storage", {})
        BASE_MEMORY_DIR = MEMORY_CONFIG.get("base_dir", "memory")
except Exception as e:
    print(f"Error loading config from {CONFIG_PATH}: {e}")
    sys.exit(1)

mcp = FastMCP("memory-service")

class MemoryStore:
    def __init__(self):
        self.memory_dir = BASE_MEMORY_DIR
        self.current_session = None  # Track current session
        os.makedirs(self.memory_dir, exist_ok=True)

    def load_session(self, session_id: str):
        """Load memory manager for a specific session."""
        self.current_session = session_id

    def _list_all_memories(self) -> List[Dict]:
        """Load all memory files using MemoryManager's date-based structure"""
        all_memories = []
        base_path = self.memory_dir  # Use the simple memory_dir path
        
        try:
            for year_dir in os.listdir(base_path):
                year_path = os.path.join(base_path, year_dir)
                if not os.path.isdir(year_path):
                    continue
                    
                for month_dir in os.listdir(year_path):
                    month_path = os.path.join(year_path, month_dir)
                    if not os.path.isdir(month_path):
                        continue
                        
                    for day_dir in os.listdir(month_path):
                        day_path = os.path.join(month_path, day_dir)
                        if not os.path.isdir(day_path):
                            continue
                        
                        # Check for session directory
                        session_dir = os.path.join(day_path, "session")
                        if os.path.isdir(session_dir):
                            # Process session directories
                            for session_id in os.listdir(session_dir):
                                session_path = os.path.join(session_dir, session_id)
                                if os.path.isdir(session_path):
                                    # Process all files in the session directory
                                    for subdir_or_file in os.listdir(session_path):
                                        subdir_or_file_path = os.path.join(session_path, subdir_or_file)
                                        if os.path.isfile(subdir_or_file_path) and subdir_or_file_path.endswith('.json'):
                                            try:
                                                with open(subdir_or_file_path, 'r') as f:
                                                    session_memories = json.load(f)
                                                    if isinstance(session_memories, list):
                                                        all_memories.extend(session_memories)
                                                    elif isinstance(session_memories, dict):
                                                        all_memories.append(session_memories)
                                            except Exception as e:
                                                print(f"Failed to load {subdir_or_file_path}: {e}")
                                        elif os.path.isdir(subdir_or_file_path):
                                            # Process any sub-directories if they exist
                                            for file in os.listdir(subdir_or_file_path):
                                                file_path = os.path.join(subdir_or_file_path, file)
                                                if os.path.isfile(file_path) and file_path.endswith('.json'):
                                                    try:
                                                        with open(file_path, 'r') as f:
                                                            session_memories = json.load(f)
                                                            if isinstance(session_memories, list):
                                                                all_memories.extend(session_memories)
                                                            elif isinstance(session_memories, dict):
                                                                all_memories.append(session_memories)
                                                    except Exception as e:
                                                        print(f"Failed to load {file_path}: {e}")
                        else:
                            # Process direct JSON files if they exist at the day level
                            for file in os.listdir(day_path):
                                if file.endswith('.json'):
                                    try:
                                        with open(os.path.join(day_path, file), 'r') as f:
                                            session_memories = json.load(f)
                                            if isinstance(session_memories, list):
                                                all_memories.extend(session_memories)
                                            elif isinstance(session_memories, dict):
                                                all_memories.append(session_memories)
                                    except Exception as e:
                                        print(f"Failed to load {file}: {e}")
        except Exception as e:
            print(f"Error traversing memory directory: {e}")
        
        print(f"Found {len(all_memories)} memory entries in total")
        return all_memories

    def _get_conversation_flow(self, conversation_id: str = None) -> Dict:
        """Get sequence of interactions in a conversation"""
        if conversation_id is None:
            conversation_id = self.current_session
        
        # Use the session path we already know
        session_path = os.path.join(self.memory_dir, conversation_id)
        if not os.path.exists(session_path):
            return {"error": "Conversation not found"}
        
        interactions = []
        for file in sorted(os.listdir(session_path)):
            if file.endswith('.json'):
                with open(os.path.join(session_path, file), 'r') as f:
                    interactions.append(json.load(f))
        
        return {
            "conversation_flow": [
                {
                    "query": interaction.get("query", ""),
                    "intent": interaction.get("intent", ""),
                    "tool_calls": [
                        {
                            "tool": call["tool"],
                            "args": call["args"],
                            "result_summary": call.get("result_summary", "No summary available")
                        }
                        for call in interaction.get("tool_calls", [])
                    ],
                    "final_answer": interaction.get("final_answer", ""),
                    "tags": interaction.get("tags", [])
                }
                for interaction in interactions
            ],
            "timestamp_start": interactions[0].get("timestamp") if interactions else None,
            "timestamp_end": interactions[-1].get("timestamp") if interactions else None
        }

# Initialize global memory store
memory_store = MemoryStore()

def handle_shutdown(signum, frame):
    """Global shutdown handler"""
    sys.exit(0)

@mcp.tool()
async def get_current_conversations(input: Dict) -> Dict[str, Any]:
    """Get current session interactions. Usage: input={"input":{}} result = await mcp.call_tool('get_current_conversations', input)"""
    try:
        # Use absolute paths
        memory_root = os.path.join(ROOT_DIR, "memory")  # ROOT_DIR is already defined at top
        dt = datetime.now()
        
        # List all files in today's directory
        day_path = os.path.join(
            memory_root,
            str(dt.year),
            f"{dt.month:02d}",
            f"{dt.day:02d}"
        )
        
        if not os.path.exists(day_path):
            return {"result": {"message": "No sessions found for today"}}
            
        # Check if there's a session directory
        session_dir = os.path.join(day_path, "session")
        if os.path.isdir(session_dir):
            # Get all session directories
            session_dirs = [d for d in os.listdir(session_dir) if os.path.isdir(os.path.join(session_dir, d))]
            if not session_dirs:
                return {"result": {"message": "No session directories found"}}
                
            # Get most recent session directory
            latest_session = sorted(session_dirs)[-1]  
            session_path = os.path.join(session_dir, latest_session)
            
            # Find all JSON files in this session directory
            all_items = []
            for root, _, files in os.walk(session_path):
                for file in files:
                    if file.endswith('.json'):
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r') as f:
                            data = json.load(f)
                            if isinstance(data, list):
                                all_items.extend(data)
                            else:
                                all_items.append(data)
                                
            return {"result": {
                "session_id": latest_session,
                "interactions": [
                    item for item in all_items 
                    if isinstance(item, dict) and item.get("type") != "run_metadata"
                ]
            }}
        else:
            # Fallback to direct JSON files
            session_files = [f for f in os.listdir(day_path) if f.endswith('.json')]
            if not session_files:
                return {"result": {"message": "No session files found"}}
                
            latest_file = sorted(session_files)[-1]  # Get most recent
            file_path = os.path.join(day_path, latest_file)
            
            # Read and return contents
            with open(file_path, 'r') as f:
                data = json.load(f)
                
            return {"result": {
                        "session_id": latest_file.replace(".json", ""),
                        "interactions": [
                            item for item in data if isinstance(item, dict) and item.get("type") != "run_metadata"
                        ]
                    }}
    except Exception as e:
        print(f"[memory] Error: {str(e)}")  # Debug print
        return {"result": {"message": f"Error retrieving conversations: {str(e)}"}}

@mcp.tool()
async def search_historical_conversations(input: SearchInput) -> Dict[str, Any]:
    """Search conversation memory between user and YOU. Usage: input={"input": {"query": "anmol singh"}} result = await mcp.call_tool('search_historical_conversations', input)"""
    try:
        print(f"Searching for: '{input.query}'")
        all_memories = memory_store._list_all_memories()
        search_terms = input.query.lower().split()
        
        matches = []
        for memory in all_memories:
            # Only search in user query, final answer, and intent
            memory_content = " ".join([
                str(memory.get("user_query", "")),
                str(memory.get("final_answer", "")),
                str(memory.get("intent", "")),
                str(memory.get("text", "")),  # Also search in general memory text
            ]).lower()
            
            if all(term in memory_content for term in search_terms):
                # Only keep fields we want to return
                matches.append({
                    "user_query": memory.get("user_query", ""),
                    "final_answer": memory.get("final_answer", ""),
                    "timestamp": memory.get("timestamp", ""),
                    "intent": memory.get("intent", ""),
                    "text": memory.get("text", "")
                })

        # Sort by timestamp (most recent first)
        matches.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        
        # Count total words in matches
        total_words = 0
        filtered_matches = []
        WORD_LIMIT = 10000
        
        for match in matches:
            match_text = " ".join([
                str(match.get("user_query", "")),
                str(match.get("final_answer", "")),
                str(match.get("text", ""))
            ])
            words_in_match = len(match_text.split())
            
            if total_words + words_in_match <= WORD_LIMIT:
                filtered_matches.append(match)
                total_words += words_in_match
            else:
                break
        
        # Make the output more readable with a summary
        summary = {
            "total_matches": len(matches),
            "matches_returned": len(filtered_matches),
            "total_words": total_words
        }
        
        return {"result": {
            "summary": summary,
            "matches": filtered_matches
        }}
    except Exception as e:
        print(f"[memory] Search error: {str(e)}")
        return {"result": {"message": f"Error searching conversations: {str(e)}", "matches": []}}

if __name__ == "__main__":
    print("Memory MCP server starting...")
    
    # Setup signal handlers
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)
    
    try:
        if len(sys.argv) > 1 and sys.argv[1] == "dev":
            mcp.run()
        else:
            mcp.run(transport="stdio")
    finally:
        print("\nShutting down memory service...")
