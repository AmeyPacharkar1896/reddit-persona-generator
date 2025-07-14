# main.py
import argparse
import json
import os
import re
from scraper import get_reddit_data
from persona_generator import generate_persona

def sanitize_filename(username: str) -> str:
    """Removes invalid characters from a username to create a valid filename."""
    if username.startswith('u/'):
        username = username[2:]
    return re.sub(r'[\\/*?:"<>|]', "", username)

def format_json_to_text(data: dict) -> str:
    """
    Converts the JSON persona data into a well-formatted, human-readable text file.
    This function is now robust enough to handle different list item types.
    """
    lines = []
    
    def get_citation_str(citations: list) -> str:
        """Helper function to format a list of citations into a string."""
        if not citations:
            return ""
        return f" [Citations: {', '.join(map(str, citations))}]"

    for key, value in data.items():
        # --- FIX: Added a check to skip the top-level "citations" key if it exists ---
        if key == "citations" and isinstance(value, list):
            continue

        section_title = key.replace('_', ' ').title()
        lines.append(f"**{section_title}**\n")
        
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                if isinstance(sub_value, dict): # For nested dicts like in the first version
                    val_str = sub_value.get('value', 'N/A')
                    citations = sub_value.get('citations', [])
                    lines.append(f"*   **{sub_key.replace('_', ' ').title()}:** {val_str}{get_citation_str(citations)}")
                else: # For simple key-value pairs in a dict
                    lines.append(f"*   **{sub_key.replace('_', ' ').title()}:** {sub_value}")
        elif isinstance(value, list):
            for item in value:
                # --- THIS IS THE CORE OF THE FIX ---
                if isinstance(item, dict):
                    # Handles the case where a list item is a dictionary with citations
                    item_text = next((str(v) for k, v in item.items() if k != 'citations'), 'N/A')
                    citations = item.get('citations', [])
                    lines.append(f"*   {item_text}{get_citation_str(citations)}")
                elif isinstance(item, str):
                    # Handles the case where a list item is just a string
                    lines.append(f"*   {item}")
                # --- END FIX ---
        else:
            lines.append(str(value))
        lines.append("")
        
    return "\n".join(lines)


def main():
    """Main function to orchestrate the persona generation process."""
    parser = argparse.ArgumentParser(
        description="Generate a Reddit user persona from their profile URL.",
        epilog="Example: python main.py --url https://www.reddit.com/user/kojied/"
    )
    parser.add_argument("--url", required=True, help="The full URL of the Reddit user's profile.")
    args = parser.parse_args()

    match = re.search(r"user/([^/]+)", args.url)
    if not match:
        print("Error: Invalid Reddit user URL format.")
        return
    
    username = match.group(1)
    
    reddit_data = get_reddit_data(username)
    if not reddit_data:
        print(f"No data found for user '{username}' or user does not exist. Exiting.")
        return

    persona_json_str = generate_persona(username, reddit_data)

    sanitized_user = sanitize_filename(username)
    output_path = os.path.join("personas", sanitized_user)
    os.makedirs(output_path, exist_ok=True)

    json_filename = os.path.join(output_path, f"{sanitized_user}_persona.json")
    try:
        parsed_json = json.loads(persona_json_str)
        with open(json_filename, "w", encoding="utf-8") as f:
            json.dump(parsed_json, f, indent=4)
        print(f"✅ Success: JSON persona saved to {json_filename}")
    except json.JSONDecodeError:
        print("❌ Error: The LLM did not return valid JSON. Saving raw output for debugging.")
        error_filename = os.path.join(output_path, f"{sanitized_user}_error_raw_output.txt")
        with open(error_filename, "w", encoding="utf-8") as f:
            f.write(persona_json_str)
        return

    text_output = format_json_to_text(parsed_json)
    txt_filename = os.path.join(output_path, f"{sanitized_user}_persona.txt")
    with open(txt_filename, "w", encoding="utf-8") as f:
        f.write(text_output)
    print(f"✅ Success: Text persona saved to {txt_filename}")


if __name__ == "__main__":
    main()