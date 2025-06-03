import pygame
import sys
import os
from game_state import GameState
from recipe import Recipe
from ingredient import Ingredient
from mini_games import ChoppingGame, MixingGame, ServingGame

# Initialize Pygame
pygame.init()
pygame.mixer.init()
pygame.font.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
BLUE = (100, 100, 200)

# Get the absolute path to the game directory
game_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Telugu font
# Use system font that supports Telugu or fallback to default
print("Using system font for Telugu text")
telugu_font = pygame.font.SysFont("Arial Unicode MS, Nirmala UI, Mangal, Latha", 24)
small_telugu_font = pygame.font.SysFont("Arial Unicode MS, Nirmala UI, Mangal, Latha", 18)

class TeluguCookingGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("తెలుగు వంటకాలు - Telugu Cooking Game")
        self.clock = pygame.time.Clock()
        self.game_state = GameState()
        
        # Get the absolute path to the game directory and print it for debugging
        print(f"Game directory: {game_dir}")
        print(f"Images directory should be: {os.path.join(game_dir, 'images')}")
        
        # Background images - initialize early
        self.background_images = {}
        self.current_background = "kitchen_background.png"
        self.load_background_images()
        
        # Create a default background in case loading fails
        self.default_bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.default_bg.fill((220, 220, 200))  # Light tan color
        
        # Load recipes
        self.recipes = [
            Recipe("పులిహోర", ["బియ్యం", "పసుపు", "నిమ్మకాయ", "కారం", "వేరుశెనగ", "ఆవాలు", "కరివేపాకు"], 
                  "బియ్యం ఉడికించి, నిమ్మకాయ రసం, పసుపు, కారం, వేరుశెనగ, ఆవాలు, కరివేపాకు కలపండి."),
            Recipe("పప్పు", ["కందిపప్పు", "పసుపు", "ఉల్లిపాయలు", "టమాటా", "కారం", "కొత్తిమీర"], 
                  "కందిపప్పు ఉడికించి, ఉల్లిపాయలు, టమాటా, పసుపు, కారం, కొత్తిమీర కలపండి."),
            Recipe("పెరుగు", ["పెరుగు", "ఉప్పు", "కారం", "కొత్తిమీర"], 
                  "పెరుగులో ఉప్పు, కారం, కొత్తిమీర కలపండి."),
            Recipe("కొబ్బరి పాయసం", ["బియ్యం", "కొబ్బరి", "పాలు", "పంచదార", "ఏలకులు"], 
                  "బియ్యం ఉడికించి, కొబ్బరి, పాలు, పంచదార, ఏలకులు కలపండి."),
            Recipe("మిరియాల రసం", ["మిరియాలు", "ఉల్లిపాయలు", "కొత్తిమీర", "ఉప్పు"], 
                  "మిరియాలు, ఉల్లిపాయలు, కొత్తిమీర, ఉప్పు కలిపి మరిగించండి.")
        ]
        
        # Load ingredients
        self.ingredients = [
            Ingredient("బియ్యం", "rice.png"),
            Ingredient("పసుపు", "turmeric.png"),
            Ingredient("నిమ్మకాయ", "lemon.png"),
            Ingredient("కారం", "chili.png"),
            Ingredient("వేరుశెనగ", "peanuts.png"),
            Ingredient("ఆవాలు", "mustard.png"),
            Ingredient("కరివేపాకు", "curry_leaves.png"),
            Ingredient("కందిపప్పు", "dal.png"),
            Ingredient("ఉల్లిపాయలు", "onion.png"),
            Ingredient("టమాటా", "tomato.png"),
            Ingredient("కొత్తిమీర", "coriander.png"),
            Ingredient("పెరుగు", "curd.png"),
            Ingredient("ఉప్పు", "salt.png"),
            Ingredient("కొబ్బరి", "coconut.png"),
            Ingredient("మిరియాలు", "black_pepper.png"),
        ]
        
        # Current recipe and game state
        self.current_recipe_index = 0
        self.current_recipe = self.recipes[self.current_recipe_index]
        self.selected_ingredients = []
        self.cooking_stage = "select"  # select, chop, mix, serve
        self.mini_game = None
        self.score = 0
        
        # Background images
        self.background_images = {}
        self.current_background = "kitchen_background.png"
        self.load_background_images()
        
        # Buttons
        self.start_button_rect = pygame.Rect(300, 400, 200, 50)
        self.next_button_rect = pygame.Rect(600, 500, 150, 50)
        self.help_button_rect = pygame.Rect(700, 550, 80, 30)
        self.close_help_rect = pygame.Rect(SCREEN_WIDTH - 30, 20, 20, 20)
        self.show_help = False
        
        # Help text for each stage
        self.help_text = {
            "select": [
                "పదార్థాలు ఎంచుకోండి - Select Ingredients",
                "1. Click on the ingredients needed for the recipe",
                "2. All required ingredients must be selected",
                "3. Click 'Next' when done"
            ],
            "chop": [
                "కోయండి - Chopping",
                "1. Click on the red highlighted areas",
                "2. You need to make 10 successful chops",
                "3. Be quick as the active area changes"
            ],
            "mix": [
                "కలపండి - Mixing",
                "1. Click and hold inside the bowl",
                "2. Move in a circular motion",
                "3. Complete 15 mixing movements"
            ],
            "serve": [
                "వడ్డించండి - Serving",
                "1. Drag the food from the pot to the plate",
                "2. You have 10 seconds to serve",
                "3. Place food completely on the plate"
            ]
        }
        
        # Load sounds
        try:
            sound_path_success = os.path.join(game_dir, "sounds", "success.wav")
            sound_path_error = os.path.join(game_dir, "sounds", "error.wav")
            self.success_sound = pygame.mixer.Sound(sound_path_success)
            self.error_sound = pygame.mixer.Sound(sound_path_error)
        except:
            print("Sound files not found or invalid.")
            self.success_sound = None
            self.error_sound = None
    
    def load_background_images(self):
        """Load background images"""
        bg_names = ["kitchen_background.png", "traditional_kitchen background.png", "modern_kitchen_background.png"]
        for bg_name in bg_names:
            try:
                bg_path = os.path.join(game_dir, "images", bg_name)
                print(f"Attempting to load background from: {bg_path}")
                bg_image = pygame.image.load(bg_path)
                # Scale to fit screen
                bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
                # Fix the key name for traditional kitchen (remove space in key)
                if bg_name == "traditional_kitchen background.png":
                    self.background_images["traditional_kitchen_background.png"] = bg_image
                else:
                    self.background_images[bg_name] = bg_image
                print(f"Successfully loaded background: {bg_name}")
            except (pygame.error, FileNotFoundError) as e:
                print(f"Could not load background image: {bg_name}")
                print(f"Error: {e}")
                # Create a placeholder background
                bg_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                if "traditional" in bg_name:
                    bg_image.fill((200, 180, 140))  # Tan color for traditional kitchen
                elif "modern" in bg_name:
                    bg_image.fill((180, 200, 220))  # Light blue for modern kitchen
                else:
                    bg_image.fill((220, 220, 200))  # Default kitchen color
                # Fix the key name for traditional kitchen (remove space in key)
                if bg_name == "traditional_kitchen background.png":
                    self.background_images["traditional_kitchen_background.png"] = bg_image
                else:
                    self.background_images[bg_name] = bg_image
        
        # Debug: Print all loaded backgrounds
        print("Loaded backgrounds:", list(self.background_images.keys()))
    
    def create_placeholder_ingredients(self):
        """Create ingredients with placeholder images instead of loading from files"""
        # This method is no longer used but kept for reference
        ingredient_names = [
            "బియ్యం", "పసుపు", "నిమ్మకాయ", "కారం", "వేరుశెనగ", "ఆవాలు", 
            "కరివేపాకు", "కందిపప్పు", "ఉల్లిపాయలు", "టమాటా", "కొత్తిమీర", 
            "పెరుగు", "ఉప్పు"
        ]
        
        ingredients = []
        for name in ingredient_names:
            ingredient = Ingredient(name, "placeholder.png")
            ingredients.append(ingredient)
        
        return ingredients
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # Add escape key to exit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                self.handle_event(event)
            
            self.update()
            self.draw()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()
    
    def handle_event(self, event):
        # Handle help button click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.help_button_rect.collidepoint(event.pos):
                self.show_help = True
                return
            if self.show_help and self.close_help_rect.collidepoint(event.pos):
                self.show_help = False
                return
        
        if self.game_state.current_state == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button_rect.collidepoint(event.pos):
                    self.game_state.set_state("recipe_selection")
        
        elif self.game_state.current_state == "recipe_selection":
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if a recipe was clicked
                for i, recipe in enumerate(self.recipes):
                    rect = pygame.Rect(200, 150 + i * 100, 400, 80)
                    if rect.collidepoint(event.pos):
                        self.current_recipe_index = i
                        self.current_recipe = self.recipes[i]
                        self.game_state.set_state("cooking")
                        self.cooking_stage = "select"
                        self.selected_ingredients = []
                        
                        # Update background based on recipe
                        if i == 0:
                            self.current_background = "kitchen_background.png"
                        elif i == 1:
                            self.current_background = "traditional_kitchen_background.png"
                        elif i == 2:
                            self.current_background = "modern_kitchen_background.png"
                        elif i == 3:
                            self.current_background = "kitchen_background.png"
                        elif i == 4:
                            self.current_background = "traditional_kitchen_background.png"
        
        elif self.game_state.current_state == "cooking":
            if self.cooking_stage == "select":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if an ingredient was clicked
                    for ingredient in self.ingredients:
                        # Calculate position based on index
                        idx = self.ingredients.index(ingredient)
                        x = 100 + (idx % 5) * 100
                        y = 150 + (idx // 5) * 100
                        rect = pygame.Rect(x, y, 64, 64)
                        
                        if rect.collidepoint(event.pos):
                            if ingredient.name in self.current_recipe.ingredients:
                                if ingredient.name not in [i.name for i in self.selected_ingredients]:
                                    self.selected_ingredients.append(ingredient)
                                    if self.success_sound:
                                        self.success_sound.play()
                            else:
                                if self.error_sound:
                                    self.error_sound.play()
                    
                    # Check if all ingredients are selected
                    if len(self.selected_ingredients) == len(self.current_recipe.ingredients):
                        self.cooking_stage = "chop"
                        self.mini_game = ChoppingGame()
            
            elif self.cooking_stage == "chop":
                if self.mini_game:
                    result = self.mini_game.handle_event(event)
                    if result == "completed":
                        # Play success sound when completed
                        if self.success_sound:
                            self.success_sound.play()
                        print("Moving from chop to mix stage")  # Debug message
                        self.cooking_stage = "mix"
                        self.mini_game = MixingGame()
            
            elif self.cooking_stage == "mix":
                if self.mini_game:
                    result = self.mini_game.handle_event(event)
                    if result == "completed":
                        # Play success sound when completed
                        if self.success_sound:
                            self.success_sound.play()
                        print("Moving from mix to serve stage")  # Debug message
                        self.cooking_stage = "serve"
                        self.mini_game = ServingGame()
            
            elif self.cooking_stage == "serve":
                if self.mini_game:
                    result = self.mini_game.handle_event(event)
                    if result == "completed":
                        # Play success sound when completed
                        if self.success_sound:
                            self.success_sound.play()
                        print("Dish completed!")  # Debug message
                        self.score += 100
                        self.game_state.set_state("recipe_selection")
            
            # Check if next button was clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.next_button_rect.collidepoint(event.pos):
                    if self.cooking_stage == "select":
                        if len(self.selected_ingredients) == len(self.current_recipe.ingredients):
                            self.cooking_stage = "chop"
                            self.mini_game = ChoppingGame()
                    elif self.cooking_stage == "chop":
                        if self.mini_game and self.mini_game.is_completed():
                            self.cooking_stage = "mix"
                            self.mini_game = MixingGame()
                    elif self.cooking_stage == "mix":
                        if self.mini_game and self.mini_game.is_completed():
                            self.cooking_stage = "serve"
                            self.mini_game = ServingGame()
                    elif self.cooking_stage == "serve":
                        if self.mini_game and self.mini_game.is_completed():
                            self.score += 100
                            self.game_state.set_state("recipe_selection")
    
    def update(self):
        if self.game_state.current_state == "cooking":
            if self.cooking_stage == "chop" and self.mini_game:
                self.mini_game.update()
            elif self.cooking_stage == "mix" and self.mini_game:
                self.mini_game.update()
            elif self.cooking_stage == "serve" and self.mini_game:
                self.mini_game.update()
    
    def draw(self):
        # Force a solid color background first so we can see if the image is being drawn
        self.screen.fill((150, 150, 150))  # Medium gray background
        
        # Always use kitchen_background.png for the first two rounds
        if self.game_state.current_state == "menu" or self.game_state.current_state == "recipe_selection":
            # Try to directly load and use the kitchen background image
            try:
                bg_path = os.path.join(game_dir, "images", "kitchen_background.png")
                bg_image = pygame.image.load(bg_path)
                bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
                self.screen.blit(bg_image, (0, 0))
            except (pygame.error, FileNotFoundError) as e:
                print(f"Error loading background directly: {e}")
                # Use the cached version if available
                if "kitchen_background.png" in self.background_images:
                    self.screen.blit(self.background_images["kitchen_background.png"], (0, 0))
                else:
                    # Fall back to the default background
                    self.screen.blit(self.default_bg, (0, 0))
        else:
            # For other states, use the current recipe's background
            if self.current_background in self.background_images:
                self.screen.blit(self.background_images[self.current_background], (0, 0))
            else:
                # If background not found, try to use a default one that exists
                if "kitchen_background.png" in self.background_images:
                    self.screen.blit(self.background_images["kitchen_background.png"], (0, 0))
                else:
                    # Fall back to the default background
                    self.screen.blit(self.default_bg, (0, 0))
        
        if self.game_state.current_state == "menu":
            # Draw title
            title_text = telugu_font.render("తెలుగు వంటకాలు - Telugu Cooking Game", True, BLACK)
            self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))
            
            # Draw start button in orange
            pygame.draw.rect(self.screen, ORANGE, self.start_button_rect)
            start_text = telugu_font.render("Start", True, BLACK)
            self.screen.blit(start_text, (self.start_button_rect.centerx - start_text.get_width() // 2, 
                                         self.start_button_rect.centery - start_text.get_height() // 2))
        
        elif self.game_state.current_state == "recipe_selection":
            # Clear any previous text by drawing a semi-transparent overlay just for the title area
            #overlay = pygame.Surface((600, 50), pygame.SRCALPHA)
           # overlay.fill((255, 255, 255, 200))  # Semi-transparent white
            #self.screen.blit(overlay, (SCREEN_WIDTH // 2 - 300, 50))
            
            # Draw title
            title_text = telugu_font.render("వంటకం ఎంచుకోండి - Select Recipe", True, BLACK)
            self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))
            
            # Draw recipes
            for i, recipe in enumerate(self.recipes):
                rect = pygame.Rect(200, 150 + i * 100, 400, 80)
                pygame.draw.rect(self.screen, ORANGE, rect)
                recipe_text = telugu_font.render(recipe.name, True, BLACK)
                self.screen.blit(recipe_text, (rect.centerx - recipe_text.get_width() // 2, 
                                             rect.centery - recipe_text.get_height() // 2))
            
            # Draw score
            score_text = telugu_font.render(f"స్కోరు - Score: {self.score}", True, BLACK)
            self.screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 20, 20))
        
        elif self.game_state.current_state == "cooking":
            # Clear any previous text for recipe name and instructions
            #recipe_overlay = pygame.Surface((760, 80), pygame.SRCALPHA)
            #recipe_overlay.fill((255, 255, 255, 200))  # Semi-transparent white
            #self.screen.blit(recipe_overlay, (20, 20))
            
            # Draw recipe name
            recipe_text = telugu_font.render(f"వంటకం - Recipe: {self.current_recipe.name}", True, BLACK)
            self.screen.blit(recipe_text, (20, 20))
            
            # Draw instructions
            instruction_text = small_telugu_font.render(self.current_recipe.instructions, True, BLACK)
            self.screen.blit(instruction_text, (20, 60))
            
            if self.cooking_stage == "select":
                # Clear any previous text for stage title
                #stage_overlay = pygame.Surface((600, 50), pygame.SRCALPHA)
                #stage_overlay.fill((255, 255, 255, 200))  # Semi-transparent white
                #self.screen.blit(stage_overlay, (SCREEN_WIDTH // 2 - 300, 100))
                
                # Draw stage title
                stage_text = telugu_font.render("పదార్థాలు ఎంచుకోండి - Select Ingredients", True, BLACK)
                self.screen.blit(stage_text, (SCREEN_WIDTH // 2 - stage_text.get_width() // 2, 100))
                
                # Draw all ingredients
                for i, ingredient in enumerate(self.ingredients):
                    x = 100 + (i % 5) * 100
                    y = 150 + (i // 5) * 100
                    
                    # Draw ingredient image
                    self.screen.blit(ingredient.image, (x, y))
                    
                    # Draw ingredient name
                    name_text = small_telugu_font.render(ingredient.name, True, BLACK)
                    self.screen.blit(name_text, (x, y + 70))
                    
                    # Highlight if selected
                    if ingredient in self.selected_ingredients:
                        pygame.draw.rect(self.screen, (0, 255, 0), (x, y, 64, 64), 3)
                
                # Draw next button if all ingredients are selected
                if len(self.selected_ingredients) == len(self.current_recipe.ingredients):
                    pygame.draw.rect(self.screen, BLUE, self.next_button_rect)
                    next_text = telugu_font.render("తరువాత - Next", True, BLACK)
                    self.screen.blit(next_text, (self.next_button_rect.centerx - next_text.get_width() // 2, 
                                               self.next_button_rect.centery - next_text.get_height() // 2))
            
            elif self.cooking_stage == "chop" and self.mini_game:
                # Set a background for the chopping stage
                if "kitchen_background.png" in self.background_images:
                    self.screen.blit(self.background_images["kitchen_background.png"], (0, 0))
                else:
                    # Create a placeholder background
                    bg_color = (220, 220, 200)  # Light tan color
                    self.screen.fill(bg_color)
                
                # Clear any previous text for stage title
                #stage_overlay = pygame.Surface((600, 50), pygame.SRCALPHA)
                #stage_overlay.fill((255, 255, 255, 200))  # Semi-transparent white
                #self.screen.blit(stage_overlay, (SCREEN_WIDTH // 2 - 300, 100))
                
                # Draw stage title
                stage_text = telugu_font.render("కోయండి - Chopping", True, BLACK)
                self.screen.blit(stage_text, (SCREEN_WIDTH // 2 - stage_text.get_width() // 2, 100))
                
                self.mini_game.draw(self.screen)
                
                # Draw next button if mini-game is completed
                if self.mini_game.is_completed():
                    pygame.draw.rect(self.screen, BLUE, self.next_button_rect)
                    next_text = telugu_font.render("తరువాత - Next", True, BLACK)
                    self.screen.blit(next_text, (self.next_button_rect.centerx - next_text.get_width() // 2, 
                                               self.next_button_rect.centery - next_text.get_height() // 2))
            
            elif self.cooking_stage == "mix" and self.mini_game:
                # Set a background for the mixing stage
                if "traditional_kitchen_background.png" in self.background_images:
                    self.screen.blit(self.background_images["traditional_kitchen_background.png"], (0, 0))
                else:
                    # Create a placeholder background
                    bg_color = (200, 180, 140)  # Tan color for traditional kitchen
                    self.screen.fill(bg_color)
                
                # Clear any previous text for stage title
               # stage_overlay = pygame.Surface((600, 50), pygame.SRCALPHA)
                #stage_overlay.fill((255, 255, 255, 200))  # Semi-transparent white
                #self.screen.blit(stage_overlay, (SCREEN_WIDTH // 2 - 300, 100))
                
                # Draw stage title
                stage_text = telugu_font.render("కలపండి - Mixing", True, BLACK)
                self.screen.blit(stage_text, (SCREEN_WIDTH // 2 - stage_text.get_width() // 2, 100))
                
                self.mini_game.draw(self.screen)
                
                # Draw next button if mini-game is completed
                if self.mini_game.is_completed():
                    pygame.draw.rect(self.screen, BLUE, self.next_button_rect)
                    next_text = telugu_font.render("తరువాత - Next", True, BLACK)
                    self.screen.blit(next_text, (self.next_button_rect.centerx - next_text.get_width() // 2, 
                                               self.next_button_rect.centery - next_text.get_height() // 2))
            
            elif self.cooking_stage == "serve" and self.mini_game:
                # Clear any previous text for stage title
               # stage_overlay = pygame.Surface((600, 50), pygame.SRCALPHA)
                #stage_overlay.fill((255, 255, 255, 200))  # Semi-transparent white
                #self.screen.blit(stage_overlay, (SCREEN_WIDTH // 2 - 300, 100))
                
                # Draw stage title
                stage_text = telugu_font.render("వడ్డించండి - Serving", True, BLACK)
                self.screen.blit(stage_text, (SCREEN_WIDTH // 2 - stage_text.get_width() // 2, 100))
                
                self.mini_game.draw(self.screen)
                
                # Draw next button if mini-game is completed
                if self.mini_game.is_completed():
                    pygame.draw.rect(self.screen, BLUE, self.next_button_rect)
                    next_text = telugu_font.render("ముగించు - Finish", True, BLACK)
                    self.screen.blit(next_text, (self.next_button_rect.centerx - next_text.get_width() // 2, 
                                               self.next_button_rect.centery - next_text.get_height() // 2))
        
        # Draw help button
        pygame.draw.rect(self.screen, (200, 200, 200), self.help_button_rect)
        help_text = small_telugu_font.render("సహాయం", True, BLACK)
        self.screen.blit(help_text, (self.help_button_rect.centerx - help_text.get_width() // 2, 
                                   self.help_button_rect.centery - help_text.get_height() // 2))
        
        # Draw help overlay if shown
        if self.show_help:
            # Draw semi-transparent overlay
          #  overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
           # overlay.fill((0, 0, 0, 180))  # Semi-transparent black
            #self.screen.blit(overlay, (0, 0))
            
            # Draw help panel
            help_panel = pygame.Rect(100, 100, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 200)
            pygame.draw.rect(self.screen, WHITE, help_panel)
            pygame.draw.rect(self.screen, BLACK, help_panel, 2)
            
            # Draw close button
            pygame.draw.rect(self.screen, (255, 0, 0), self.close_help_rect)
            close_text = telugu_font.render("X", True, WHITE)
            self.screen.blit(close_text, (self.close_help_rect.centerx - close_text.get_width() // 2, 
                                        self.close_help_rect.centery - close_text.get_height() // 2))
            
            # Draw help text for current stage
            help_title = telugu_font.render("సహాయం - Help", True, BLACK)
            self.screen.blit(help_title, (help_panel.centerx - help_title.get_width() // 2, help_panel.y + 20))
            
            help_lines = self.help_text.get(self.cooking_stage, ["No help available for this stage"])
            for i, line in enumerate(help_lines):
                line_text = small_telugu_font.render(line, True, BLACK)
                self.screen.blit(line_text, (help_panel.x + 20, help_panel.y + 60 + i * 30))

# Main game loop
if __name__ == "__main__":
    game = TeluguCookingGame()
    game.run()
