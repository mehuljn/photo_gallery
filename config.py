import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB limit

    # --- Gemini API Configuration ---
    # For Google AI Studio API Key (simpler for quick dev)
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY') # Get this from aistudio.google.com/app/apikey
    GEMINI_MODEL_NAME = 'gemini-1.5-flash' # Or 'gemini-1.5-flash-latest' if you want the newest stable version

    # For Vertex AI (more robust, enterprise-ready, requires GCP project and service account)
    # Set GOOGLE_APPLICATION_CREDENTIALS env var to your service account key file path
    # If using Vertex AI, you'll also need PROJECT_ID and LOCATION
    GCP_PROJECT_ID = os.environ.get('GCP_PROJECT_ID') # Your Google Cloud Project ID
    GCP_LOCATION = os.environ.get('GCP_LOCATION', 'us-central1') # e.g., 'us-central1'
