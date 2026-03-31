"""
Authentication module for user account creation and login.
Handles password hashing and verification.
"""

import hashlib
import os
import pickle
from storage import load_users, save_users


def hash_password(password):
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def username_exists(username):
    """Check if a username already exists."""
    users = load_users()
    return username in users


def create_account():
    """Guide the user through account creation."""
    print("\n=== Create New Account ===")
    
    while True:
        username = input("Choose a username: ").strip()
        
        if not username:
            print("Username cannot be empty. Please try again.")
            continue
            
        if username_exists(username):
            print(f"The username '{username}' is already taken. Please choose a different one.")
            continue
        
        break
    
    password = input("Choose a password: ").strip()
    
    # Store the account
    users = load_users()
    users[username] = hash_password(password)
    save_users(users)
    
    print(f"Account created successfully! Welcome, {username}!")
    return username


def login():
    """Guide the user through login."""
    print("\n=== Login ===")
    
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    
    users = load_users()
    
    if username not in users:
        print("Invalid username or password.")
        return None
    
    if users[username] != hash_password(password):
        print("Invalid username or password.")
        return None
    
    print(f"Welcome back, {username}!")
    return username


def startup_screen():
    """Show the startup screen and let user choose login or create account."""
    print("\n" + "="*40)
    print("   Welcome to the Quiz Application")
    print("="*40)
    
    while True:
        print("\nWhat would you like to do?")
        print("1. Log in")
        print("2. Create a new account")
        
        choice = input("Enter your choice (1 or 2): ").strip()
        
        if choice == "1":
            user = login()
            if user:
                return user
            print("Please try again.")
        elif choice == "2":
            return create_account()
        else:
            print("Invalid choice. Please enter 1 or 2.")
