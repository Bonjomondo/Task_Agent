"""
Gemini API client for interacting with Google's Gemini models
"""

import os
import logging
from typing import Optional, Dict, Any
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class GeminiClient:
    """Client for interacting with Gemini API"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-pro"):
        """
        Initialize Gemini client
        
        Args:
            api_key: Gemini API key (defaults to GEMINI_API_KEY env var)
            model: Model name to use (default: gemini-pro)
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key not provided. Set GEMINI_API_KEY environment variable.")
        
        self.model_name = model
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
        logger.info(f"Initialized Gemini client with model: {self.model_name}")
    
    def generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 4096) -> str:
        """
        Generate text using Gemini API
        
        Args:
            prompt: Input prompt
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
        """
        try:
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens
            )
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            if not response.text:
                logger.error("Empty response from Gemini API")
                raise ValueError("Empty response from Gemini API")
            
            logger.debug(f"Generated {len(response.text)} characters")
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating content: {str(e)}")
            raise
    
    def chat(self, messages: list, temperature: float = 0.7) -> str:
        """
        Have a conversation with Gemini
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Sampling temperature
            
        Returns:
            Generated response
        """
        try:
            chat = self.model.start_chat(history=[])
            
            for msg in messages[:-1]:  # Add history
                if msg['role'] == 'user':
                    chat.send_message(msg['content'])
            
            # Send last message and get response
            last_msg = messages[-1]['content']
            response = chat.send_message(last_msg)
            
            return response.text
            
        except Exception as e:
            logger.error(f"Error in chat: {str(e)}")
            raise
