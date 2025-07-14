# main.py
import argparse
import re
from scraper import get_reddit_data
from persona_generator import generate_persona

def sanitize_filename(username):
    """Removes invalid characters from a username to create a valid filename."""
    return re.sub(r'[\\/*?:"<>|]', "", username)

def main():
    parser = argparse.ArgumentParser(description="Generate a Reddit user persona.")
    parser.add_argument("--url", required=True, help="The full URL of the Reddit user's profile.")
    args = parser.parse_args()

    # Extract username from URL
    match = re.search(r"user/([^/]+)", args.url)
    if not match:
        print("Invalid Reddit user URL format. Please use 'https://www.reddit.com/user/username/'.")
        return
    
    username = match.group(1)
    
    # 1. Scrape Data
    reddit_data = get_reddit_data(username)

    if not reddit_data:
        print("No data found for this user. Exiting.")
        return

    # 2. Generate Persona
    persona = generate_persona(username, reddit_data)

    # 3. Save Output
    filename = f"{sanitize_filename(username)}_persona.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(persona)
    
    print(f"Persona successfully generated and saved to {filename}")

if __name__ == "__main__":
    main()