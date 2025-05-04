"""
Conversation history manager that helps retrieve and integrate past conversations into the agent context.
This module ensures the agent can access and learn from its past interactions.
"""

import asyncio
import logging
import json
from typing import List, Dict, Any, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Constants
TOOL_CALL_TIMEOUT = 10  # Timeout for tool calls in seconds

class ConversationHistoryManager:
    """
    Manages the retrieval and processing of past conversation history.
    """
    
    def __init__(self, mcp_dispatcher=None):
        """
        Initialize the conversation history manager.
        
        Args:
            mcp_dispatcher: The MCP dispatcher instance for making tool calls
        """
        self.mcp_dispatcher = mcp_dispatcher
        self.cache = {}  # Simple cache to avoid repeated calls
        # Check if tools are available
        self.available_tools = []
        
    async def _verify_tool_availability(self):
        """Verify which tools are available to avoid hanging on unavailable tools."""
        if not self.mcp_dispatcher:
            return []
            
        try:
            tools = await self.mcp_dispatcher.list_all_tools()
            logger.info(f"Available tools: {tools}")
            return tools
        except Exception as e:
            logger.error(f"Error listing available tools: {str(e)}")
            return []
    
    async def search_relevant_conversations(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search for conversations related to the current query.
        
        Args:
            query: The search query (typically the user's input)
            max_results: Maximum number of conversation history items to return
            
        Returns:
            List of relevant conversation items
        """
        # Use cached results if available
        if query in self.cache:
            logger.info(f"Using cached results for query: {query[:30]}...")
            return self.cache[query]
            
        if not self.mcp_dispatcher:
            logger.warning("No MCP dispatcher available for history search")
            return []
            
        try:
            logger.info(f"Searching conversation history for: {query[:30]}...")
            
            # Check if the required tool is available
            available_tools = await self._verify_tool_availability()
            if "search_historical_conversations" not in available_tools:
                logger.warning("Tool 'search_historical_conversations' not available")
                return []
            
            # Call the memory MCP server to search historical conversations
            search_input = {"input": {"query": query}}
            
            # Add timeout to prevent hanging indefinitely
            try:
                tool_result = await asyncio.wait_for(
                    self.mcp_dispatcher.call_tool("search_historical_conversations", search_input),
                    timeout=TOOL_CALL_TIMEOUT
                )
            except asyncio.TimeoutError:
                logger.error(f"Tool call timed out after {TOOL_CALL_TIMEOUT} seconds")
                return []
            
            # Check for empty response
            if not tool_result:
                logger.warning("Empty tool result received")
                return []
                
            # Check if content attribute exists
            if not hasattr(tool_result, 'content') or not tool_result.content:
                logger.warning("No content in search result")
                return []
                
            # Parse the result content
            try:
                content_text = tool_result.content[0].text
                data = json.loads(content_text)
            except (IndexError, AttributeError, json.JSONDecodeError) as e:
                logger.error(f"Error parsing tool result: {str(e)}")
                return []
            
            if "result" not in data:
                logger.warning(f"Unexpected response format: {data}")
                return []
                
            matches = data["result"].get("matches", [])
            logger.info(f"Found {len(matches)} matching conversations")
            
            # Limit the number of results
            limited_matches = matches[:max_results]
            
            # Cache the results
            self.cache[query] = limited_matches
            
            return limited_matches
        except Exception as e:
            logger.error(f"Error searching conversation history: {str(e)}")
            return []
    
    async def get_current_session_history(self) -> Dict[str, Any]:
        """
        Get the conversation history for the current session.
        
        Returns:
            Dictionary containing session history information
        """
        if not self.mcp_dispatcher:
            logger.warning("No MCP dispatcher available for session history")
            return {}
            
        try:
            # Check if the required tool is available
            available_tools = await self._verify_tool_availability()
            if "get_current_conversations" not in available_tools:
                logger.warning("Tool 'get_current_conversations' not available")
                return {}
                
            # Call the memory MCP server to get current session history
            tool_input = {"input": {}}
            
            # Add timeout to prevent hanging indefinitely
            try:
                tool_result = await asyncio.wait_for(
                    self.mcp_dispatcher.call_tool("get_current_conversations", tool_input),
                    timeout=TOOL_CALL_TIMEOUT
                )
            except asyncio.TimeoutError:
                logger.error(f"Tool call timed out after {TOOL_CALL_TIMEOUT} seconds")
                return {}
            
            if not tool_result or not hasattr(tool_result, 'content') or not tool_result.content:
                logger.warning("No content in current session result")
                return {}
                
            # Parse the result content
            try:
                content_text = tool_result.content[0].text
                data = json.loads(content_text)
            except (IndexError, AttributeError, json.JSONDecodeError) as e:
                logger.error(f"Error parsing tool result: {str(e)}")
                return {}
            
            if "result" not in data:
                logger.warning(f"Unexpected response format: {data}")
                return {}
                
            return data["result"]
        except Exception as e:
            logger.error(f"Error getting current session history: {str(e)}")
            return {}
    
    def format_history_for_context(self, history_items: List[Dict[str, Any]]) -> str:
        """
        Format historical conversation items into a string for inclusion in prompts.
        
        Args:
            history_items: List of conversation history items
            
        Returns:
            Formatted history text for inclusion in prompts
        """
        if not history_items:
            return ""
            
        formatted_items = []
        
        for item in history_items:
            # Convert timestamp to readable format if available
            timestamp = item.get("timestamp")
            if timestamp:
                try:
                    dt = datetime.fromtimestamp(timestamp)
                    formatted_date = dt.strftime("%Y-%m-%d %H:%M:%S")
                except (TypeError, ValueError):
                    formatted_date = str(timestamp)
            else:
                formatted_date = "Unknown time"
            
            # Format the history item
            formatted_item = f"--- Previous Conversation ({formatted_date}) ---\n"
            
            if "user_query" in item and item["user_query"]:
                formatted_item += f"Query: {item['user_query']}\n"
                
            if "final_answer" in item and item["final_answer"]:
                answer = item["final_answer"]
                # Clean up FINAL_ANSWER prefix if present
                if answer.startswith("FINAL_ANSWER:"):
                    answer = answer[len("FINAL_ANSWER:"):].strip()
                formatted_item += f"Answer: {answer}\n"
                
            if "text" in item and item["text"] and not item.get("user_query"):
                formatted_item += f"Content: {item['text']}\n"
                
            formatted_items.append(formatted_item)
            
        return "\n".join(formatted_items)

# Global instance for easy access
history_manager = None

def initialize_history_manager(mcp_dispatcher=None):
    """Initialize the global history manager instance."""
    global history_manager
    history_manager = ConversationHistoryManager(mcp_dispatcher)
    return history_manager

def get_history_manager():
    """Get the global history manager instance."""
    global history_manager
    if history_manager is None:
        logger.warning("History manager not initialized; creating with no dispatcher")
        history_manager = ConversationHistoryManager()
    return history_manager