# modules/perception.py

from typing import List, Optional
from pydantic import BaseModel
from modules.model_manager import ModelManager
from modules.tools import load_prompt, extract_json_block
from core.context import AgentContext
import heuristics  # Import the heuristics module
import json
from modules.history_manager import get_history_manager


# Optional logging fallback
try:
    from agent import log
except ImportError:
    import datetime
    def log(stage: str, msg: str):
        now = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"[{now}] [{stage}] {msg}")

model = ModelManager()


prompt_path = r"D:\Projects\TSAI_common\Session_9_Session_27_Assignment\Hybrid-MCP-App\prompts\perception_prompt.txt"

class PerceptionResult(BaseModel):
    intent: str
    entities: List[str] = []
    tool_hint: Optional[str] = None
    tags: List[str] = []
    selected_servers: List[str] = []  # 🆕 NEW field

async def extract_perception(user_input: str, mcp_server_descriptions: dict) -> PerceptionResult:
    """
    Extracts perception details and selects relevant MCP servers based on the user query.
    """
    # Validate user input using heuristics
    is_valid, error_messages, validated_input = heuristics.validate_llm_input(user_input)
    if not is_valid:
        log("perception", f"Input validation issues: {error_messages}")
        # Continue with the validated/sanitized input
        user_input = validated_input
    
    # Get history manager and search for relevant history
    history_manager = get_history_manager()
    history_items = []
    if history_manager:
        try:
            history_items = await history_manager.search_relevant_conversations(user_input)
            if history_items:
                log("perception", f"Found {len(history_items)} relevant historical conversations")
        except Exception as e:
            log("perception", f"Error fetching historical conversations: {e}")
    
    # Format history items for inclusion in the prompt
    history_context = ""
    if history_items:
        history_context = history_manager.format_history_for_context(history_items)
        log("perception", f"Added {len(history_context.split())} words of historical context")
    
    # log("perception", f"User input: {user_input}")
    server_list = []
    for server_id, server_info in mcp_server_descriptions.items():
        description = server_info.get("description", "No description available")
        server_list.append(f"- {server_id}: {description}")

    servers_text = "\n".join(server_list)

    prompt_template = load_prompt(prompt_path)
    
    # Check if the template has a {history_context} placeholder, if not add it before the user_input
    if "{history_context}" not in prompt_template:
        if history_context:
            # Add history context before user input if there's relevant history
            prompt = prompt_template.format(
                servers_text=servers_text,
                user_input=f"[RELEVANT HISTORY]\n{history_context}\n\n[CURRENT QUERY]\n{user_input}"
            )
        else:
            prompt = prompt_template.format(
                servers_text=servers_text,
                user_input=user_input
            )
    else:
        # Template already supports history context
        prompt = prompt_template.format(
            servers_text=servers_text,
            user_input=user_input,
            history_context=history_context
        )

    try:
        # Pass expected format to generate_text for output validation
        raw = await model.generate_text(prompt, expected_format="perception")
        raw = raw.strip()
        log("perception", f"Raw output: {raw}")

        # Try parsing into PerceptionResult
        json_block = extract_json_block(raw)
        result = json.loads(json_block)

        # If selected_servers missing, fallback
        if "selected_servers" not in result:
            result["selected_servers"] = list(mcp_server_descriptions.keys())
        print("result", result)

        return PerceptionResult(**result)

    except Exception as e:
        log("perception", f"⚠️ Perception failed: {e}")
        # Fallback: select all servers
        return PerceptionResult(
            intent="unknown",
            entities=[],
            tool_hint=None,
            tags=[],
            selected_servers=list(mcp_server_descriptions.keys())
        )


async def run_perception(context: AgentContext, user_input: Optional[str] = None):

    """
    Clean wrapper to call perception from context.
    """
    return await extract_perception(
        user_input = user_input or context.user_input,
        mcp_server_descriptions=context.mcp_server_descriptions
    )

