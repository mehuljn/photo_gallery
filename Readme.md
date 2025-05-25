# 📸 AI-Powered Flask Photo Gallery with Gemini 1.5 Flash

---

## Overview

This project showcases a dynamic Flask-based photo gallery enhanced with an interactive AI chat assistant. Leveraging **Google's Gemini 1.5 Flash API**, the AI can "see" and understand the content of your webpage by taking real-time snapshots. Users can upload images, browse their gallery, and then ask the AI questions about the displayed content, receiving intelligent, context-aware responses.

---

## Features

* **Photo Upload:** Easily upload images to your gallery.
* **Dynamic Gallery Display:** View all your uploaded photos in a responsive grid.
* **Interactive AI Chatbot:** A floating chat bubble provides direct access to an AI assistant.
* **Multimodal AI Interaction:** When you ask a question, the application captures a snapshot of the current webpage. This image, along with your text query, is sent to Google's Gemini 1.5 Flash.
* **Context-Aware Responses:** Gemini 1.5 Flash processes both the visual (snapshot) and textual input to provide highly relevant and intelligent answers.
* **Simple & Clean UI:** A straightforward interface focused on core functionality.

---

## Technologies Used

* **Backend:**
    * **Flask:** A lightweight Python web framework.
    * **Google Gemini 1.5 Flash API:** For powerful multimodal AI capabilities.
    * **Python:** The core programming language.
* **Frontend:**
    * **HTML/CSS:** For structuring and styling the web pages.
    * **JavaScript:** For dynamic interactions and API calls.
    * **`html2canvas`:** A JavaScript library used to take screenshots of the DOM.

---

## Getting Started

Follow these steps to get your AI-powered photo gallery up and running locally.

### Prerequisites

* **Python 3.8+** installed.
* An **API Key from Google AI Studio**:
    1.  Go to [Google AI Studio](https://aistudio.google.com/app/apikey).
    2.  Create a new API key.
    3.  **Important:** Keep this API key secure. You'll set it as an environment variable.

### 1. Clone the Repository

```bash
git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
cd YOUR_REPO_NAME
