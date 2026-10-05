import os
import json
from google import genai
from google.genai import types

def generate_intel():
    # The client automatically picks up the GEMINI_API_KEY from GitHub Actions secrets
    client = genai.Client()
    
    prompt = """
    You are an expert geopolitical intelligence analyst for the APAC region. 
    Generate a combined daily security briefing for the Asia-Pacific region.
    Return the response STRICTLY as a JSON array of incident objects. Do not include markdown formatting or backticks around the JSON.
    Each object must have exactly these keys:
    - "title": A short headline.
    - "location": The specific country or city in APAC (e.g., Sydney, Australia; Hong Kong; Mumbai, India).
    - "latitude": Float latitude of the location.
    - "longitude": Float longitude of the location.
    - "severity": "Critical", "High", or "Moderate".
    - "summary": A 1-2 sentence description of the threat.
    
    Generate 8-12 realistic, highly detailed hypothetical incidents spanning Australia, New Zealand, Hong Kong, India, Philippines, South China Sea, Taiwan, Myanmar, and Singapore.
    """
    
    # We use the new google-genai SDK to call the model
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.7,
        )
    )
    
    # Save the output to data.json
    try:
        data = json.loads(response.text)
        with open("data.json", "w") as f:
            json.dump({"incidents": data}, f, indent=4)
        print("Successfully generated data.json")
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        print("Raw response:", response.text)

if __name__ == "__main__":
    generate_intel()
