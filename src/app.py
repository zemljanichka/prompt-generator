import os
import csv
from fastapi import FastAPI, Request, Query, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from typing import Optional, Dict
from pydantic import BaseModel
import random

from utils import generate_scenarios_characters, get_localized_data, construct_prompt, setup_i18n, get_yandex_token
from api_clients import YandexGPTClient, GigaChatClient


app = FastAPI(title="Prompt generator")

API_URL = os.environ.get('API_URL', 'http://localhost:8000')

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "PATCH", "DELETE", "PUT"],
    allow_headers=["*"],
)

# Configure templates
templates = Jinja2Templates(directory="templates")

# Define request model
class PromptUpdate(BaseModel):
    description: Optional[str] = None
    case1: Optional[str] = None
    case2: Optional[str] = None
    ending: Optional[str] = None
    lang: str = "en"

class PromptResponse(BaseModel):
    prompt: str
    characters: Dict[str, str]

def generate_prompt_text(lang: str, description: Optional[str] = None, case1: Optional[str] = None, case2: Optional[str] = None, ending: Optional[str] = "") -> PromptResponse:
    """
    Helper function to generate prompt text.
    
    Args:
        lang: Language code
        description: Optional custom description
        case1: Optional custom case 1
        case2: Optional custom case 2
        ending: Optional ending text
        
    Returns:
        PromptResponse: Generated prompt text and character lists
    """
    # Set up translations
    _ = setup_i18n(lang)

    dimension = random.choice(["species", "social_value", "gender", "age", "fitness", "utilitarianism", "random"])
    
    # Generate pedestrian sets
    pedestrians_set_1, pedestrians_set_2, scenario_info = generate_scenarios_characters(lang, dimension)
    
    # Get all language-specific strings
    (
        animals, people,                     # Species groups
        low_status, neutral_status, high_status,  # Social groups
        females, males,                      # Gender groups
        age_pairs, fitness_pairs,           # Paired groups
        all_chars, plural_forms,            # Character lists
        text_joins,                         # Text formatting
        base_description,                   # Base description
        case1_description,                  # Case 1 description
        case2_description,                  # Case 2 description
        case1_header,                       # Case 1 header
        case2_header                        # Case 2 header
    ) = get_localized_data(lang)
    
    # Use default descriptions if not provided
    description = description or base_description
    case1 = case1 or case1_description
    case2 = case2 or case2_description
    
    prompt = construct_prompt(
        description=description,
        case1=case1,
        case2=case2,
        pedestrians_set_1=pedestrians_set_1,
        pedestrians_set_2=pedestrians_set_2,
        case1_header=case1_header,
        case2_header=case2_header,
        ending=ending,
        lang=lang
    )

    return PromptResponse(
        prompt=prompt,
        characters={
            "case1": pedestrians_set_1,
            "case2": pedestrians_set_2
        },
        scenario_info=scenario_info
    )

@app.get("/")
async def generate_prompt(request: Request, lang: str = "en"):
    """
    Generate a new prompt based on the specified language.
    
    Args:
        request: FastAPI request object
        lang: The language code for prompt generation
        
    Returns:
        dict: Generated prompt data or HTML template
    """
    # Generate the initial prompt
    prompt_response = generate_prompt_text(lang)
    
    # If the client accepts HTML, return the template with the initial prompt
    if request.headers.get("accept", "").startswith("text/html"):
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "initial_prompt": prompt_response.prompt,
                "initial_characters": prompt_response.characters,
                "api_path": API_URL,
                "lang": lang  # Pass the language to the template
            }
        )
    
    # Otherwise, return the prompt as JSON
    return prompt_response

@app.post("/")
async def update_prompt(prompt_data: PromptUpdate) -> PromptResponse:
    """
    Update an existing prompt with new parameters.
    
    Args:
        prompt_data: PromptUpdate model containing update parameters
        
    Returns:
        PromptResponse: Updated prompt data and character lists
    """
    return generate_prompt_text(
        lang=prompt_data.lang,
        description=prompt_data.description,
        case1=prompt_data.case1,
        case2=prompt_data.case2,
        ending=prompt_data.ending
    )

@app.post("/startup")
async def send_prompt(
    base_description: str = Body(..., description="Base description text"),
    case1_description: str = Body(..., description="Case 1 description"),
    case2_description: str = Body(..., description="Case 2 description"),
    ending: str = Body(..., description="Optional ending text"),
    batch_size: int = Query(default=1, ge=1, le=100000),
    model: str = Query(..., regex="^(yandexGPT|gigaChat|chatGPT|lmStudio)$"),
    lang: str = Query(default="en", regex="^(en|ru)$")
) -> dict:
    """
    Startup endpoint for sending prompts to AI models.
    
    Args:
        base_description: Base description text
        case1_description: Case 1 description
        case2_description: Case 2 description
        ending: Optional ending text
        batch_size: Number of prompts to generate (1-100000)
        model: AI model to use
        lang: Language code
        
    Returns:
        dict: Response status
    """
    if model == "yandexGPT":
        catalog_id = os.environ.get("CATALOG_ID_YANDEXGPT")
        api_key = get_yandex_token()
        assert catalog_id and api_key, 'no keys specified...'

        client = YandexGPTClient(catalog_id, api_key)

        system_content = base_description

        prompt = generate_prompt_text(
            description="  ",
            case1=case1_description,
            case2=case2_description,
            ending=ending,
            lang=lang
        )
        user_content = prompt.prompt
        response = client.generate_response(system_content, user_content, verbose=True)
        if response:
            print("\n--- Response ---")
            response = response.json()
            print(response)
            print("------------------")
        else:
            print("\nCould not retrieve a response.")
            raise HTTPException(status_code=500)

    elif model == "gigaChat":
        api_key = os.environ.get("API_KEY_GIGACHAT")
        assert api_key, 'no keys specified...'

        client = GigaChatClient(api_key)

        prompt = generate_prompt_text(
            description=base_description,
            case1=case1_description,
            case2=case2_description,
            ending=ending,
            lang=lang
        )
        user_content = prompt.prompt
        response = client.generate_response(user_content)

        if response:
            print("\n--- Response ---")
            response = response.json()
            print(response)
            print("------------------")
        else:
            print("\nCould not retrieve a response.")
            raise HTTPException(status_code=500)
        
    elif model == "chatGPT":
        pass
    
    return {
        "status": "accepted",
        "model": model,
        "batch_size": batch_size,
        "lang": lang,
        "response": response,
        "prompt": prompt.prompt,
    }
