"""
Storage module for saving and loading user data and score history.
Uses pickle for non-human-readable storage.
"""

import os
import pickle
from datetime import datetime


USERS_FILE = "users.dat"
SCORES_FILE = "scores.dat"


def load_users():
    """Load users dictionary from users.dat. Returns empty dict if file doesn't exist."""
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "rb") as f:
                return pickle.load(f)
        except Exception as e:
            print(f"Error loading users file: {e}")
            return {}
    return {}


def save_users(users):
    """Save users dictionary to users.dat."""
    try:
        with open(USERS_FILE, "wb") as f:
            pickle.dump(users, f)
    except Exception as e:
        print(f"Error saving users file: {e}")


def load_scores():
    """Load scores dictionary from scores.dat. Returns empty dict if file doesn't exist."""
    if os.path.exists(SCORES_FILE):
        try:
            with open(SCORES_FILE, "rb") as f:
                return pickle.load(f)
        except Exception as e:
            print(f"Error loading scores file: {e}")
            return {}
    return {}


def save_scores(scores):
    """Save scores dictionary to scores.dat."""
    try:
        with open(SCORES_FILE, "wb") as f:
            pickle.dump(scores, f)
    except Exception as e:
        print(f"Error saving scores file: {e}")


def add_score(username, correct, total, category, feedback):
    """
    Add a score record for a user.
    
    Args:
        username: The user's username
        correct: Number of correct answers
        total: Total number of questions
        category: Category of the quiz
        feedback: Dictionary of question_index -> 'like'/'dislike'/'neutral'
    """
    scores = load_scores()
    
    if username not in scores:
        scores[username] = {
            "history": [],
            "feedback": {}
        }
    
    percentage = (correct / total * 100) if total > 0 else 0
    
    # Add to history
    scores[username]["history"].append({
        "timestamp": datetime.now().isoformat(),
        "correct": correct,
        "total": total,
        "percentage": percentage,
        "category": category
    })
    
    # Add feedback
    scores[username]["feedback"].update(feedback)
    
    save_scores(scores)


def get_score_history(username):
    """Get the score history for a user."""
    scores = load_scores()
    if username not in scores:
        return []
    return scores[username]["history"]


def get_question_feedback(username):
    """Get the like/dislike feedback for questions for a user."""
    scores = load_scores()
    if username not in scores:
        return {}
    return scores[username].get("feedback", {})
