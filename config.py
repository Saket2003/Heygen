"""
Configuration settings for the MediMate application.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Haygen API configuration
HAYGEN_API_KEY = os.getenv('HAYGEN_API_KEY')
HAYGEN_API_BASE_URL = os.getenv('HAYGEN_API_BASE_URL', 'https://api.haygen.ai/v1')

# Default avatar settings
DEFAULT_AVATAR = os.getenv('DEFAULT_AVATAR', 'doctor_female')
AVAILABLE_AVATARS = [
    'doctor_female',
    'doctor_male',
    'nurse_female',
    'nurse_male',
    'specialist_female',
    'specialist_male'
]  # These are placeholder names - replace with actual Haygen avatar options

# Medical domain keywords to identify medical queries
MEDICAL_KEYWORDS = [
    'health', 'medical', 'doctor', 'hospital', 'symptom', 'pain', 'treatment', 
    'medicine', 'disease', 'diagnosis', 'prescription', 'dose', 'therapy',
    'allergy', 'vaccination', 'surgery', 'emergency', 'vaccine', 'drug',
    'blood', 'heart', 'lung', 'kidney', 'liver', 'brain', 'stomach', 
    'headache', 'fever', 'cough', 'cold', 'flu', 'covid', 'virus',
    'bacteria', 'infection', 'inflammation', 'chronic', 'acute',
    'condition', 'disorder', 'syndrome', 'prevention', 'cure'
]

# Application settings
DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1', 't')
PORT = int(os.getenv('PORT', 5000))