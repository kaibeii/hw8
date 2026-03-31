# Code Review: Quiz Application

## Acceptance Criteria Review

1. **[PASS]** A user can create a new account with a username and password
   - File: [auth.py](auth.py#L23-L41)
   - `create_account()` successfully prompts for username, validates it doesn't already exist, prompts for password, and stores it.

2. **[WARN]** Passwords are not stored in plain text
   - File: [auth.py](auth.py#L13-L14)
   - Passwords are hashed using SHA-256, which is good. **However**, no salt is used. This makes passwords vulnerable to rainbow table attacks. Recommendation: Use `bcrypt` or add random salt per password.

3. **[PASS]** A returning user can log in with the correct password
   - File: [auth.py](auth.py#L43-L55)
   - `login()` correctly verifies the password by comparing the hash of the entered password with the stored hash.

4. **[PASS]** The app loads questions from a human-readable `questions.json` file
   - File: [utils.py](utils.py#L9-L23)
   - `load_questions()` successfully loads and parses JSON with proper error handling.

5. **[PASS]** The app supports multiple choice, true/false, and short answer questions
   - Multiple choice: [quiz.py](quiz.py#L45-L52) and [utils.py](utils.py#L95-L98)
   - True/false: [quiz.py](quiz.py#L53-L54) and [utils.py](utils.py#L89-L93)
   - Short answer: [utils.py](utils.py#L94)
   - All three types are properly supported with normalization and answer checking.

6. **[PASS]** The app stores score history and feedback in a non-human-readable file
   - File: [storage.py](storage.py#L1-L99)
   - Uses `pickle` module to serialize data to `.dat` files (users.dat, scores.dat).
   - Scores, timestamps, and feedback are all stored.

7. **[FAIL]** The user can give like/dislike/neutral feedback on questions, and that feedback affects future question selection
   - **Critical Bug Found:**
   - File: [quiz.py](quiz.py#L110-L124) stores feedback with **1-indexed keys**: `question_feedback[str(i)] = feedback` where `i` starts at 1
   - File: [utils.py](utils.py#L62-L71) retrieves feedback with **0-indexed keys**: `feedback_key = str(i)` where `i` starts at 0
   - **Problem:** Stored keys are "1", "2", "3" ... but lookup keys are "0", "1", "2" ...
   - **Result:** Feedback is applied to wrong questions. If user likes question at position 1, the feedback is stored as "1", but on next quiz it gets applied to the question at index 1 (which may be a different question).
   - **Recommendation:** Use stable question identifiers (add `id` field to questions or use question text as key).

8. **[PASS]** The user can choose a category and receive only questions from that category
   - File: [quiz.py](quiz.py#L8-L20) presents categories
   - File: [utils.py](utils.py#L34-L38) filters correctly
   - Categories are properly filtered and "All categories" option works.

9. **[PASS]** Running the app with a missing or invalid question file shows a friendly error and exits cleanly
   - File: [utils.py](utils.py#L12-L23)
   - Properly checks for file existence and JSON validity with informative error messages.

---

## Additional Issues Found

### 10. **[WARN]** Unused import in auth.py
   - File: [auth.py](auth.py#L16)
   - `pickle` is imported but never used in this file (probably leftover from development).
   - Minor: Remove line `import pickle`

### 11. **[WARN]** Unused import in auth.py
   - File: [auth.py](auth.py#L15)
   - `os` is imported but never used in this file.
   - Minor: Remove line `import os`

### 12. **[WARN]** No validation of question JSON structure
   - File: [quiz.py](quiz.py#L45-L54), [utils.py](utils.py#L89-L98)
   - Code assumes all required fields exist ('question', 'type', 'answer', 'options' for multiple choice).
   - If a question is malformed, the app could crash with `KeyError`. Example: If a multiple choice question is missing 'options' field, [quiz.py](quiz.py#L50) will crash.
   - Recommendation: Validate question structure in `load_questions()`.

### 13. **[WARN]** Inconsistent indexing in feedback system
   - File: [quiz.py](quiz.py#L110-L124)
   - Feedback is indexed starting at 1 (from `enumerate(quiz_questions, 1)`)
   - File: [utils.py](utils.py#L62)
   - Feedback is retrieved starting at 0 (from `enumerate(questions)`)
   - This off-by-one issue compounds the bug in Acceptance Criterion #7.

### 14. **[WARN]** Pickle security concern
   - File: [storage.py](storage.py)
   - `pickle` is known to be unsafe as it can execute arbitrary code during deserialization.
   - For a local-only app without untrusted pickle data, this is acceptable but not ideal.
   - Recommendation: Consider using `json` for storage (which is also human-readable to some degree) or add integrity checks.

### 15. **[INFO]** Race condition vulnerability (low risk for local app)
   - File: [auth.py](auth.py#L23-L41), [storage.py](storage.py#L23-L28)
   - If two instances of the app run simultaneously, both could create account with same username before either writes to disk.
   - For a single-user local app, not critical, but could be addressed with file locking.

### 16. **[WARN]** No password strength validation
   - File: [auth.py](auth.py#L38)
   - User can choose a password of any length, including empty or single character.
   - While not explicitly required by spec, this is a security consideration.
   - Recommendation: Add minimum password length requirement.

### 17. **[PASS]** Handling of too many requested questions
   - File: [utils.py](utils.py#L72-L75)
   - When user requests more questions than available, the code gracefully caps to available count. Acceptable per spec.

### 18. **[WARN]** Empty category handling
   - File: [quiz.py](quiz.py#L73-L76)
   - If a category has no questions, the app returns to main menu silently.
   - Minor: Message could be clearer about why quiz ended.

### 19. **[INFO]** String case sensitivity in answer checking
   - File: [utils.py](utils.py#L103-L114)
   - Multiple choice answers are normalized to lowercase before comparison.
   - This is good for user experience but assumes questions.json uses lowercase answers.

### 20. **[WARN]** Questions lack unique identifiers
   - Files: [questions.json](questions.json) (not provided, but referenced throughout)
   - The specification doesn't include an "id" field for questions.
   - This makes it impossible to reliably track feedback across quizzes when questions are reordered or when using "All categories".
   - Recommendation: Add `"id": "unique_identifier"` field to each question in questions.json.

---

## Summary

**Critical Issues:** 1
- Feedback mechanism broken (affects AC #7)

**Warnings:** 9
- Password hashing without salt (security)
- Unused imports (code quality)
- Missing JSON validation (robustness)
- Pickle security (safety)

**Passed:** 8 of 9 acceptance criteria (AC #7 has critical bug)

**Recommendation:** Fix the feedback indexing bug before deployment. This requires either:
1. Adding unique IDs to questions in questions.json
2. Using question text as the feedback key
3. Converting to 0-indexed feedback keys throughout
