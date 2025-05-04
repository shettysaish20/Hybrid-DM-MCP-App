"""
Heuristics module for LLM input/output validation and transformation.

This module provides functions to validate and sanitize inputs going to LLM API calls
and verify/transform outputs coming from them.
"""

import re
import json
from typing import Dict, List, Any, Optional, Union, Tuple
import logging
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Constants
MAX_INPUT_LENGTH = 100000  # Characters
MIN_INPUT_LENGTH = 3  # Characters
MAX_URL_LENGTH = 2048  # Characters
NSFW_WORDS = [
    # Add list of inappropriate words here
    "inappropriate", "offensive", "obscene"  # Placeholders
]
JSON_REQUIRED_FIELDS = {
    "tool_call": ["name", "args"],
    "perception": ["selected_servers"],
    "plan": ["steps"]
    # Add more schemas as needed
}

# Input validation functions
def validate_input_length(text: str) -> Tuple[bool, Optional[str]]:
    """
    Check if input text is within acceptable length bounds.
    
    Args:
        text: Input text to be sent to LLM
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(text) > MAX_INPUT_LENGTH:
        return False, f"Input exceeds maximum length of {MAX_INPUT_LENGTH} characters"
    if len(text) < MIN_INPUT_LENGTH:
        return False, f"Input is too short (min {MIN_INPUT_LENGTH} characters required)"
    return True, None

def validate_urls(text: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Check if URLs in text are properly formatted.
    
    Args:
        text: Input text containing URLs
        
    Returns:
        Tuple of (is_valid, error_message, fixed_text)
    """
    # Simple URL regex pattern
    url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
    urls = re.findall(url_pattern, text)
    
    fixed_text = text
    for url in urls:
        if len(url) > MAX_URL_LENGTH:
            return False, f"URL exceeds maximum length of {MAX_URL_LENGTH} characters: {url[:50]}...", None
        
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                # Try to fix the URL
                if url.startswith('www.'):
                    fixed_url = f"https://{url}"
                    fixed_text = fixed_text.replace(url, fixed_url)
                else:
                    return False, f"Invalid URL format: {url}", None
        except Exception:
            return False, f"URL parsing error: {url}", None
    
    return True, None, fixed_text

def validate_no_nsfw(text: str) -> Tuple[bool, Optional[str]]:
    """
    Check for inappropriate content in text.
    
    Args:
        text: Input text to be checked
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    lower_text = text.lower()
    for word in NSFW_WORDS:
        if word.lower() in lower_text:
            return False, f"Text contains potentially inappropriate content"
    return True, None

def validate_email_format(text: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Check if email addresses in text are properly formatted.
    
    Args:
        text: Input text containing email addresses
        
    Returns:
        Tuple of (is_valid, error_message, fixed_text)
    """
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    
    fixed_text = text
    for email in emails:
        if '@' not in email or '.' not in email.split('@')[1]:
            return False, f"Invalid email format: {email}", None
        
        # Simple heuristic to catch common email typos
        domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"]
        typo_variants = ["gmial.com", "yaho.com", "outlock.com", "hotmial.com"]
        for typo, correct in zip(typo_variants, domains):
            if email.lower().endswith(f"@{typo}"):
                corrected_email = email.replace(typo, correct)
                fixed_text = fixed_text.replace(email, corrected_email)
    
    return True, None, fixed_text

# Output validation functions
def validate_json_parsable(text: str) -> Tuple[bool, Optional[str], Optional[Dict]]:
    """
    Check if output text is valid JSON and return parsed object.
    
    Args:
        text: Output text from LLM that should be JSON
        
    Returns:
        Tuple of (is_valid, error_message, parsed_json)
    """
    # First try to find JSON-like content within markdown code blocks
    json_block_pattern = r'```(?:json)?\s*([\s\S]*?)\s*```'
    match = re.search(json_block_pattern, text)
    
    if match:
        json_text = match.group(1).strip()
    else:
        # If no code blocks, try the whole text
        json_text = text.strip()
    
    # Look for common JSON formatting errors and try to fix them
    # Replace single quotes with double quotes
    json_text = re.sub(r"'([^']*)':\s*", r'"\1": ', json_text)
    json_text = re.sub(r":\s*'([^']*)'", r': "\1"', json_text)
    
    # Add quotes to unquoted keys
    json_text = re.sub(r'([{,]\s*)([a-zA-Z0-9_]+)(\s*:)', r'\1"\2"\3', json_text)
    
    try:
        parsed_json = json.loads(json_text)
        return True, None, parsed_json
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON format: {str(e)}", None

def validate_required_fields(json_obj: Dict, schema_key: str) -> Tuple[bool, Optional[str], Optional[Dict]]:
    """
    Validate that JSON has all required fields for a specific schema.
    
    Args:
        json_obj: Parsed JSON object
        schema_key: Key identifying which validation schema to use
        
    Returns:
        Tuple of (is_valid, error_message, fixed_json)
    """
    if schema_key not in JSON_REQUIRED_FIELDS:
        return True, None, json_obj
    
    required_fields = JSON_REQUIRED_FIELDS[schema_key]
    missing_fields = [field for field in required_fields if field not in json_obj]
    
    if missing_fields:
        # Try to fix by adding default values
        fixed_json = json_obj.copy()
        for field in missing_fields:
            if field == "name":
                fixed_json[field] = "default_tool"
            elif field == "args":
                fixed_json[field] = {}
            elif field == "selected_servers":
                fixed_json[field] = []
            elif field == "steps":
                fixed_json[field] = []
            else:
                fixed_json[field] = None
        
        return False, f"Missing required fields: {missing_fields}", fixed_json
    
    return True, None, json_obj

