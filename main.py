"""
Main entry point for the Quiz Application.
Handles the overall program flow, main menu, and navigation.
"""

from auth import startup_screen
from quiz import run_quiz, view_past_performance


def main_menu(username):
    """Display the main menu and handle user choices."""
    while True:
        print(f"\n{'='*40}")
        print(f"   Main Menu - {username}")
        print(f"{'='*40}")
        print("1. Start a quiz")
        print("2. View past performance")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1, 2, or 3): ").strip()
        
        if choice == "1":
            run_quiz(username)
        elif choice == "2":
            view_past_performance(username)
        elif choice == "3":
            print(f"\nThank you for using the Quiz App, {username}! Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


def main():
    """Main function to run the application."""
    # Show startup screen and authenticate user
    username = startup_screen()
    
    # Show main menu
    main_menu(username)


if __name__ == "__main__":
    main()
