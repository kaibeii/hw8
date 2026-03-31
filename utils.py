"""
Utility functions for the quiz application.
Includes input validation, answer normalization, and question selection.
"""

import random
import json
import os


def load_questions():
    """
    Load questions from questions.json and validate structure.
    Raises an error if the file is missing or invalid.
    """
    if not os.path.exists("questions.json"):
        print("Error: The question bank file 'questions.json' could not be found.")
        exit(1)
    
    try:
        with open("questions.json", "r") as f:
            data = json.load(f)
        questions = data.get("questions", [])
        
        # Validate question structure
        _validate_questions(questions)
        return questions
    except json.JSONDecodeError:
        print("Error: The file 'questions.json' is unreadable and must be fixed.")
        exit(1)
    except ValueError as e:
        print(f"Error: Invalid question structure - {e}")
        exit(1)
    except Exception as e:
        print(f"Error loading questions: {e}")
        exit(1)


def _validate_questions(questions):
    """
    Validate that all questions have required fields based on their type.
    Raises ValueError if validation fails.
    """
    required_fields = {"question", "type", "answer"}
    type_specific_fields = {
        "multiple_choice": {"options"},
        "true_false": set(),
        "short_answer": set()
    }
    
    for idx, q in enumerate(questions):
        if not isinstance(q, dict):
            raise ValueError(f"Question {idx}: must be a dictionary")
        
        # Check required fields
        missing = required_fields - set(q.keys())
        if missing:
            raise ValueError(f"Question {idx}: missing fields {missing}")
        
        # Check question type is valid
        q_type = q.get("type")
        if q_type not in type_specific_fields:
            raise ValueError(f"Question {idx}: invalid type '{q_type}'")
        
        # Check type-specific fields
        if q_type == "multiple_choice":
            if "options" not in q:
                raise ValueError(f"Question {idx}: multiple_choice missing 'options' field")
            if not isinstance(q["options"], list) or len(q["options"]) < 2:
                raise ValueError(f"Question {idx}: 'options' must be a list with at least 2 items")
            if q["answer"] not in q["options"]:
                raise ValueError(f"Question {idx}: answer '{q['answer']}' not in options")


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
    Select random questions without repetition, preferring liked questions and avoiding disliked ones.
    
    Args:
        questions: List of all available questions
        num_questions: Number of questions to select
        user_feedback: Dictionary of question_index -> 'like'/'dislike'/'neutral'
    
    Returns:
        Tuple of (List of selected questions, actual number selected)
    """
    # Build weighted list
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
    
    # Cap to available questions (should be handled by caller, but safety check)
    num_questions = min(num_questions, len(available))
    
    # Select questions using weighted random sampling without replacement
    selected = _weighted_sample_without_replacement(available, weights, num_questions)
    
    return selected, num_questions


def _weighted_sample_without_replacement(population, weights, k):
    """
    Select k items from population without replacement, using weights.
    Items with higher weights are more likely to be selected, but no item appears twice.
    """
    if k > len(population):
        k = len(population)
    
    selected = []
    remaining_indices = list(range(len(population)))
    remaining_weights = list(weights)
    
    for _ in range(k):
        # Select one index based on weights from remaining items
        chosen_position = random.choices(range(len(remaining_indices)), weights=remaining_weights, k=1)[0]
        # Get the actual population item and add to selected
        selected.append(population[remaining_indices[chosen_position]])
        # Remove from remaining pool
        remaining_indices.pop(chosen_position)
        remaining_weights.pop(chosen_position)
    
    return selected


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