def validate_empty_values(json_obj: Dict) -> Tuple[bool, Optional[str], Optional[Dict]]:
    """
    Check if any keys in the JSON have empty values.
    
    Args:
        json_obj: Parsed JSON object
        
    Returns:
        Tuple of (is_valid, error_message, fixed_json)
    """
    empty_keys = []
    fixed_json = json_obj.copy()
    
    def check_empty(obj, path=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                new_path = f"{path}.{k}" if path else k
                if v is None or (isinstance(v, str) and not v.strip()):
                    empty_keys.append(new_path)
                    # Try to set a default value based on key name
                    if "name" in k.lower():
                        obj[k] = "unnamed_item"
                    elif "description" in k.lower():
                        obj[k] = "No description provided."
                    elif "url" in k.lower():
                        obj[k] = "https://example.com"
                    else:
                        obj[k] = "N/A"
                elif isinstance(v, (dict, list)):
                    check_empty(v, new_path)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                check_empty(item, f"{path}[{i}]")
    
    check_empty(fixed_json)
    
    if empty_keys:
        return False, f"Found empty values for keys: {empty_keys}", fixed_json
    
    return True, None, fixed_json

# Main validation functions
def validate_llm_input(text: str) -> Tuple[bool, List[str], str]:
    """
    Run all input validation checks and return results.
    
    Args:
        text: Input text to be sent to LLM
        
    Returns:
        Tuple of (is_valid, error_messages, fixed_text)
    """
    is_valid = True
    error_messages = []
    fixed_text = text
    
    # Check input length
    length_valid, length_error = validate_input_length(text)
    if not length_valid:
        is_valid = False
        error_messages.append(length_error)
        # Truncate if too long
        if len(text) > MAX_INPUT_LENGTH:
            fixed_text = text[:MAX_INPUT_LENGTH - 100] + "... [truncated]"
    
    # Check URLs
    urls_valid, urls_error, urls_fixed = validate_urls(fixed_text)
    if not urls_valid:
        is_valid = False
        error_messages.append(urls_error)
    elif urls_fixed:
        fixed_text = urls_fixed
    
    # Check for inappropriate content
    nsfw_valid, nsfw_error = validate_no_nsfw(fixed_text)
    if not nsfw_valid:
        is_valid = False
        error_messages.append(nsfw_error)
        # Don't return fixed text in this case, let the caller decide how to handle NSFW content
    
    # Check email format
    email_valid, email_error, email_fixed = validate_email_format(fixed_text)
    if not email_valid:
        is_valid = False
        error_messages.append(email_error)
    elif email_fixed:
        fixed_text = email_fixed
    
    return is_valid, error_messages, fixed_text

def validate_llm_output(text: str, expected_format: str = None) -> Tuple[bool, List[str], Any]:
    """
    Run all output validation checks and return results.
    
    Args:
        text: Output text from LLM
        expected_format: Expected output format (e.g., "json", "tool_call")
        
    Returns:
        Tuple of (is_valid, error_messages, fixed_output)
    """
    is_valid = True
    error_messages = []
    fixed_output = text
    
    # If JSON output is expected
    if expected_format in ["json", "tool_call", "perception", "plan"]:
        json_valid, json_error, parsed_json = validate_json_parsable(text)
        if not json_valid:
            is_valid = False
            error_messages.append(json_error)
            fixed_output = text  # Can't fix invalid JSON
        else:
            # Check required fields if a schema is specified
            if expected_format in JSON_REQUIRED_FIELDS:
                fields_valid, fields_error, fields_fixed = validate_required_fields(parsed_json, expected_format)
                if not fields_valid:
                    is_valid = False
                    error_messages.append(fields_error)
                    parsed_json = fields_fixed
            
            # Check empty values
            empty_valid, empty_error, empty_fixed = validate_empty_values(parsed_json)
            if not empty_valid:
                is_valid = False
                error_messages.append(empty_error)
                parsed_json = empty_fixed
            
            fixed_output = parsed_json
    
    return is_valid, error_messages, fixed_output

def apply_heuristics_to_llm_call(input_text: str, output_text: str, expected_format: str = None) -> Dict[str, Any]:
    """
    Apply all input and output heuristics to an LLM call.
    
    Args:
        input_text: The text sent to the LLM
        output_text: The text received from the LLM
        expected_format: Expected output format
        
    Returns:
        Dictionary with validation results and fixed texts
    """
    input_valid, input_errors, fixed_input = validate_llm_input(input_text)
    output_valid, output_errors, fixed_output = validate_llm_output(output_text, expected_format)
    
    return {
        "input": {
            "original": input_text,
            "valid": input_valid,
            "errors": input_errors,
            "fixed": fixed_input
        },
        "output": {
            "original": output_text,
            "valid": output_valid,
            "errors": output_errors,
            "fixed": fixed_output
        },
        "overall_valid": input_valid and output_valid
    }

# Integration function for the existing agent loop
async def validate_and_fix_llm_interaction(prompt: str, response: str, expected_format: str = None) -> Tuple[str, str, Dict]:
    """
    Asynchronous function to validate and fix LLM inputs and outputs.
    
    Args:
        prompt: The prompt sent to the LLM
        response: The response received from the LLM
        expected_format: Expected output format
        
    Returns:
        Tuple of (fixed_prompt, fixed_response, validation_info)
    """
    validation_results = apply_heuristics_to_llm_call(prompt, response, expected_format)
    
    # Log validation issues
    if not validation_results["input"]["valid"]:
        logger.warning(f"Input validation issues: {validation_results['input']['errors']}")
    
    if not validation_results["output"]["valid"]:
        logger.warning(f"Output validation issues: {validation_results['output']['errors']}")
    
    return (
        validation_results["input"]["fixed"],
        validation_results["output"]["fixed"],
        validation_results
    )