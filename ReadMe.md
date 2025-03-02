# MediMate - Medical Voice Assistant

MediMate is a voice-enabled medical assistant that runs on your local machine. It uses the Haygen API to generate voice responses to medical queries and politely declines to answer non-medical questions.

## Features

- Voice and text input for medical questions
- AI-powered responses to medical queries only
- Customizable avatars for a personalized experience
- Modern, responsive user interface
- Runs locally on your machine

## Prerequisites

- Python 3.8 or higher
- Haygen API subscription (API key required)
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection (for Haygen API calls)

## Project Structure

```
MediMate/
├── app.py                  # Main Flask application
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── static/                 # Static assets
│   ├── css/
│   │   └── style.css       # CSS styling
│   ├── js/
│   │   ├── main.js         # Main JavaScript file
│   │   └── haygen.js       # Haygen API integration
│   └── img/                # Images for the application
│       └── logo.png        # MediMate logo (create your own)
└── templates/              # HTML templates
    └── index.html          # Main page
```

## Setup and Installation

### 1. Clone or Download the Project

Create a new directory for your project and place all the files in the structure shown above.

### 2. Create a Virtual Environment (Recommended)

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root directory with your Haygen API key:

```
HAYGEN_API_KEY=your_haygen_api_key_here
HAYGEN_API_BASE_URL=https://api.haygen.ai/v1  # Or the correct base URL for Haygen API
DEBUG=True
PORT=5000
```

### 5. Add a Logo Image

Create or obtain a logo image for your MediMate application and save it as `logo.png` in the `static/img/` directory.

### 6. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000` (or the port you specified in the `.env` file).

## How to Use

1. Open your web browser and navigate to `http://localhost:5000`
2. Choose an avatar from the dropdown menu
3. Type a medical question in the text box and press Enter or click the Send button, or
4. Click the microphone button and speak your medical question
5. The assistant will respond to medical queries and politely decline non-medical questions
6. Audio responses will play automatically if available

## Customizing the Application

### Adding More Avatars

1. Update the `AVAILABLE_AVATARS` list in `config.py` with your desired avatar options
2. Make sure the avatar IDs match the ones available in your Haygen API subscription

### Adjusting the Medical Query Detection

1. Modify the `MEDICAL_KEYWORDS` list in `config.py` to add or remove medical keywords
2. Update the training data in `app.py` to improve the classification model

### Styling

1. Modify the `style.css` file to customize the appearance of the application
2. Update the color variables at the top of the CSS file to change the color scheme

## Integrating with Haygen API

This application provides integration with the Haygen API for voice synthesis and avatar capabilities. The integration assumes the following API endpoints:

- `/speak` - For generating voice responses
- Avatar selection through the API request payload

If the actual Haygen API structure differs, you may need to update the `call_haygen_api` function in `app.py` and the `HaygenClient` class in `static/js/haygen.js` to match the actual API specification.

## Troubleshooting

- **API Key Issues**: Make sure your Haygen API key is correctly set in the `.env` file
- **Voice Recognition Not Working**: Ensure you're using a compatible browser and have allowed microphone access
- **Application Not Starting**: Check for errors in the terminal/console where you ran `python app.py`

## License

This project is for personal use only. Usage is subject to the terms of your Haygen API subscription.

## Disclaimer

MediMate is for informational purposes only. Always consult with a healthcare professional for medical advice.