# scraper.py
import os
import praw
from dotenv import load_dotenv

load_dotenv()

# --- FIX: Corrected the return type hint from list[str] to list[dict].
# This now accurately reflects that the function returns a list of dictionaries,
# each containing 'subreddit' and 'content' keys.
def get_reddit_data(username: str, limit: int = 50) -> list[dict]:
    """
    Scrapes a user's latest comments and posts from Reddit.

    Args:
        username: The Reddit username.
        limit: The number of items to fetch.

    Returns:
        A list of dictionaries, where each dict contains the content and subreddit.
        Example: [{'subreddit': 'python', 'content': 'Hello world!'}]
    """
    try:
        reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv("REDDIT_USER_AGENT"),
        )
        # --- REFINEMENT: Added a check for redditor existence. ---
        redditor = reddit.redditor(username)
        redditor.id # This will raise an exception if the user doesn't exist

        print(f"Fetching data for u/{username}...")
        
        content_list = []

        # Fetch comments
        for comment in redditor.comments.new(limit=limit):
            content_list.append({
                "subreddit": comment.subreddit.display_name,
                "content": comment.body
            })

        # Fetch posts
        for submission in redditor.submissions.new(limit=limit):
            # --- REFINEMENT: Ensure selftext is not empty for posts. ---
            if submission.selftext:
                content_list.append({
                    "subreddit": submission.subreddit.display_name,
                    "content": submission.selftext
                })
        
        print(f"Found {len(content_list)} items.")
        # --- REFINEMENT: Removed redundant list() call on an existing list. ---
        return content_list

    except Exception as e:
        print(f"Error fetching data for u/{username}: {e}")
        return []