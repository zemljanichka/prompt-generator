"""YandexGPT API client for handling requests and responses."""
import os
import requests
import json
import time
from typing import Optional, Dict, Any
from getpass import getpass



class YandexGPTClient:
    """Client for interacting with YandexGPT API."""
    
    BASE_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1"
    
    def __init__(self, catalog_id: str, api_key: str):
        """
        Initialize YandexGPT client.
        
        Args:
            catalog_id: Yandex Cloud Catalog ID
            api_key: Yandex Cloud Service Account API Key
        """
        self.catalog_id = catalog_id
        self.api_key = api_key
        
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests."""
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
    def _prepare_completion_request(self, system_content: str, user_content: str) -> Dict[str, Any]:
        """Prepare the completion request payload."""
        return {
            "modelUri": f"gpt://{self.catalog_id}/yandexgpt/latest",
            "completionOptions": {
                "stream": False,
                "temperature": 0,
                "maxTokens": "2000"
            },
            "messages": [
                {"role": "system", "text": system_content},
                {"role": "user", "text": user_content}
            ]
        }
        
    def send_request(self, system_content: str, user_content: str) -> Optional[str]:
        """
        Send an asynchronous request to YandexGPT.
        
        Args:
            system_content: System message content
            user_content: User message content
            
        Returns:
            Optional[str]: Request ID if successful, None otherwise
        """
        response = requests.post(
            f"{self.BASE_URL}/completion",
            headers=self._get_headers(),
            json=self._prepare_completion_request(system_content, user_content)
        )
    
        return response
            
    def get_response(
        self,
        request_id: str,
        max_attempts: int = 10,
        delay: int = 3,
        verbose: bool = False
    ) -> Optional[str]:
        """
        Get response for a previously sent request.
        
        Args:
            request_id: Request ID from send_request
            max_attempts: Maximum number of attempts to get the response
            delay: Delay between attempts in seconds
            verbose: Whether to print response details
            
        Returns:
            Optional[str]: Response text if successful, None otherwise
        """
        result_url = f"https://llm.api.cloud.yandex.net/operations/{request_id}"
        
        for attempt in range(max_attempts):
            try:
                response = requests.get(result_url, headers=self._get_headers())
                response.raise_for_status()
                data = response.json()
                
                if verbose:
                    print(f"Attempt {attempt + 1}, Status: {'Done' if data.get('done') else 'In Progress'}")
                    
                if data.get("done", False):
                    if "response" in data:
                        alternatives = data["response"].get("alternatives", [])
                        if alternatives:
                            return alternatives[0].get("message", {}).get("text")
                    elif "error" in data:
                        print(f"YandexGPT operation finished with an error: {data['error']}")
                        return None
                    return None
                    
                time.sleep(delay)
                
            except requests.exceptions.RequestException as e:
                print(f"Error getting response on attempt {attempt + 1}: {e}")
                if e.response:
                    print(f"Response body: {e.response.text}")
                time.sleep(delay)
                
        print("Failed to get response after multiple attempts.")
        return None
        
    def generate_response(
        self,
        system_content: str,
        user_content: str,
        max_attempts: int = 10,
        delay: int = 3,
        verbose: bool = False
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
        request = self.send_request(system_content, user_content)
        if not request:
            return None
        return request


if __name__ == '__main__':
    # This block demonstrates how to use the YandexGPTClient for a single request.
    # It will prompt for credentials and then send a predefined prompt.
    try:
        catalog_id = os.environ.get("CATALOG_ID_YANDEXGPT")
        api_key = os.environ.get("API_KEY_YANDEXGPT")

        client = YandexGPTClient(catalog_id, api_key)

        # Example prompt
        system_content = "You are a helpful assistant."
        user_content = "Tell me a short story about a robot."
        
        print("\nSending request to YandexGPT...")
        response = client.generate_response(system_content, user_content, verbose=True)

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
