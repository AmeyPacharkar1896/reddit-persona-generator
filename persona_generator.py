# persona_generator.py
import os
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_persona(username: str, reddit_data: list[dict]) -> str:
    """
    Generates a user persona using an LLM based on their Reddit data.
    """
    if not reddit_data:
        return '{"error": "Could not generate persona due to lack of data."}'

    formatted_data = ""
    for i, item in enumerate(reddit_data):
        subreddit = item.get('subreddit', 'unknown')
        content = item.get('content', '')
        formatted_data += f"--- SOURCE {i+1} (from r/{subreddit}) ---\n{content}\n\n"

    # --- THIS PROMPT IS NOW MORE STRICT AND EXPLICIT ---
    prompt = f"""
    **Objective:** Analyze the following Reddit data to create a detailed user persona for '{username}'. Base the persona *only* on the provided text.

    **CRITICAL OUTPUT INSTRUCTIONS:**
    1.  Your final output MUST be a single, valid JSON object. Do not include any text or markdown outside of the JSON structure.
    2.  For **every single point, characteristic, or item**, you MUST cite the source number(s) it is based on in a "citations" array.

    **REQUIRED JSON STRUCTURE:**
    -   For lists (like `key_interests_and_communities`, `motivations`, `frustrations_pain_points`, `goals_and_needs`), **EACH item in the list MUST be a JSON object** containing the point itself and its "citations" array.
    -   For direct values (like `demographics`), the value should be an object containing the "value" and its "citations".

    **Example JSON Structure to Follow Meticulously:**
    {{
      "name": "{username}",
      "key_interests_and_communities": [
        {{ "interest": "iOS Development", "citations": [27, 55] }},
        {{ "interest": "Basketball", "citations": [7, 35, 45] }}
      ],
      "demographics": {{
        "age_range": {{ "value": "Likely 25-35", "citations": [12, 29, 10] }},
        "location": {{ "value": "New York City, USA", "citations": [6, 15] }}
      }},
      "personality": {{
          "spectrum": {{"value": "Analytical/Creative", "citations": [13, 56]}},
          "justification": {{"value": "The user shows analytical thinking in finance [13, 29] but also a creative side in art [56].", "citations": [13, 29, 56]}}
      }},
      "motivations": [
          {{ "motivation": "Learning about new tech", "citations": [10, 38] }},
          {{ "motivation": "Improving game strategy", "citations": [9, 44] }}
      ],
      "frustrations_pain_points": [
          {{ "frustration": "High cost of options", "citations": [13] }}
      ],
      "goals_and_needs": [
          {{ "goal": "To integrate Vision Pro into workflow", "citations": [38] }}
      ],
      "behavior_and_habits": [
          {{ "habit": "Frequently posts on tech subreddits", "citations": [27, 38] }}
      ],
      "quote": {{ "value": "A representative quote from the user.", "citations": [38] }}
    }}

    **Reddit Data to Analyze:**
    {formatted_data}

    **Output:**
    """

    print("Generating persona with LLM...")
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        cleaned_response = re.sub(r'^```json\s*|\s*```$', '', response.text.strip(), flags=re.MULTILINE)
        return cleaned_response
    except Exception as e:
        return f'{{"error": "An exception occurred: {str(e)}"}}'