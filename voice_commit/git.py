import subprocess
from typing import Optional

def get_staged_diff() -> str:
    """Get the git diff of staged files."""
    try:
        result = subprocess.run(
            ["git", "diff", "--staged"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError:
        return ""

def has_staged_changes() -> bool:
    """Check if there are staged changes."""
    return bool(get_staged_diff().strip())

def make_commit(message: str) -> bool:
    """Execute git commit with the given message."""
    try:
        subprocess.run(
            ["git", "commit", "-m", message],
            check=True
        )
        return True
    except subprocess.CalledProcessError:
        return False
