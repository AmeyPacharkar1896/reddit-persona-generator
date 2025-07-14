# persona_generator.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_persona(username: str, reddit_data: list[str]) -> str:
    """
    Generates a user persona using an LLM based on their Reddit data.

    Args:
        username: The Reddit username.
        reddit_data: A list of the user's comments and posts.

    Returns:
        A string containing the user persona.
    """
    if not reddit_data:
        return "Could not generate persona due to lack of data."

    # Format the data for the prompt, adding citation numbers
    formatted_data = ""
    for i, item in enumerate(reddit_data):
        formatted_data += f"--- COMMENT/POST {i+1} ---\n{item}\n\n"

    # The prompt is engineered to match the example persona's structure
    # and explicitly asks for citations.
    prompt = f"""
    **Objective:** Analyze the following Reddit comments and posts to create a detailed user persona for the user '{username}'. The persona should be based *only* on the provided text.

    **Persona Structure Required:**
    - **Name:** {username}
    - **Demographics:** Infer potential age range, location, occupation, and relationship status. Use phrases like 'Appears to be...', 'Likely...', or state if there's not enough information.
    - **Personality:** Use a simple spectrum (e.g., Introvert/Extrovert, Analytical/Creative). Briefly justify your choice.
    - **Motivations:** What drives this user? (e.g., Learning, career growth, helping others, specific hobbies).
    - **Frustrations/Pain Points:** What problems or annoyances do they express?
    - **Goals & Needs:** What are they trying to achieve or what do they need?
    - **Behavior & Habits:** Summarize their online behavior and mentioned lifestyle habits.
    - **Quote:** A representative quote that captures their essence.

    **CRITICAL INSTRUCTION: For every single point you make in the persona, you MUST cite the specific comment or post number it is based on. Use the format [Citation: X, Y, Z].** If a point is synthesized from multiple sources, cite them all.

    **Reddit Data to Analyze:**
    {formatted_data}

    **Output:** Now, generate the complete user persona based on the rules above.
    """

    print("Generating persona with LLM...")
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating persona: {e}"