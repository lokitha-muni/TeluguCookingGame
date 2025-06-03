# Telugu Cooking Game

A Pygame-based cooking game featuring traditional Telugu dishes like Pulihora, Pappu, and Perugu. The game includes Telugu labels for ingredients, instructions, and scoring.

## Features

- Three traditional Telugu dishes to prepare
- Mini-games for chopping, mixing, and serving
- Telugu language interface
- Sound effects for cooking actions
- Score tracking system

## Requirements

- Python 3.6+
- Pygame

## Installation

1. Install Python from [python.org](https://www.python.org/downloads/)
2. Install Pygame:
   ```
   pip install pygame
   ```
3. Download Telugu font (Noto Sans Telugu) from Google Fonts and place it in the `fonts` directory

## Directory Structure

```
TeluguCookingGame/
├── images/         # Images for ingredients and UI elements
├── sounds/         # Sound effects for cooking actions
├── fonts/          # Telugu fonts
└── src/            # Game source code
    ├── main.py     # Main game file
    ├── game_state.py
    ├── recipe.py
    ├── ingredient.py
    └── mini_games.py
```

## How to Play

1. Run the game:
   ```
   python src/main.py
   ```
2. Select a dish to prepare
3. Complete the mini-games for each ingredient:
   - Chopping: Click on the red circles to chop ingredients
   - Mixing: Stir in the correct direction by moving your mouse
   - Serving: Drag and drop the food onto the plates

## Adding New Dishes

To add new dishes, modify the `recipes` list in `main.py` with new Recipe objects containing:
- Telugu name of the dish
- List of ingredients in Telugu
- Cooking instructions in Telugu

## Credits

- Game developed as a Telugu cooking educational tool
- Uses Noto Sans Telugu font from Google Fonts
