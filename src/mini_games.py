import pygame
import random

class MiniGame:
    def __init__(self):
        self.completed = False
    
    def handle_event(self, event):
        pass
    
    def update(self):
        pass
    
    def draw(self, screen):
        pass
    
    def is_completed(self):
        return self.completed

class ChoppingGame(MiniGame):
    def __init__(self):
        super().__init__()
        self.chop_count = 0
        self.required_chops = 10
        self.chop_areas = [
            pygame.Rect(200, 200, 100, 100),
            pygame.Rect(350, 200, 100, 100),
            pygame.Rect(500, 200, 100, 100)
        ]
        self.active_area = random.choice(self.chop_areas)
        self.timer = 0
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.active_area.collidepoint(event.pos):
                self.chop_count += 1
                self.active_area = random.choice(self.chop_areas)
                if self.chop_count >= self.required_chops:
                    self.completed = True
                    print("Chopping completed!")  # Debug message
                    return "completed"
        return None
    
    def update(self):
        self.timer += 1
        if self.timer > 60:  # Change active area every second
            self.active_area = random.choice(self.chop_areas)
            self.timer = 0
    
    def draw(self, screen):
        # Create a semi-transparent overlay for text area to prevent overlapping
       # text_overlay = pygame.Surface((400, 50), pygame.SRCALPHA)
       # text_overlay.fill((255, 255, 255, 200))  # Semi-transparent white
        #screen.blit(text_overlay, (200, 100))
        
        # Draw instructions
        font = pygame.font.SysFont(None, 36)
        instructions = font.render("", True, (0, 0, 0))
        screen.blit(instructions, (300, 100))
        
        # Create overlay for progress text
        #progress_overlay = pygame.Surface((100, 40), pygame.SRCALPHA)
       # progress_overlay.fill((255, 255, 255, 200))
        #screen.blit(progress_overlay, (350, 350))
        
        # Draw progress
        progress = font.render(f"{self.chop_count}/{self.required_chops}", True, (0, 0, 0))
        screen.blit(progress, (350, 350))
        
        # Draw chopping areas
        for area in self.chop_areas:
            color = (255, 0, 0) if area == self.active_area else (200, 200, 200)
            pygame.draw.rect(screen, color, area)

class MixingGame(MiniGame):
    def __init__(self):
        super().__init__()
        self.mix_count = 0
        self.required_mixes = 15
        self.mix_direction = "clockwise"
        self.last_pos = None
        self.bowl_rect = pygame.Rect(300, 200, 200, 200)
        self.center = (400, 300)
        self.last_angle = None
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            
            if self.bowl_rect.collidepoint(pos):
                if self.last_pos:
                    # Calculate angle from center
                    dx1, dy1 = self.last_pos[0] - self.center[0], self.last_pos[1] - self.center[1]
                    dx2, dy2 = pos[0] - self.center[0], pos[1] - self.center[1]
                    
                    # Calculate angles
                    angle1 = pygame.math.Vector2(dx1, dy1).angle_to((1, 0))
                    angle2 = pygame.math.Vector2(dx2, dy2).angle_to((1, 0))
                    
                    # Check if we've moved enough
                    if abs(angle2 - angle1) > 10:
                        # Check direction
                        if self.mix_direction == "clockwise" and angle2 < angle1:
                            self.mix_count += 1
                        elif self.mix_direction == "counterclockwise" and angle2 > angle1:
                            self.mix_count += 1
                        
                        if self.mix_count >= self.required_mixes:
                            self.completed = True
                            return "completed"
                
                self.last_pos = pos
        
        if event.type == pygame.MOUSEBUTTONUP:
            self.last_pos = None
        
        return None
    
    def draw(self, screen):
        # Create a semi-transparent overlay for text area to prevent overlapping
        #text_overlay = pygame.Surface((400, 50), pygame.SRCALPHA)
       # text_overlay.fill((255, 255, 255, 200))  # Semi-transparent white
        #screen.blit(text_overlay, (200, 100))
        
        # Draw instructions
        font = pygame.font.SysFont(None, 36)
        instructions = font.render("", True, (0, 0, 0))
        screen.blit(instructions, (300, 100))
        
        # Create overlay for progress text
        #progress_overlay = pygame.Surface((100, 40), pygame.SRCALPHA)
        #progress_overlay.fill((255, 255, 255, 200))
        #screen.blit(progress_overlay, (350, 450))
        
        # Draw progress
        progress = font.render(f"{self.mix_count}/{self.required_mixes}", True, (0, 0, 0))
        screen.blit(progress, (350, 450))
        
        # Draw bowl
        pygame.draw.ellipse(screen, (200, 200, 200), self.bowl_rect)
        pygame.draw.ellipse(screen, (150, 150, 150), self.bowl_rect, 5)

class ServingGame(MiniGame):
    def __init__(self):
        super().__init__()
        self.plate_rect = pygame.Rect(300, 400, 200, 50)
        self.pot_rect = pygame.Rect(300, 150, 200, 100)
        self.food_rect = pygame.Rect(350, 175, 100, 50)
        self.dragging = False
        self.served = False
        self.time_limit = 10 * 60  # 10 seconds at 60 FPS
        self.timer = 0
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.food_rect.collidepoint(event.pos):
                self.dragging = True
        
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.food_rect.center = event.pos
        
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
            if self.plate_rect.contains(self.food_rect):
                self.served = True
                self.completed = True
                return "completed"
        
        return None
    
    def update(self):
        self.timer += 1
        if self.timer >= self.time_limit and not self.completed:
            self.completed = True
            return "timeout"
    
    def draw(self, screen):
        # Create a semi-transparent overlay for text area to prevent overlapping
        #text_overlay = pygame.Surface((400, 50), pygame.SRCALPHA)
        #text_overlay.fill((255, 255, 255, 200))  # Semi-transparent white
        #screen.blit(text_overlay, (200, 100))
        
        # Draw instructions
        font = pygame.font.SysFont(None, 36)
        instructions = font.render("", True, (0, 0, 0))
        screen.blit(instructions, (300, 100))
        
        # Create overlay for time text
        time_overlay = pygame.Surface((150, 40), pygame.SRCALPHA)
        time_overlay.fill((255, 255, 255, 200))
        screen.blit(time_overlay, (650, 100))
        
        # Draw time remaining
        time_left = max(0, (self.time_limit - self.timer) // 60)
        time_text = font.render(f"Time: {time_left}s", True, (255, 0, 0) if time_left <= 3 else (0, 0, 0))
        screen.blit(time_text, (650, 100))
        
        # Draw pot
        pygame.draw.rect(screen, (100, 100, 100), self.pot_rect)

        # Draw plate
        pygame.draw.ellipse(screen, (255, 255, 255), self.plate_rect)
        pygame.draw.ellipse(screen, (200, 200, 200), self.plate_rect, 3)
        
        # Draw food
        if not self.served:
            pygame.draw.ellipse(screen, (255, 200, 0), self.food_rect)
        
