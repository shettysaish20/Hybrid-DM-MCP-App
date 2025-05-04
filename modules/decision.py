from typing import List, Optional
from modules.perception import PerceptionResult
from modules.memory import MemoryItem
from modules.model_manager import ModelManager
from modules.tools import load_prompt
from modules.history_manager import get_history_manager
import heuristics  # Import the heuristics module
import re

# Optional logging fallback
try:
    from agent import log
except ImportError:
    import datetime
    def log(stage: str, msg: str):
        now = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"[{now}] [{stage}] {msg}")

model = ModelManager()


# prompt_path = "prompts/decision_prompt.txt"

async def generate_plan(
    user_input: str, 
    perception: PerceptionResult,
    memory_items: List[MemoryItem],
    tool_descriptions: Optional[str],
    prompt_path: str,
    step_num: int = 1,
    max_steps: int = 3,
) -> str:

    """Generates the full solve() function plan for the agent."""

    # Validate user input using heuristics
    is_valid, error_messages, validated_input = heuristics.validate_llm_input(user_input)
    if not is_valid:
        log("plan", f"Input validation issues: {error_messages}")
        # Continue with the validated/sanitized input
        user_input = validated_input
        
    # Get history manager and search for relevant history
    history_manager = get_history_manager()
    history_items = []
    if history_manager:
        try:
            # Only search history if this is step 1 (initial planning)
            if step_num == 1:
                history_items = await history_manager.search_relevant_conversations(user_input)
                if history_items:
                    log("plan", f"Found {len(history_items)} relevant historical conversations for planning")
        except Exception as e:
            log("plan", f"Error fetching historical conversations: {e}")
    
    # Format history items for inclusion in the prompt
    history_context = ""
    if history_items:
        history_context = history_manager.format_history_for_context(history_items)
        log("plan", f"Added {len(history_context.split())} words of historical context to planning")

    memory_texts = "\n".join(f"- {m.text}" for m in memory_items) or "None"
    
    #log("plan", f"Memory items:\n{memory_texts}")

    prompt_template = load_prompt(prompt_path)

    # Check if the template has a {history_context} placeholder
    if "{history_context}" not in prompt_template:
        if history_context:
            # Prepare the user input with history context
            enhanced_user_input = f"[RELEVANT HISTORY]\n{history_context}\n\n[CURRENT QUERY]\n{user_input}"
            prompt = prompt_template.format(
                memory_texts=memory_texts,
                tool_descriptions=tool_descriptions,
                user_input=enhanced_user_input
            )
        else:
            prompt = prompt_template.format(
                memory_texts=memory_texts,
                tool_descriptions=tool_descriptions,
                user_input=user_input
            )
    else:
        # Template already supports history context
        prompt = prompt_template.format(
            memory_texts=memory_texts,
            tool_descriptions=tool_descriptions,
            user_input=user_input,
            history_context=history_context
        )
    
    #log("plan", f"Prompt for LLM:\n{prompt}")


    try:
        # Pass expected format (though "plan" might not have a specific JSON structure)
        raw = (await model.generate_text(prompt, expected_format="plan")).strip()
        # log("plan", f"LLM output: {raw}")

        # If fenced in ```python ... ```, extract
        if raw.startswith("```"):
            raw = raw.strip("`").strip()
            if raw.lower().startswith("python"):
                raw = raw[len("python"):].strip()

        if re.search(r"^\s*(async\s+)?def\s+solve\s*\(", raw, re.MULTILINE):
            return raw  # ✅ Correct, it's a full function
        else:
            log("plan", "⚠️ LLM did not return a valid solve(). Defaulting to FINAL_ANSWER")
            return "FINAL_ANSWER: [Could not generate valid solve()]"


    except Exception as e:
        log("plan", f"⚠️ Planning failed: {e}")
        return "FINAL_ANSWER: [unknown]"
