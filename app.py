from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from config import Config
import os
import base64
# import requests # No longer needed for Ollama

# --- Import Gemini SDK ---
import google.generativeai as genai
# If using Vertex AI:
# from google.cloud import aiplatform

app = Flask(__name__)
app.config.from_object(Config)

# --- Configure Gemini API ---
if app.config.get('GEMINI_API_KEY'):
    genai.configure(api_key=app.config['GEMINI_API_KEY'])
    app.logger.info("Configured Gemini with API Key.")
elif app.config.get('GCP_PROJECT_ID') and app.config.get('GCP_LOCATION'):
    # For Vertex AI, the SDK will automatically pick up GOOGLE_APPLICATION_CREDENTIALS
    # Ensure google-cloud-aiplatform is installed
    app.logger.info(f"Configured for Vertex AI with Project ID: {app.config['GCP_PROJECT_ID']}, Location: {app.config['GCP_LOCATION']}")
    # You might need to explicitly initialize the client for Vertex AI usage
    # aiplatform.init(project=app.config['GCP_PROJECT_ID'], location=app.config['GCP_LOCATION'])
else:
    app.logger.warning("Neither GEMINI_API_KEY nor GOOGLE_APPLICATION_CREDENTIALS/GCP_PROJECT_ID are set. Gemini API will not work.")

# Initialize the Gemini model
try:
    if app.config.get('GCP_PROJECT_ID'): # Using Vertex AI
        from vertexai.preview.generative_models import GenerativeModel, Part, Image  # New imports for Vertex AI
        # This will use the default credentials picked up from GOOGLE_APPLICATION_CREDENTIALS
        model = GenerativeModel(app.config['GEMINI_MODEL_NAME'])
        app.logger.info(f"Initialized Gemini model for Vertex AI: {app.config['GEMINI_MODEL_NAME']}")
    else: # Using Google AI Studio API Key
        model = genai.GenerativeModel(app.config['GEMINI_MODEL_NAME'])
        app.logger.info(f"Initialized Gemini model for AI Studio: {app.config['GEMINI_MODEL_NAME']}")

except Exception as e:
    app.logger.error(f"Failed to initialize Gemini model: {e}")
    model = None # Set model to None if initialization fails

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    image_files = []
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            if allowed_file(filename):
                image_files.append(filename)
    return render_template('index.html', image_files=image_files)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            try:
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                flash('Image successfully uploaded')
                return redirect(url_for('index'))
            except Exception as e:
                flash(f'Error uploading file: {e}')
                return redirect(request.url)
        else:
            flash('Allowed image types are png, jpg, jpeg, gif')
            return redirect(request.url)
    return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/chat_with_llm', methods=['POST'])
def chat_with_llm():
    if model is None:
        return jsonify({'error': 'Gemini model not initialized. Check server logs.'}), 500

    data = request.json
    user_query = data.get('query')
    image_data_b64 = data.get('image')

    if not user_query or not image_data_b64:
        return jsonify({'error': 'Missing query or image data'}), 400

    try:
        # Decode base64 image data and prepare for Gemini
        # Gemini expects raw bytes or a specific Image object for multimodal input
        if image_data_b64.startswith('data:image/'):
            image_data_b64 = image_data_b64.split(',')[1]

        image_bytes = base64.b64decode(image_data_b64)

        # Gemini 1.5 Flash (and other Gemini models) typically expect a list of "parts"
        # Each part can be text or an image.
        contents = [
            {"text": user_query},
            {"inline_data": {"mime_type": "image/jpeg", "data": image_data_b64}}
            # If using Vertex AI's `vertexai.preview.generative_models` (which you should if on GCP):
            # Image.from_bytes(image_bytes, mime_type="image/jpeg"), # You can use this if you import `Image` from vertexai.preview.generative_models
        ]
        
        # If you were using the new `vertexai.preview.generative_models`
        # contents = [
        #    Part.from_text(user_query),
        #    Part.from_data(data=image_bytes, mime_type="image/jpeg")
        # ]

        app.logger.info(f"Sending request to Gemini model: {app.config['GEMINI_MODEL_NAME']}")

        # Use the generate_content method
        response = model.generate_content(contents)

        # Extract the text from the response
        llm_response_content = response.text # Gemini's response object has a .text attribute

        return jsonify({'response': llm_response_content})

    except Exception as e:
        app.logger.error(f"Error calling Gemini API: {e}")
        # More specific error handling could be added for different API errors
        return jsonify({'error': f'Failed to get response from Gemini: {e}'}), 500

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
