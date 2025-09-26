import json
import ollama
import re

def llm_structuring(prompt: str) -> dict:
    """
    Sends a prompt to the Ollama model and returns the structured JSON output as a Python dict.

    Returns:
        dict: {
            "table": [...],
            "confidence": float,
            "flags": [...]
        }
        Returns None if LLM output cannot be parsed.
    """
    try:
        response = ollama.chat(
            model="llama3.1",
            messages=[{"role": "user", "content": prompt}],
        )

        raw_output = response.get("message", {}).get("content", "")
        if not raw_output:
            print("LLM returned empty response")
            return None

        match = re.search(r"\{.*\}", raw_output, flags=re.DOTALL)
        if not match:
            print("No JSON object found in LLM output")
            print("Raw output:\n", raw_output)
            return None

        json_str = match.group(0)

        # Convert string output to dict
        try:
            structured = json.loads(raw_output)
            return structured
        except json.JSONDecodeError as e:
            print(f"Failed to parse LLM output as JSON: {e}")
            print("Raw LLM output:\n", raw_output)
            return None

    except Exception as e:
        print(f"Error in llm_structuring: {e}")
        return None
