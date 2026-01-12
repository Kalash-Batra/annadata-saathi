<<<<<<< HEAD
## Annadata Saathi – AI Agricultural Assistant

Annadata Saathi is a simple and farmer-friendly AI-based web application created to help Indian farmers with day-to-day agricultural decisions.
The goal of this project is to make modern agricultural guidance easily accessible, even for users with limited technical knowledge.

This project was built as part of an academic / hackathon initiative with a strong focus on simplicity, usefulness, and privacy.

# About the Project

Annadata Saathi acts as a digital assistant for farmers.
It provides guidance related to crops, diseases, weather planning, market timing, and government schemes in multiple Indian languages.

Farmers can interact with the system without creating any account or sharing personal data.

# Main Features
1. Text-Based Crop Advisory

Farmers can explain their crop problems in simple language.
The system analyzes the issue and provides easy-to-understand, practical suggestions that farmers can apply in real life.

2. Image-Based Crop Analysis

Farmers can upload photos of crop leaves or plants.
The application analyzes the image and suggests possible issues such as diseases, nutrient deficiency, or pest problems, along with basic care tips.

3. Weather & Market Planning

This section helps farmers with:

Seasonal planning

Irrigation timing

Harvest decisions

Market selling guidance

The advice is general in nature and meant to support better planning.

4. Government Scheme Advisor

Farmers can discover relevant government schemes based on:

State

Crop type

The system explains schemes in simple language, including benefits and eligibility details.

5. Multilingual Support

The interface supports multiple Indian languages to ensure accessibility.

Supported languages:

Hindi

Marathi

Tamil

Telugu

Punjabi

Bengali

English

6. Responsible AI & Disclaimer

All advisory responses include a disclaimer encouraging farmers to verify information with:

Local agricultural officers

Krishi Vigyan Kendras

Official government sources

This helps maintain transparency and trust.

# Technology Used

Frontend: HTML, CSS, JavaScript

Backend: Python (Flask)

Database: SQLite

AI Model: OpenAI GPT-4o-mini

Image Processing: Pillow

API Handling: Flask-RESTful

# Project Structure
annadata_saathi/
├── app.py              # Main Flask application
├── ai_engine.py        # AI logic and prompts
├── requirements.txt    # Dependencies
├── .env.example        # Environment variables sample
├── database/
│   └── init_db.py      # Database setup
├── templates/
│   └── index.html      # Frontend UI
└── static/
    ├── css/style.css
    └── js/main.js

# How to Run the Project
# Requirements

Python 3.8 or above

pip

OpenAI API key

# Setup Steps

Create a virtual environment

python -m venv venv


# Activate it

venv\Scripts\activate


# Install dependencies

pip install -r requirements.txt


# Create a .env file

OPENAI_API_KEY=your_openai_api_key_here
FLASK_ENV=development
FLASK_DEBUG=True


# Initialize database

python database/init_db.py


# Run the app

python app.py


# Open browser and visit:
http://localhost:5000

# Privacy & Security

No user login required

No personal data stored

No tracking

Stateless API requests

This project follows a privacy-first approach.

# Future Scope

Possible improvements include:

Real-time weather integration

Live mandi prices

WhatsApp / SMS advisory

Offline support

Farmer profiles

IoT and sensor integration

 # License

This project is developed for educational and demonstration purposes.
=======
# annadata-saathi
Annadata Saathi is a multilingual AI-powered web application that helps Indian farmers with crop advisory, weather and market planning, and government scheme awareness—without login or data storage.
>>>>>>> a483a506532825b60ada7b6f8d9b763d2922819d
