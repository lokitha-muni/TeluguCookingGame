import pygame
import os

class Ingredient:
    def __init__(self, name, image_file):
        self.name = name
        # Get the absolute path to the game directory
        game_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.image_path = os.path.join(game_dir, "images", image_file)
        self.image = None
        self.load_image()
    
    def load_image(self):
        try:
            self.image = pygame.image.load(self.image_path)
            self.image = pygame.transform.scale(self.image, (64, 64))
            # No background color added - using original image
        except (pygame.error, FileNotFoundError) as e:
            print(f"Could not load image: {self.image_path}")
            print(f"Error: {e}")
            # Create a placeholder image
            self.image = pygame.Surface((64, 64))
            self.image.fill(self.get_color_for_ingredient())  # Use color based on ingredient
    
    def get_color_for_ingredient(self):
        """Return a color based on the ingredient name - only used for placeholder images"""
        colors = {
            "బియ్యం": (255, 255, 255),      # White for rice
            "పసుపు": (255, 200, 0),         # Yellow for turmeric
            "నిమ్మకాయ": (255, 255, 0),      # Yellow for lemon
            "కారం": (255, 0, 0),            # Red for chili
            "వేరుశెనగ": (210, 180, 140),    # Tan for peanuts
            "ఆవాలు": (50, 50, 50),          # Dark gray for mustard
            "కరివేపాకు": (0, 128, 0),        # Green for curry leaves
            "కందిపప్పు": (255, 200, 100),    # Light orange for dal
            "ఉల్లిపాయలు": (255, 228, 196),   # Bisque for onion
            "టమాటా": (255, 99, 71),         # Tomato red
            "కొత్తిమీర": (0, 255, 0),        # Green for coriander
            "పెరుగు": (245, 245, 245),      # Off-white for yogurt
            "ఉప్పు": (255, 255, 255),       # White for salt
            "కొబ్బరి": (240, 240, 240),     # Light gray for coconut
            "మిరియాలు": (50, 50, 50)        # Dark gray for black pepper
        }
        return colors.get(self.name, (200, 200, 200))  # Default gray
