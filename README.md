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
S3_ENDPOINT=            # S3 URL
S3_ACCESS_KEY=          # Key for S3
S3_SECRET_KEY=          # Secret key for S3
S3_BUCKET_NAME=         # S3 bucket name
 ```

 3. Download certificate for GigaChat API:
 ```
 cd ./certificate
 wget https://gu-st.ru/content/lending/russian_trusted_root_ca_pem.crt
 ```

### Running the Server

To start the development server using docker:
 ```
 docker-compose up --build
 ```

The API will be available at: http://localhost:8000