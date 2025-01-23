import requests
import os
from dotenv import load_dotenv
from flask import Flask, request, render_template

# Load environment variables from .env file
load_dotenv()

# Get the AIML API key securely
api_key = os.getenv("AIML_API_KEY")

app = Flask(__name__)

# Updated function to generate horoscope using AIML API
def generate_horoscope(data):
    url = "https://api.aimlapi.com/generateHoroscope"  # Check if this URL is correct
    headers = {
        "Authorization": f"Bearer {api_key}",  # Use Bearer token for authorization
        "Content-Type": "application/json"  # Ensure the server knows the body is JSON
    }

    # Prepare the data to be sent as a JSON payload
    payload = {
        "name": data['name'],
        "dob": data['dob'],
        "time": data['time'],
        "place": data['place'],
        "mood": data['mood'],
        "current_location": data['current_location'],
        "focus_area": data['focus_area'],
        "detail_level": data['detail_level'],
        "gender": data['gender'],
        "interests": data['interests'],
        "special_events": data['special_events']
    }

    try:
        # Make the request to the AIML API using POST method
        response = requests.post(url, json=payload, headers=headers)
        
        # Check the response status and content
        if response.status_code == 200:
            return response.json().get("horoscope", "No horoscope found.")
        else:
            # Detailed error response
            return f"Error generating horoscope: {response.status_code} - {response.text}"

    except Exception as e:
        return f"Error generating horoscope: {e}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-horoscope', methods=['POST'])
def get_horoscope():
    user_data = {
        "dob": request.form['dob'],
        "time": request.form.get('time'),
        "place": request.form.get('place'),
        "mood": request.form['mood'],
        "current_location": request.form.get('current_location'),
        "focus_area": request.form['focus_area'],
        "detail_level": request.form['detail_level'],
        "name": request.form['name'],
        "gender": request.form.get('gender'),
        "interests": request.form.get('interests'),
        "special_events": request.form.get('special_events'),
    }
    
    horoscope = generate_horoscope(user_data)
    return render_template('result.html', horoscope=horoscope)

if __name__ == '__main__':
    app.run(debug=True)
