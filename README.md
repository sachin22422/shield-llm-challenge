
# Shield: PII Anonymizer & Secure LLM Interface

This repository contains the solution for the LLM Engineer coding challenge. "Shield" is a full-stack application designed to detect and sanitize Personally Identifiable Information (PII) from user prompts *before* they are sent to a local Large Language Model for processing, ensuring user privacy and data security.

Demo Video: https://drive.google.com/file/d/1s2LL33F74dxLc8ZCR8guf75WIiYxK2H7/view?usp=drive_link
---

### Key Features

- **Robust PII Detection:** Utilizes the `spaCy` library to accurately identify entities like names, locations, organizations, and other sensitive data.
- **Secure Sanitization:** Redacts PII from the prompt by replacing it with generic labels (e.g., `[PERSON]`, `[GPE]`) before it ever reaches the LLM.
- **Local LLM Integration:** Communicates with any local model (e.g., `phi3`, `gemma:2b`) served via the **Ollama** REST API, keeping all data on the user's machine.
- **Interactive Frontend:** A clean, responsive UI built with vanilla HTML, CSS, and JavaScript allows for real-time interaction and clear visualization of results.
- **FastAPI Backend:** A lightweight and efficient Python backend orchestrates the entire workflow from PII detection to LLM communication.

---

### System Architecture

The application follows a simple, robust client-server architecture:
[User] --> [Frontend (HTML/JS)] --> [Backend API (FastAPI)] --+
|
+--> [spaCy (for NER)]
|
+--> [Ollama REST API (for LLM)]

1. The user enters text into the browser-based **Frontend**.
2. On submission, the text is sent to the **FastAPI Backend**.
3. The backend uses **spaCy** to detect and list all PII entities.
4. A sanitized version of the prompt is created.
5. The sanitized prompt is sent to the **Ollama API** to get a response from the local LLM.
6. The backend bundles the detected entities and the LLM response and sends it back to the frontend for display.

---

### Tech Stack

- **Backend:** Python, FastAPI
- **NER Library:** spaCy (`en_core_web_sm`)
- **LLM Service:** Ollama
- **Frontend:** HTML5, CSS3, JavaScript

---

### Setup and Usage

Follow these steps to get the application running on your local machine.

**1. Prerequisites:**
- Python 3.8+
- [Ollama](https://ollama.com/) installed and running.

**2. Clone the repository:**
```bash
# Replace the URL with your repository's URL
git clone https://github.com/sachin22422/shield-llm-challenge.git
cd shield-llm-challenge

# Install Python packages
pip install -r requirements.txt

# Download the spaCy model
python -m spacy download en_core_web_sm

#Make sure you have a model downloaded for Ollama to use. phi3 is recommended.
ollama pull phi3
ollama run phi3

#From the project's root directory, start the FastAPI server.
uvicorn main:app --reload
http://127.0.0.1:8000.

#Navigate to the project folder in your file explorer.
#Open the chatpage_2.html file directly in a modern web browser (like Chrome, Firefox, or Edge).
