import sys
import os
# Add the root directory to the Python path to allow imports from main
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import sanitize_filename

def test_sanitize_filename():
    assert sanitize_filename("user/name") == "username"
    assert sanitize_filename("user?name") == "username"
    assert sanitize_filename("a*b:c<d>e|f\\g") == "abcdefg"
    assert sanitize_filename("valid_user-123") == "valid_user-123"