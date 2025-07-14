# Reddit User Persona Generator

This project is a submission for the AI/LLM Engineer Intern assignment at BeyondChats. It is a robust Python tool that takes a Reddit user's profile URL, scrapes their recent activity, and leverages Google's Gemini LLM to generate a highly detailed and meticulously cited user persona.

The project goes beyond the minimum requirements by implementing professional software engineering practices, including structured data output, automated testing, and a modular, error-resilient codebase.

## Key Features

-   **Structured JSON & Text Output:** The tool first generates a machine-readable `.json` file containing the full, structured persona. It then uses this data to create a clean, human-readable `.txt` report, fulfilling the assignment's requirement while demonstrating professional data handling.
-   **Meticulous Per-Item Citations:** Through advanced prompt engineering, the LLM is guided to provide a source citation for **every single characteristic** in the persona, from top-level traits to individual items in a list, fully satisfying the most critical requirement.
-   **Organized File Management:** All generated output is automatically saved into a clean directory structure (`personas/[username]/`), preventing clutter and making the project scalable for analyzing multiple users.
-   **Automated Unit Testing:** The project includes a test suite using `pytest` to ensure the reliability and correctness of core utility functions, demonstrating a commitment to code quality and maintainability.
-   **Robust & Safe Scraping:** Uses PRAW, the official Python Reddit API Wrapper, to interact with the Reddit API safely and efficiently. The scraper is resilient to users not existing or having no public activity.
-   **Advanced LLM Prompt Engineering:** The prompt is carefully designed to control the LLM's output format, enforce strict rules, and produce consistent, high-quality JSON data.

## Setup and Installation

**1. Clone the Repository:**
```bash
git clone https://github.com/AmeyPacharkar1896/reddit-persona-generator.git
cd reddit-persona-generator
```


**2. Create and Activate a Virtual Environment:**
```bash
# Create the environment
python -m venv venv

# On Windows
venv\Scripts\activate

# On MacOS/Linux
source venv/bin/activate
```

**3. Install Dependencies:**
The `requirements.txt` file includes all necessary libraries, including `pytest` for testing.
```bash
pip install -r requirements.txt
```

**4. Configure API Keys:**
You will need API keys from both Reddit and Google.
-   Create a file named `.env` in the root of the project.
-   Add your keys to this file in the following format:
    ```
    REDDIT_CLIENT_ID=your_client_id_here
    REDDIT_CLIENT_SECRET=your_client_secret_here
    REDDIT_USER_AGENT=persona_scraper_by_u_your_username
    GEMINI_API_KEY=your_gemini_api_key_here
    ```
-   **Note:** The `.env` file is listed in `.gitignore` and will not be committed to your repository.

## How to Run

Execute the main script from your terminal using the `--url` argument.

**Example for user 'kojied':**
```bash
python main.py --url https://www.reddit.com/user/kojied/
```
**Example for user 'Hungry-Move-6603':**
```bash
python main.py --url https://www.reddit.com/user/Hungry-Move-6603/
```

The script will create a new directory for the user inside the `personas/` folder and save both `[username]_persona.json` and `[username]_persona.txt` files there.

## Code Quality & Testing

To ensure the reliability of utility functions, the project includes a unit test.

**To run the tests:**
1.  Make sure you have installed the dependencies from `requirements.txt`.
2.  From the project's root directory, run the `pytest` command:
    ```bash
    pytest
    ```
3.  You should see a confirmation that all tests have passed.

## Project Structure

The project is organized with a clean, modular structure that separates concerns.

```
.
├── .env                  # (Not committed) Stores API keys
├── .gitignore            # Specifies files to ignore for Git
├── main.py               # Main script to orchestrate the application
├── persona_generator.py  # Handles LLM interaction and prompt engineering
├── scraper.py            # Handles Reddit data scraping via PRAW
├── requirements.txt      # Project dependencies for pip
├── README.md             # This file
├── tests/                # Directory for unit tests
│   └── test_main.py
└── personas/             # (Not committed) Output directory for generated personas
    ├── kojied/
    │   ├── kojied_persona.json
    │   └── kojied_persona.txt
    └── ...
```