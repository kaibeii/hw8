"""
Quiz module for running quizzes, selecting questions, and checking answers.
"""

import random
from utils import (
    load_questions, get_categories, filter_questions_by_category,
    select_random_questions, check_answer, normalize_answer, get_feedback
)
from storage import add_score, get_question_feedback, get_score_history


def show_categories(questions):
    """Show available categories and let user choose."""
    categories = get_categories(questions)
    
    print("\nAvailable categories:")
    print("0. All categories")
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")
    
    while True:
        try:
            choice = int(input("\nChoose a category (0 for all): ").strip())
            if choice == 0:
                return "All"
            elif 1 <= choice <= len(categories):
                return categories[choice - 1]
            else:
                print(f"Please enter a number between 0 and {len(categories)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_num_questions():
    """Ask user how many questions they want."""
    while True:
        try:
            num = int(input("How many questions do you want? ").strip())
            if num <= 0:
                print("Please enter a positive number.")
                continue
            return num
        except ValueError:
            print("Invalid input. Please enter a number.")


def display_question(question, question_num, total):
    """Display a question to the user."""
    print(f"\n{'='*50}")
    print(f"Question {question_num}/{total}")
    print(f"{'='*50}")
    print(f"Category: {question.get('category', 'N/A')}")
    print(f"\n{question['question']}\n")
    
    if question["type"] == "multiple_choice":
        options = question.get("options", [])
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        print()
    elif question["type"] == "true_false":
        print("(Answer with 'true' or 'false')\n")


def get_user_answer(question):
    """Get the user's answer to a question."""
    if question["type"] == "multiple_choice":
        options = question.get("options", [])
        while True:
            try:
                choice = int(input("Your answer (enter the number): ").strip())
                if 1 <= choice <= len(options):
                    return options[choice - 1]
                else:
                    print(f"Please enter a number between 1 and {len(options)}.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    else:
        return input("Your answer: ").strip()


def run_quiz(username):
    """Run a full quiz."""
    # Load questions
    questions = load_questions()
    
    # Ask user preferences
    num_questions = get_num_questions()
    selected_category = show_categories(questions)
    
    # Filter by category
    filtered_questions = filter_questions_by_category(questions, selected_category)
    
    if not filtered_questions:
        print(f"No questions found in category '{selected_category}'.")
        return
    
    # Get user feedback to weight question selection
    user_feedback = get_question_feedback(username)
    
    # Select questions
    quiz_questions, actual_num = select_random_questions(
        filtered_questions, num_questions, user_feedback
    )
    
    # Run the quiz
    correct_count = 0
    question_feedback = {}
    
    for i, question in enumerate(quiz_questions):
        display_question(question, i + 1, actual_num)  # i+1 for display (1-indexed)
        
        user_answer = get_user_answer(question)
        is_correct = check_answer(user_answer, question["answer"], question["type"])
        
        if is_correct:
            print("✓ Correct!")
            correct_count += 1
        else:
            print(f"✗ Incorrect. The correct answer is: {question['answer']}")
        
        # Get feedback (store with 0-indexed key to match utils.py retrieval)
        feedback = get_feedback()
        question_feedback[str(i)] = feedback
    
    # Show results
    percentage = (correct_count / actual_num * 100) if actual_num > 0 else 0
    
    print(f"\n{'='*50}")
    print("Quiz Complete!")
    print(f"{'='*50}")
    print(f"Score: {correct_count}/{actual_num}")
    print(f"Percentage: {percentage:.1f}%")
    print(f"{'='*50}\n")
    
    # Save score
    add_score(username, correct_count, actual_num, selected_category, question_feedback)


def view_past_performance(username):
    """Display user's past performance."""
    history = get_score_history(username)
    
    if not history:
        print("\nYou haven't taken any quizzes yet.")
        return
    
    print(f"\n{'='*50}")
    print(f"Past Performance for {username}")
    print(f"{'='*50}\n")
    
    total_correct = 0
    total_questions = 0
    
    for i, record in enumerate(history, 1):
        print(f"Quiz {i}:")
        print(f"  Date: {record['timestamp']}")
        print(f"  Category: {record['category']}")
        print(f"  Score: {record['correct']}/{record['total']}")
        print(f"  Percentage: {record['percentage']:.1f}%")
        print()
        
        total_correct += record['correct']
        total_questions += record['total']
    
    overall_percentage = (total_correct / total_questions * 100) if total_questions > 0 else 0
    
    print(f"{'='*50}")
    print(f"Overall Stats:")
    print(f"Total Score: {total_correct}/{total_questions}")
    print(f"Overall Percentage: {overall_percentage:.1f}%")
    print(f"Quizzes Taken: {len(history)}")
    print(f"{'='*50}\n")
