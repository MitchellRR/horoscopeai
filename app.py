import os
import openai
from dotenv import load_dotenv
from flask import Flask, request, render_template

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secure-secret-key'  # Set a secure secret key

# Function to generate horoscope using OpenAI API
def generate_horoscope(data):
    try:
        # Construct the prompt for the OpenAI API
        prompt = (
            f"Generate a personalized horoscope based on the following details:\n"
            f"Name: {data['name']}\n"
            f"Date of Birth: {data['dob']}\n"
            f"Time of Birth: {data.get('time', 'N/A')}\n"
            f"Place of Birth: {data.get('place', 'N/A')}\n"
            f"Current Mood: {data['mood']}\n"
            f"Focus Area: {data['focus_area']}\n"
            f"Level of Detail: {data['detail_level']}\n"
            f"Interests: {data.get('interests', 'N/A')}\n"
            f"Special Events: {data.get('special_events', 'N/A')}\n\n"
            f"Write this horoscope in a friendly and engaging tone."
        )

        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can also use "gpt-4"
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        # Extract and return the generated text
        return response['choices'][0]['message']['content'].strip()
    
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-horoscope', methods=['POST'])
def get_horoscope():
    try:
        user_data = {
            "name": request.form.get('name'),
            "dob": request.form.get('dob'),
            "time": request.form.get('time'),
            "place": request.form.get('place'),
            "mood": request.form.get('mood'),
            "focus_area": request.form.get('focus_area'),
            "detail_level": request.form.get('detail_level'),
            "interests": request.form.get('interests'),
            "special_events": request.form.get('special_events'),
        }

        # Basic validation
        if not user_data['name'] or not user_data['dob'] or not user_data['mood']:
            return render_template('result.html', horoscope="Error: Missing required fields.")

        horoscope = generate_horoscope(user_data)
        return render_template('result.html', horoscope=horoscope)

    except Exception as e:
        return render_template('result.html', horoscope=f"An error occurred: {e}")

if __name__ == '__main__':
    app.run(debug=True)
