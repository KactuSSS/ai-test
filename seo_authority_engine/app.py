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
    Generates a high-authority industry report using OpenAI.
    Focused on E-E-A-T: Experience, Expertise, Authoritativeness, and Trustworthiness.
    """
    if not os.getenv("OPENAI_API_KEY"):
        # Fallback to high-quality mock for testing
        return {
            "title": f"Strategic Analysis: The 2025 Evolution of {topic.title()}",
            "sections": [
                {
                    "title": "Executive Summary",
                    "content": f"The {topic} sector is undergoing a fundamental shift. Based on trends such as {data_points}, we see a move towards integrated authority models."
                },
                {
                    "title": "Methodology & Data Synthesis",
                    "content": f"Our analysis incorporates real-time indicators including: {data_points}. This methodology ensures a high degree of expert-level accuracy."
                },
                {
                    "title": "Strategic Recommendations",
                    "content": "1. Prioritize data transparency. 2. Implement authority-first content cycles. 3. Focus on trust-building via verifiable expertise."
                },
                {
                    "title": "Conclusion: The Authority Imperative",
                    "content": "To survive the next wave of search engine updates, organizations must transition from generic content to high-authority assets."
                }
            ]
        }

    prompt = f"""
    You are a Senior B2B Content Strategist and Industry Analyst specializing in E-E-A-T (Experience, Expertise, Authoritativeness, and Trustworthiness).

    Task: Generate a deep-dive, professional industry report (Whitepaper style).
    Topic: {topic}
    Core Data Points/Trends to Include: {data_points}

    Requirements:
    - Tone: Academic, professional, and authoritative.
    - Insight: Provide unique strategic perspectives that go beyond surface-level AI summaries.
    - Structure: Must be exactly 4-5 substantial sections.

    The response must be in JSON format with the following structure:
    {{
        "title": "A compelling, high-authority academic/industry report title",
        "sections": [
            {{
                "title": "Executive Summary",
                "content": "Deep analysis of the current state of the topic..."
            }},
            {{
                "title": "Market Dynamics & Data Synthesis",
                "content": "Deep dive into the provided data points and their implications..."
            }},
            {{
                "title": "Strategic Implications for Stakeholders",
                "content": "Actionable, expert-level advice based on the trends..."
            }},
            {{
                "title": "Future Outlook & Projections",
                "content": "Where the industry is heading in the next 12-24 months..."
            }},
            {{
                "title": "Concluding Synthesis",
                "content": "A final authoritative take on why this matters now."
            }}
        ]
    }}
    Ensure each 'content' block is at least 3-4 paragraphs of high-value text.
    """

    client = get_openai_client()
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are a world-class B2B analyst and industry researcher."},
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
