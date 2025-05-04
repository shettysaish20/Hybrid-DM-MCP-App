from typing import List, Optional
from modules.perception import PerceptionResult
from modules.memory import MemoryItem
from modules.model_manager import ModelManager
from modules.tools import load_prompt
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

    memory_texts = "\n".join(f"- {m.text}" for m in memory_items) or "None"
    
    #log("plan", f"Memory items:\n{memory_texts}")

    prompt_template = load_prompt(prompt_path)

    prompt = prompt_template.format(
        # memory_texts=memory_texts,
        tool_descriptions=tool_descriptions,
        user_input=user_input
    )
    
    log("plan", f"Prompt for LLM:\n{prompt}")


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
