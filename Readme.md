📸 AI-Powered Flask Photo Gallery with Gemini 1.5 Flash
Overview
This project showcases a dynamic Flask-based photo gallery enhanced with an interactive AI chat assistant. Leveraging Google's Gemini 1.5 Flash API, the AI can "see" and understand the content of your webpage by taking real-time snapshots. Users can upload images, browse their gallery, and then ask the AI questions about the displayed content, receiving intelligent, context-aware responses.

Features
Photo Upload: Easily upload images to your gallery.
Dynamic Gallery Display: View all your uploaded photos in a responsive grid.
Interactive AI Chatbot: A floating chat bubble provides direct access to an AI assistant.
Multimodal AI Interaction: When you ask a question, the application captures a snapshot of the current webpage. This image, along with your text query, is sent to Google's Gemini 1.5 Flash.
Context-Aware Responses: Gemini 1.5 Flash processes both the visual (snapshot) and textual input to provide highly relevant and intelligent answers.
Simple & Clean UI: A straightforward interface focused on core functionality.
Technologies Used
Backend:
Flask: A lightweight Python web framework.
Google Gemini 1.5 Flash API: For powerful multimodal AI capabilities.
Python: The core programming language.
Frontend:
HTML/CSS: For structuring and styling the web pages.
JavaScript: For dynamic interactions and API calls.
html2canvas: A JavaScript library used to take screenshots of the DOM.
Getting Started
Follow these steps to get your AI-powered photo gallery up and running locally.

Prerequisites
Python 3.8+ installed
A Google Cloud Project (optional, for Vertex AI) or an API Key from Google AI Studio (easiest for development):
Go to Google AI Studio.
Create a new API key.
Important: Keep this API key secure. You'll set it as an environment variable.
1. Clone the Repository
Bash

git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
2. Set Up Virtual Environment
It's good practice to use a virtual environment to manage dependencies.

Bash

python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
3. Install Dependencies
Bash

pip install Flask google-generativeai Pillow
4. Configure Your Gemini API Key
Set your Gemini API key as an environment variable. Replace YOUR_GEMINI_API_KEY with the actual key you obtained from Google AI Studio.

Bash

# On macOS/Linux
export GEMINI_API_KEY='YOUR_GEMINI_API_KEY'

# On Windows (in Command Prompt)
set GEMINI_API_KEY=YOUR_GEMINI_API_KEY
5. Create Uploads Directory
The application needs a place to store uploaded images.

Bash

mkdir static/uploads
6. Run the Flask Application
Bash

flask run
Usage
Open your browser to http://127.0.0.1:5000/.
Use the "Upload Image" link to add some photos to your gallery.
Click the 💬 chat bubble in the bottom-right corner to open the AI assistant.
Type your question related to what you see on the page (e.g., "Describe the images in the gallery," "What's the main color of the header?").
Press Enter or click "Send" to get a response from Gemini 1.5 Flash!
Project Structure
photo_gallery/
├── app.py              # Main Flask application logic, routes, Gemini integration
├── config.py           # Application configuration, API keys, paths
├── static/
│   ├── uploads/        # Directory for uploaded images
│   ├── chat.js         # Frontend JavaScript for chat UI and API calls
│   └── style.css       # CSS for general styling and chat UI
└── templates/
    ├── index.html      # Gallery display page
    ├── upload.html     # Image upload form
    └── base.html       # Base template for consistent UI elements (like chat bubble)
License
This project is open-source
