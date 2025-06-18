from itertools import product
from collections import Counter
import requests
from getpass import getpass
import uuid
from typing import Dict, Any, Optional
import os

class GigaChatClient:
    """Client for interacting with GigaChat API."""
    
    TOKEN_URL = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    API_URL = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    
    def __init__(self, api_key: str):
        """
        Initialize GigaChat client.
        
        Args:
            catalog_id: Yandex Cloud Catalog ID
            api_key: Yandex Cloud Service Account API Key
        """
        self.api_key = api_key


        payload={"scope": "GIGACHAT_API_PERS"}
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'Authorization': f'Basic {self.api_key}',
        'RqUID': str(uuid.uuid4())
        }

        response = requests.request("POST", self.TOKEN_URL, headers=headers, data=payload, verify="./api_clients/certificate/russian_trusted_root_ca_pem.crt")

        self.access_token = response.json()["access_token"]

        payload={}
        
        
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests."""
        return {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {self.access_token}'
        }
    
    def _prepare_completion_request(self, user_content: str) -> Dict[str, Any]:
        """Prepare the completion request payload."""
        return {
        "model": "GigaChat",
        "messages": [
            {
            "role": "user",
            "content": user_content,
            }
        ],
        "stream": False,
        "repetition_penalty": 1,
        }

    def send_request(self, user_content:str):
        print(self._prepare_completion_request(user_content))

        response = requests.request("POST", self.API_URL, headers=self._get_headers(), json=self._prepare_completion_request(user_content), verify="./api_clients/certificate/russian_trusted_root_ca_pem.crt")
        print(response)
        print(response.text)
        return response

    
    def generate_response(
        self,
        user_content: str,
        max_attempts: int = 10,
        delay: int = 3,
    ) -> Optional[str]:
        """
        Send request and get response in one call.
        
        Args:
            system_content: System message content
            user_content: User message content
            max_attempts: Maximum number of attempts to get the response
            delay: Delay between attempts in seconds
            verbose: Whether to print response details
            
        Returns:
            Optional[str]: Response text if successful, None otherwise
        """
        request = self.send_request(user_content)
        if not request:
            return None
        return request

if __name__ == '__main__':
    # This block demonstrates how to use the GigaChatClient for a single request.
    # It will prompt for credentials and then send a predefined prompt.
    try:
        api_key = os.environ.get("API_KEY_GIGACHAT")

        client = GigaChatClient(api_key)

        # Example prompt
        user_content = "Tell me a short story about a robot."
        
        print("\nSending request to GigaChat...")
        response = client.generate_response(user_content)

        if response:
            print("\n--- Response ---")
            print(response.json())
            print("------------------")
        else:
            print("\nCould not retrieve a response.")

    except (KeyboardInterrupt, EOFError):
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
