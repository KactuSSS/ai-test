import os
import json
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return OpenAI(api_key=api_key)
    return None

def generate_authority_asset(topic, data_points):
    """
    Generates an authority asset using OpenAI.
    """
    if not os.getenv("OPENAI_API_KEY"):
        # Fallback to mock for testing without key
        return {
            "title": f"Industrial Report: The Future of {topic.title()} (DEMO)",
            "sections": [
                {"title": "Introduction", "content": f"The landscape of {topic} is evolving rapidly..."},
                {"title": "Key Data Points", "content": f"We identified: {data_points}"},
                {"title": "Expert Conclusion", "content": "Organizations must focus on authority."}
            ]
        }

    prompt = f"""
    Generate a high-authority industry report (SEO Authority Asset) for the following topic and data points.
    Topic: {topic}
    Key Data Points: {data_points}

    The response must be in JSON format with the following structure:
    {{
        "title": "A compelling, high-authority report title",
        "sections": [
            {{ "title": "Introduction", "content": "..." }},
            {{ "title": "Data Analysis & Methodology", "content": "..." }},
            {{ "title": "Strategic Insights", "content": "..." }},
            {{ "title": "Expert Conclusion", "content": "..." }}
        ]
    }}
    Ensure the content is deep, professional, and satisfies Google's E-E-A-T criteria.
    """

    client = get_openai_client()
    if not client:
         return {
            "title": f"Industrial Report: The Future of {topic.title()} (DEMO)",
            "sections": [
                {"title": "Introduction", "content": f"The landscape of {topic} is evolving rapidly..."},
                {"title": "Key Data Points", "content": f"We identified: {data_points}"},
                {"title": "Expert Conclusion", "content": "Organizations must focus on authority."}
            ]
        }

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are a specialized B2B content strategist."},
                      {"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    topic = data.get('topic')
    data_points = data.get('data_points')

    if not topic or not data_points:
        return jsonify({"error": "Missing topic or data points"}), 400

    asset = generate_authority_asset(topic, data_points)
    if "error" in asset:
        return jsonify(asset), 500
    return jsonify(asset)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
