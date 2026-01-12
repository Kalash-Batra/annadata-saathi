import os
import base64
import requests
import json


api_key = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"


LANGUAGE_PROMPTS = {
    'hindi': 'Please respond in simple Hindi (Hinglish is acceptable). Use easy words that farmers understand.',
    'marathi': 'Please respond in simple Marathi. Use easy words suitable for farmers.',
    'tamil': 'Please respond in simple Tamil. Use easy words suitable for farmers.',
    'telugu': 'Please respond in simple Telugu. Use easy words suitable for farmers.',
    'punjabi': 'Please respond in simple Punjabi. Use easy words suitable for farmers.',
    'bengali': 'Please respond in simple Bengali. Use easy words suitable for farmers.',
    'english': 'Please respond in simple English with easy-to-understand language.'
}

def get_crop_advisory(problem_text, crop_type, language='english'):
    """
    Get AI-powered crop advisory based on farmer's problem description
  
    """
    try:
        language_instruction = LANGUAGE_PROMPTS.get(language.lower(), LANGUAGE_PROMPTS['english'])
        
        prompt = f"""You are an agricultural expert assistant helping Indian farmers. {language_instruction}

A farmer is asking about their {crop_type} crop:

Problem: {problem_text}
IMPORTANT:
- Do NOT use markdown.
- Do NOT use ##, ###, **, bullet points, or hyphens.
- Write in plain simple text.
- Use numbered paragraphs like:
1)
2)
3)

Please provide:
1. What might be the likely cause
2. Simple, practical, low-cost solutions
3. Preventive measures for future

Remember: Keep your response simple, practical, and in {language} language. No technical jargon. Give solutions a farmer can implement with local resources.

IMPORTANT DISCLAIMER: This is AI-based advisory. The farmer should consult with local agricultural officers for confirmation before implementing."""

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are a helpful agricultural assistant for Indian farmers. Provide practical, simple advice."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 800
        }
        
        response = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        return data['choices'][0]['message']['content']
    except Exception as e:
        return f"Error getting advisory: {str(e)}"

def analyze_crop_image(image_file, language='english'):
    """
    Analyze crop image using vision capabilities
    
    """
    try:

        image_data = image_file.read()
        base64_image = base64.b64encode(image_data).decode('utf-8')
        
        language_instruction = LANGUAGE_PROMPTS.get(language.lower(), LANGUAGE_PROMPTS['english'])
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"""You are an agricultural expert analyzing crop images. {language_instruction}
IMPORTANT:
- Do NOT use markdown.
- Do NOT use ##, ###, **, bullet points, or hyphens.
- Write in plain simple text.
- Use numbered paragraphs like:
1)
2)
3)
Please analyze this crop/leaf image and provide:
1. What you observe (color, texture, any visible damage or stress)
2. Possible diseases, nutrient deficiencies, or stress factors (if any)
3. Preventive and care measures
4. When to seek expert help

IMPORTANT: Always mention that this is an AI estimation and the farmer should verify with local agricultural officers.

Respond in {language} language in a simple, farmer-friendly way."""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 800
        }
        
        response = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        
        data = response.json()
        return data['choices'][0]['message']['content']
    except Exception as e:
        return f"Error analyzing image: {str(e)}"

def get_planning_advisory(crop_type, planning_type, language='english'):
    """
    Get weather/market planning advisory
  
    """
    try:
        language_instruction = LANGUAGE_PROMPTS.get(language.lower(), LANGUAGE_PROMPTS['english'])
        
        if planning_type == 'weather':
            prompt = f"""You are an agricultural expert. {language_instruction}
  IMPORTANT:
- Do NOT use markdown.
- Do NOT use ##, ###, **, bullet points, or hyphens.
- Write in plain simple text.
- Use numbered paragraphs like:
1)
2)
3)
Provide seasonal planning advice for {crop_type} considering typical weather patterns:

1. Best planting season
2. Irrigation needs based on monsoon patterns
3. Frost/extreme weather risks
4. Harvest timing
5. Storage and post-harvest care

Give practical advice for Indian farmers in {language}. Include general seasonal patterns.

DISCLAIMER: This is general advisory. Check local weather forecasts and agricultural department recommendations."""

        else:
            prompt = f"""You are an agricultural expert. {language_instruction}

Provide market planning guidance for {crop_type} farmers:

1. Best time to sell in Indian market
2. Common market cycles and demand patterns
3. How to get better prices
4. Direct-to-consumer options
5. Value addition opportunities

Give practical, simple advice in {language}. Focus on typical market patterns.

DISCLAIMER: This is general market advisory. Check current prices and local market conditions."""

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are a helpful agricultural advisor for Indian farmers."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 800
        }
        
        response = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        
        data = response.json()
        return data['choices'][0]['message']['content']
    except Exception as e:
        return f"Error getting planning advisory: {str(e)}"

def get_scheme_explanation(scheme_name, scheme_data, language='english'):
    """
    Get AI-generated explanation of government schemes
  
    """
    try:
        language_instruction = LANGUAGE_PROMPTS.get(language.lower(), LANGUAGE_PROMPTS['english'])
        
        prompt = f"""You are explaining a government agriculture scheme to a farmer. {language_instruction}

Scheme: {scheme_name}
Description: {scheme_data.get('description', 'N/A')}
Benefits: {scheme_data.get('benefits', 'N/A')}
Eligibility: {scheme_data.get('eligibility', 'N/A')}
How to Apply: {scheme_data.get('how_to_apply', 'N/A')}
  IMPORTANT:
- Do NOT use markdown.
- Do NOT use ##, ###, **, bullet points, or hyphens.
- Write in plain simple text.
- Use numbered paragraphs like:
1)
2)
3)
Please explain in simple {language} language:
1. What this scheme is about
2. Who can benefit
3. What they will get
4. Simple steps to apply
5. Where to go for more help

Make it very simple and encouraging. No complex official language."""

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are a helpful agriculture advisor explaining government schemes to farmers."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 600
        }
        
        response = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        return data['choices'][0]['message']['content']
    except Exception as e:
        return f"Error explaining scheme: {str(e)}"

        