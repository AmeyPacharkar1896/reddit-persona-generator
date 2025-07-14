# Reddit User Persona Generator

This project is a submission for the AI/LLM Engineer Intern assignment at BeyondChats. It takes a Reddit user profile URL as input, scrapes the user's recent posts and comments, and uses a Large Language Model (Google Gemini) to generate a detailed user persona with citations.

## Features

-   **Reddit Scraper:** Uses PRAW (Python Reddit API Wrapper) to efficiently and safely collect user data.
-   **LLM-Powered Analysis:** Leverages Google's Gemini Pro to analyze text and infer persona characteristics.
-   **Detailed Personas:** Generates personas based on the example provided, including demographics, personality, motivations, and more.
-   **Source Citing:** Each piece of information in the persona is cited back to the specific post or comment it was derived from.
-   **Dynamic & Robust:** Handles different Reddit users and saves the output to a clean text file.

## Setup and Installation

**1. Clone the Repository:**
```bash
git clone https://github.com/your-username/reddit-persona-generator.git
cd reddit-persona-generator
```

**2. Create a Virtual Environment:**
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On MacOS/Linux
source venv/bin/activate
```

**3. Install Dependencies:**
```bash
pip install -r requirements.txt
```

**4. Configure API Keys:**
You will need API keys from both Reddit and Google.

-   Create a `.env` file in the root of the project.
-   Add your keys to the `.env` file in the following format:
```
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USER_AGENT=persona_scraper_by_u_your_username
GEMINI_API_KEY=your_gemini_api_key_here
```

## How to Run

Execute the main script from your terminal using the `--url` argument.

```bash
python main.py --url https://www.reddit.com/user/kojied/
```

Or for the other example:

```bash
python main.py --url https://www.reddit.com/user/Hungry-Move-6603/
```

The script will create a text file in the project directory named `[username]_persona.txt`.

## Project Structure
```
    .
    ├── .env          # (Not committed) Stores API keys
    ├── .gitignore    # Specifies files to ignore for Git
    ├── main.py       # Main script to run the application
    ├── persona_generator.py # Handles LLM interaction
    ├── README.md     # This file
    ├── requirements.txt # Project dependencies
    └── scraper.py    # Handles Reddit data scraping
```
