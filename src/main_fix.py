import os
import sys
import pygame
import shutil

def fix_main_py():
    """Fix the typos in main.py"""
    print("Fixing typos in main.py...")
    
    # Get the absolute path to the game directory
    game_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    main_py_path = os.path.join(game_dir, "src", "main.py")
    
    # Create a backup of the original file
    backup_path = os.path.join(game_dir, "src", "main.py.bak")
    shutil.copy2(main_py_path, backup_path)
    print(f"Created backup of main.py at {backup_path}")
    
    # Read the main.py file
    with open(main_py_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix any typos in the file
    # The error message showed: title = telugu_font.render("తెలుగగు వంటకాలు - Telugu Cooking Game", Truue, BLACK)
    # Fix "తెలుగగు" to "తెలుగు" and "Truue" to "True"
    content = content.replace("తెలుగగు", "తెలుగు")
    content = content.replace("Truue", "True")
    
    # Write the corrected content back to the file
    with open(main_py_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed typos in {main_py_path}")
    print("Please run your game again with: python TeluguCookingGame/src/main.py")

if __name__ == "__main__":
    fix_main_py()
