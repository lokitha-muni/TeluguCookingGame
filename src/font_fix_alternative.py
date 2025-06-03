import os
import sys
import pygame

def fix_font_issue():
    """Fix the Telugu font issue by using a system font instead"""
    print("Attempting to fix Telugu font issue using system fonts...")
    
    # Initialize pygame
    pygame.init()
    pygame.font.init()
    
    # Get the absolute path to the game directory
    game_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    main_py_path = os.path.join(game_dir, "src", "main.py")
    
    # Read the main.py file
    with open(main_py_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the font loading code with system font
    old_font_code = """try:
    font_path = os.path.join(game_dir, "fonts", "Noto_Sans_Telugu-Regular.ttf")
    telugu_font = pygame.font.Font(font_path, 24)
    small_telugu_font = pygame.font.Font(font_path, 18)
except:
    print("Telugu font not found. Using default font.")
    telugu_font = pygame.font.SysFont(None, 24)
    small_telugu_font = pygame.font.SysFont(None, 18)"""
    
    new_font_code = """# Use system font that supports Telugu or fallback to default
print("Using system font for Telugu text")
telugu_font = pygame.font.SysFont("Arial Unicode MS, Nirmala UI, Mangal, Latha", 24)
small_telugu_font = pygame.font.SysFont("Arial Unicode MS, Nirmala UI, Mangal, Latha", 18)"""
    
    # Replace the font code
    new_content = content.replace(old_font_code, new_font_code)
    
    # Write the modified content back to the file
    with open(main_py_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Modified {main_py_path} to use system fonts")
    print("Please run your game again with: python TeluguCookingGame/src/main.py")

if __name__ == "__main__":
    fix_font_issue()
