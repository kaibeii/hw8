"""
Utility functions for the quiz application.
Includes input validation, answer normalization, and question selection.
"""

import random
import json
import os


def load_questions():
    """
    Load questions from questions.json.
    Raises an error if the file is missing or invalid.
    """
    if not os.path.exists("questions.json"):
        print("Error: The question bank file 'questions.json' could not be found.")
        exit(1)
    
    try:
        with open("questions.json", "r") as f:
            data = json.load(f)
        return data.get("questions", [])
    except json.JSONDecodeError:
        print("Error: The file 'questions.json' is unreadable and must be fixed.")
        exit(1)
    except Exception as e:
        print(f"Error loading questions: {e}")
        exit(1)


def get_categories(questions):
    """Get a list of unique categories from the questions."""
    categories = set()
    for q in questions:
        if "category" in q:
            categories.add(q["category"])
    return sorted(list(categories))


def filter_questions_by_category(questions, category):
    """Filter questions by category."""
    if category == "All":
        return questions
    return [q for q in questions if q.get("category") == category]


def select_random_questions(questions, num_questions, user_feedback):
    """
    Select random questions, preferring liked questions and avoiding disliked ones.
    
    Args:
        questions: List of all available questions
        num_questions: Number of questions to select
        user_feedback: Dictionary of question_index -> 'like'/'dislike'/'neutral'
    
    Returns:
        List of selected questions
    """
    # Adjust availability based on feedback
    available = []
    weights = []
    
    for i, q in enumerate(questions):
        feedback_key = str(i)
        feedback = user_feedback.get(feedback_key, "neutral")
        
        if feedback == "like":
            weights.append(2.0)  # Prefer liked questions
        elif feedback == "dislike":
            weights.append(0.1)  # Avoid disliked questions
        else:
            weights.append(1.0)  # Normal weight for neutral
        
        available.append(q)
    
    # Handle case where more questions are requested than available
    if num_questions > len(available):
        print(f"Only {len(available)} questions available in the chosen category.")
        num_questions = len(available)
    
    # Select questions using weighted random selection
    selected = random.choices(available, weights=weights, k=num_questions)
    
    return selected, num_questions


def normalize_answer(answer, question_type):
    """Normalize an answer based on the question type."""
    answer = answer.strip().lower()
    
    if question_type == "true_false":
        if answer in ["true", "t", "yes", "y", "1"]:
            return "true"
        elif answer in ["false", "f", "no", "n", "0"]:
            return "false"
        else:
            return None  # Invalid answer
    
    if question_type == "short_answer":
        return answer
    
    if question_type == "multiple_choice":
        return answer
    
    return answer


def check_answer(user_answer, correct_answer, question_type):
    """Check if the user's answer is correct."""
    normalized_answer = normalize_answer(user_answer, question_type)
    
    if normalized_answer is None and question_type == "true_false":
        return False
    
    if question_type == "short_answer":
        # For short answers, do case-insensitive comparison
        return normalized_answer == correct_answer.strip().lower()
    
    if question_type == "true_false":
        return normalized_answer == correct_answer.strip().lower()
    
    if question_type == "multiple_choice":
        # For multiple choice, just check string equality (case-insensitive)
        return normalized_answer == correct_answer.strip().lower()
    
    return False


def get_feedback():
    """Get user feedback on a question."""
    while True:
        response = input("Did you like this question? (like/dislike/neutral): ").strip().lower()
        if response in ["like", "dislike", "neutral"]:
            return response
        print("Please enter 'like', 'dislike', or 'neutral'.")
