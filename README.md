# Prompt-generator

A FastAPI-based service for generating and processing scenarios for research of moral bias of LLM

### Installation

1. Clone the repository:
 ```
   git clone https://github.com/zemljanichka/prompt-generator
 ```

2. Fill .env file:
 ```
AUTH_KEY_YANDEXGPT=     # OAuth-token yandexgpt
CATALOG_ID_YANDEXGPT=   # Yandexgpt catalog id
API_KEY_GIGACHAT=       # Api-key for gigachat
 ```

### Running the Server

To start the development server using docker:
 ```
 docker-compose up --build
 ```

The API will be available at: http://localhost:8000