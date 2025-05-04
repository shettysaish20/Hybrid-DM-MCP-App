import os
import json
import yaml
import requests
import logging
from pathlib import Path
from google import genai
from dotenv import load_dotenv
import heuristics  # Import the heuristics module

load_dotenv()

ROOT = Path(__file__).parent.parent
MODELS_JSON = ROOT / "config" / "models.json"
PROFILE_YAML = ROOT / "config" / "profiles.yaml"

class ModelManager:
    def __init__(self):
        self.config = json.loads(MODELS_JSON.read_text())
        self.profile = yaml.safe_load(PROFILE_YAML.read_text())

        self.text_model_key = self.profile["llm"]["text_generation"]
        self.model_info = self.config["models"][self.text_model_key]
        self.model_type = self.model_info["type"]

        # ✅ Gemini initialization (your style)
        if self.model_type == "gemini":
            api_key = os.getenv("GEMINI_API_KEY")
            self.client = genai.Client(api_key=api_key)

    async def generate_text(self, prompt: str, expected_format: str = None) -> str:
        # Apply input validation and sanitization
        is_valid, error_messages, validated_prompt = heuristics.validate_llm_input(prompt)
        if not is_valid:
            logging.warning(f"Input validation issues: {error_messages}")
        
        # Generate response using the validated prompt
        if self.model_type == "gemini":
            response = self._gemini_generate(validated_prompt)
        elif self.model_type == "ollama":
            response = self._ollama_generate(validated_prompt)
        else:
            raise NotImplementedError(f"Unsupported model type: {self.model_type}")
        
        # Apply output validation and sanitization
        is_valid, error_messages, validated_response = heuristics.validate_llm_output(response, expected_format)
        if not is_valid:
            logging.warning(f"Output validation issues: {error_messages}")
            
        # If the response was successfully parsed as a dict/object, convert it back to string
        if isinstance(validated_response, dict):
            try:
                return json.dumps(validated_response, indent=2)
            except:
                pass
                
        return validated_response

    def _gemini_generate(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model_info["model"],
            contents=prompt
        )

        # ✅ Safely extract response text
        try:
            return response.text.strip()
        except AttributeError:
            try:
                return response.candidates[0].content.parts[0].text.strip()
            except Exception:
                return str(response)

    def _ollama_generate(self, prompt: str) -> str:
        response = requests.post(
            self.model_info["url"]["generate"],
            json={"model": self.model_info["model"], "prompt": prompt, "stream": False}
        )
        response.raise_for_status()
        return response.json()["response"].strip()
