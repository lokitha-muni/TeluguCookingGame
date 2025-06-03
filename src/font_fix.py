import os
import sys
import pygame
import requests
from io import BytesIO

def download_telugu_font():
    """Download the Noto Sans Telugu font and save it to the fonts directory"""
    print("Downloading Telugu font...")
    
    # Get the absolute path to the game directory
    game_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    font_dir = os.path.join(game_dir, "fonts")
    font_path = os.path.join(font_dir, "Noto_Sans_Telugu-Regular.ttf")
    
    # Create fonts directory if it doesn't exist
    if not os.path.exists(font_dir):
        os.makedirs(font_dir)
    
    # URL for the Noto Sans Telugu font - using Google Fonts API
    font_url = "https://fonts.google.com/download?family=Noto%20Sans%20Telugu"
    
    try:
        # Download the font
        response = requests.get(font_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Save the font file
        with open(font_path, 'wb') as f:
            f.write(response.content)
        
        print(f"Font downloaded successfully to {font_path}")
        
        # Check file size to ensure it's a valid font file
        file_size = os.path.getsize(font_path)
        if file_size < 10000:  # A valid font file should be at least 10KB
            print(f"Warning: Downloaded font file is suspiciously small ({file_size} bytes)")
            return False
            
        return True
    except Exception as e:
        print(f"Error downloading font: {e}")
        return False

def test_telugu_font():
    """Test if the Telugu font can be loaded and used to render text"""
    pygame.init()
    pygame.font.init()
    
    # Get the absolute path to the game directory
    game_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    font_path = os.path.join(game_dir, "fonts", "Noto_Sans_Telugu-Regular.ttf")
    
    try:
        # Try to load the font
        telugu_font = pygame.font.Font(font_path, 24)
        
        # Try to render some Telugu text
        text = telugu_font.render("తెలుగు వంటకాలు", True, (0, 0, 0))
        
        print("Font loaded and rendered successfully!")
        return True
    except Exception as e:
        print(f"Error loading or rendering font: {e}")
        return False

def main():
    """Main function to fix the Telugu font issue"""
    # Download the font
    if download_telugu_font():
        # Test the font
        if test_telugu_font():
            print("Font fix completed successfully!")
        else:
            print("Font downloaded but failed to load or render. Please check the font file.")
    else:
        print("Failed to download the font. Please check your internet connection.")

if __name__ == "__main__":
    main()
