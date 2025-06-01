import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Model Configuration
MODEL_CONFIG = {
    'temperature': 0.7,
    'model_name': 'gpt-4.1-nano'
}

# Document Processing Configuration
DOC_CONFIG = {
    'chunk_size': 1000,
    'chunk_overlap': 100,
    'data_directory': 'data'
}

# Vector Store Configuration
VECTOR_STORE_CONFIG = {
    'similarity_search_k': 3
}

# Logging Configuration
LOG_CONFIG = {
    'filename': 'chatbot.log',
    'level': 'INFO',
    'format': '%(asctime)s - %(levelname)s - %(message)s'
}

# Evaluation Configuration
EVAL_CONFIG = {
    'metrics_file': 'evaluation_metrics.json',
    'response_time_threshold': 5.0,  # seconds
    'min_response_length': 10
} 