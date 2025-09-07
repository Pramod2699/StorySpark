# Standard library imports
import os
from datetime import date
from typing import Any, Dict, Optional
from src.utils.Logger import Logger

# Third-party imports
from openai import OpenAI


class AIHelper:
    """Helper class for generating responses and managing interactions with OpenAI's API."""

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize the AIHelper with a logger and configuration.

        Args:
            logger: Logger instance for logging operations.
            config: Configuration dictionary containing OpenAI API settings.
        """
        self._logger = Logger()
        self._config = config
        os.environ["OPENAI_API_KEY"] = self._config["openai"]["credentials"]["default"]
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


    def genrate_from_prompt(self, model, prompt, temperature=0, n=1) -> str:
        """
        Generates responses based on a given prompt using the OpenAI API.

        Args:
            model (str): The model identifier to use for generating responses (e.g., `gpt-4o-2024-08-06`).
            prompt (str): The input text guiding the generation process.
            temperature (float, optional): A parameter controlling the randomness of the output (default is 0).
            n (int, optional): The number of response choices to generate (default is 1).

        Returns:
            list:
                - On success: A list of generated response choices from the OpenAI API.
                - On failure: Returns False, indicating that response generation failed.

        Process:
            1. The OpenAI API is called using the specified `model`, `prompt`, and optional parameters like `temperature` and `n`.
            2. A maximum of 1025 tokens are generated in the completion.
            3. The first generated response is logged, along with total token usage for the request.
            4. The function returns the list of response choices if successful.
            5. If an error occurs during the API call, the error is logged, and the function returns False.
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1025,
                temperature=temperature,
                n=n,
                stop=None,
            )
            self._logger.info(
                f"Response Created: {str(response.choices[0].message.content)}"
            )
            if response.usage:
                self._logger.critical(f"Total Token {response.usage.total_tokens}")
            if response.choices[0].message.content:
                return response.choices[0].message.content
            else:
                return ""
        except Exception as e:
            self._logger.critical("Not able to genrate answer")
            self._logger.exception(e)
            return ""
