"""
Gemini Multimodal Client Module
Handles authentication, model initialization, multimodal vision queries,
and text generation with graceful fallback to Demonstration Mode.
"""

import os
import json
import re
from typing import Optional, Dict, Any, Tuple
from PIL import Image

# Try importing the new google.genai or fallback to google.generativeai
GENAI_SDK_TYPE = None
try:
    from google import genai
    from google.genai import types
    GENAI_SDK_TYPE = "genai"
except ImportError:
    try:
        import google.generativeai as legacy_genai
        GENAI_SDK_TYPE = "legacy"
    except ImportError:
        GENAI_SDK_TYPE = None


def clean_json_response(raw_text: str) -> Dict[str, Any]:
    """
    Cleans markdown formatting such as ```json ... ``` and parses raw LLM output into JSON.
    """
    if not raw_text:
        raise ValueError("Empty response received from LLM")
    
    # Strip markdown code blocks if present
    text = raw_text.strip()
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if match:
        text = match.group(1).strip()
        
    try:
        return json.loads(text)
    except json.JSONDecodeError as err:
        # Fallback regex extraction if there are surrounding comments
        json_obj_match = re.search(r"(\{[\s\S]*\})", text)
        if json_obj_match:
            return json.loads(json_obj_match.group(1))
        raise ValueError(f"Could not parse valid JSON from response: {err}\nRaw text:\n{raw_text}")


class GeminiVisionEngine:
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-2.5-flash"):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "").strip()
        self.model_name = model_name
        self.is_live = False
        self.client = None
        self._init_client()

    def _init_client(self):
        """Initializes the client if a key is provided."""
        if not self.api_key:
            self.is_live = False
            return

        try:
            if GENAI_SDK_TYPE == "genai":
                self.client = genai.Client(api_key=self.api_key)
                self.is_live = True
            elif GENAI_SDK_TYPE == "legacy":
                legacy_genai.configure(api_key=self.api_key)
                self.client = legacy_genai.GenerativeModel(self.model_name)
                self.is_live = True
            else:
                self.is_live = False
        except Exception:
            self.is_live = False

    def query_multimodal(self, prompt: str, image: Image.Image) -> Tuple[Optional[str], Optional[str]]:
        """
        Sends an image + prompt to Gemini.
        Returns: (response_text, error_message)
        """
        if not self.is_live or not self.client:
            return None, "No active Gemini API key configured. Operating in Demonstration Mode."

        try:
            if GENAI_SDK_TYPE == "genai":
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=[prompt, image]
                )
                return response.text, None
            elif GENAI_SDK_TYPE == "legacy":
                # Fallback model selection if specified model isn't available
                model_to_use = self.client
                response = model_to_use.generate_content([prompt, image])
                return response.text, None
        except Exception as e:
            err_msg = str(e)
            # Check for invalid key or quota
            return None, f"Gemini API request failed: {err_msg}"

    def query_text(self, prompt: str, system_instruction: Optional[str] = None) -> Tuple[Optional[str], Optional[str]]:
        """
        Queries Gemini with pure text for the engineering chatbot assistant.
        Returns: (response_text, error_message)
        """
        if not self.is_live or not self.client:
            return None, "No active Gemini API key configured. Operating in Demonstration Mode."

        try:
            full_prompt = f"System: {system_instruction}\n\nUser: {prompt}" if system_instruction else prompt
            if GENAI_SDK_TYPE == "genai":
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=full_prompt
                )
                return response.text, None
            elif GENAI_SDK_TYPE == "legacy":
                response = self.client.generate_content(full_prompt)
                return response.text, None
        except Exception as e:
            return None, f"Gemini Chat API request failed: {str(e)}"
