# Local Quiz App Specification

## 1. Overview

This project is a fully local command-line quiz app for studying topics such as Python. The app loads questions from a JSON file, quizzes the user, gives a score at the end, and tracks score history over time for each user. The app also allows users to give feedback on whether they like or dislike questions, which influences what questions they get in future quizzes.

The app runs entirely locally and does not use a backend, GUI, HTML, CSS, or any external APIs.

---

## 2. App Flow

1. The user runs the program.
2. The app greets the user and gives them two options:
   - Log in
   - Create a new account
3. **Creating a new account:**
   - The app asks for a username.
   - The app checks whether that username already exists.
   - If it does not exist, the app asks for a password.
   - The password is hashed before being stored.
4. **Logging in:**
   - The app asks for username and password.
   - The app checks the entered password against the stored hashed password.
5. After logging in, the app shows the **main menu:**
   - Start quiz
   - View past performance
   - Exit
6. **Starting a quiz:**
   - The app asks how many questions the user wants.
   - The app asks whether they want all categories or a specific category.
   - The app loads questions from `questions.json`.
   - Questions are randomly selected while accounting for the chosen category and the user's past like/dislike feedback.
7. **During the quiz:**
   - One question is shown at a time.
   - Multiple choice questions show answer options.
   - True/false questions require the user to type `true` or `false`.
   - Short answer questions require a typed response.
8. **After each question:**
   - The app tells the user whether they were correct.
   - If incorrect, the app shows the correct answer.
   - The user is asked whether they liked the question, disliked it, or feel neutral about it.
9. **After all questions are answered**, the app shows:
   - Number correct
   - Total questions
   - Percentage score
10. The result is stored in the score history file for that user.
11. The user returns to the main menu to start another quiz, view past performance, or exit.

---

## 3. Question Bank Format

The question bank is stored in a human-readable JSON file named `questions.json`.

```json
{
  "questions": [
    {
      "question": "What keyword is used to define a function in Python?",
      "type": "multiple_choice",
      "options": ["func", "define", "def", "function"],
      "answer": "def",
      "category": "Python Basics"
    },
    {
      "question": "A list in Python is immutable.",
      "type": "true_false",
      "answer": "false",
      "category": "Data Structures"
    },
    {
      "question": "What built-in function returns the number of items in a list?",
      "type": "short_answer",
      "answer": "len",
      "category": "Python Basics"
    },
    {
      "question": "Which data type stores key-value pairs in Python?",
      "type": "multiple_choice",
      "options": ["tuple", "dictionary", "set", "string"],
      "answer": "dictionary",
      "category": "Data Structures"
    },
    {
      "question": "The expression 3 == 3.0 evaluates to True in Python.",
      "type": "true_false",
      "answer": "true",
      "category": "Operators"
    }
  ]
}
```

---

## 4. File Structure

```
HW8/
│
├── main.py
├── auth.py
├── quiz.py
├── storage.py
├── utils.py
├── questions.json
├── users.dat
├── scores.dat
└── SPEC.md
```

### File Descriptions

| File | Purpose |
|---|---|
| `main.py` | Runs the overall program, including the startup screen, main menu, and navigation between login, quiz, and score history. |
| `auth.py` | Handles account creation and login. Checks usernames, hashes passwords, and verifies passwords during login. |
| `quiz.py` | Runs the quiz itself. Selects questions, shows them to the user, checks answers, collects like/dislike feedback, and calculates the final score. |
| `storage.py` | Handles saving and loading data from files, including user login data and score history. |
| `utils.py` | Contains helper functions such as input validation, answer normalization, and random question selection. |
| `questions.json` | Stores the question bank in a human-readable format so it can be easily edited for other subjects. |
| `users.dat` | Stores usernames and hashed passwords in a non-human-readable format. |
| `scores.dat` | Stores score history, user performance statistics, and question feedback in a non-human-readable format. |

---

## 5. Error Handling

| Error | Behavior |
|---|---|
| Missing `questions.json` | Print an error message explaining that the question bank file could not be found. |
| Invalid JSON in `questions.json` | Print an error saying the file is unreadable and must be fixed. |
| Duplicate username | Tell the user the username is already taken and ask for a different one. |
| Incorrect password | Show an error and allow the user to try again. |
| Too many questions requested | Either use all available questions in the chosen category, or prompt the user to choose a smaller number. |

---

## 6. Required Features

- A local login system that prompts users for a username and password (or allows them to create a new account). Passwords must not be stored in plain text.
- A score history file that tracks performance and other useful statistics over time per user. This file should not be human-readable — someone viewing it may discover usernames, but not passwords or scores.
- Users can provide like/dislike feedback on questions, which influences future question selection.
- Questions are stored in a human-readable `questions.json` file so the app can be adapted for any subject by swapping the question bank.

> **Note:** No backend, HTML, CSS, graphical interface, or external APIs are required. Everything runs locally.

---

## 7. Category-Based Filtering (also a required feature)

When starting a quiz, the user can choose:

- **All categories**, or
- **One specific category**, such as:
  - Python Basics
  - Data Structures
  - Operators

The quiz will then only pull questions from the chosen category.

---

## 8. Acceptance Criteria

The implementation is complete when all of the following are true:

-  A user can create a new account with a username and password
-  Passwords are not stored in plain text
-  A returning user can log in with the correct password
-  The app loads questions from a human-readable `questions.json` file
-  The app supports multiple choice, true/false, and short answer questions
-  The app stores score history and feedback in a non-human-readable file
-  The user can give like/dislike/neutral feedback on questions, and that feedback affects future question selection
-  The user can choose a category and receive only questions from that category
-  Running the app with a missing or invalid question file shows a friendly error and exits cleanly