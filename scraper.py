# scraper.py
import os
import praw
from dotenv import load_dotenv

load_dotenv()

def get_reddit_data(username: str, limit: int = 50) -> list[str]:
    """
    Scrapes a user's latest comments and posts from Reddit.

    Args:
        username: The Reddit username.
        limit: The number of items to fetch.

    Returns:
        A list of strings, where each string is the text of a comment or post.
    """
    try:
        reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv("REDDIT_USER_AGENT"),
        )
        redditor = reddit.redditor(username)
        
        print(f"Fetching data for u/{username}...")
        
        # Using a set to avoid duplicate content if a user comments on their own post
        content = set()

        # Fetch comments
        for comment in redditor.comments.new(limit=limit):
            content.add(comment.body)

        # Fetch posts
        for submission in redditor.submissions.new(limit=limit):
            content.add(submission.selftext)
        
        print(f"Found {len(content)} unique items.")
        return list(content)

    except Exception as e:
        print(f"Error fetching data for u/{username}: {e}")
        return []