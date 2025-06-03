# Contributing to Telugu Cooking Game

Thank you for your interest in contributing to the Telugu Cooking Game project! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/TeluguCookingGame.git`
3. Create a branch for your changes: `git checkout -b feature/your-feature-name`

## Development Environment

1. Install Python 3.6 or higher
2. Install dependencies: `pip install -r requirements.txt`
3. Run the game: `python src/main.py`

## Adding New Features

### Adding New Recipes

To add a new recipe:

1. Add the recipe to the `recipes` list in `src/main.py`
2. Add any new ingredient images to the `images` directory
3. Update the ingredients list if needed

### Adding New Mini-Games

To add a new mini-game:

1. Create a new class in `src/mini_games.py`
2. Implement the required methods: `__init__`, `handle_event`, `update`, `draw`, and `is_completed`
3. Add the mini-game to the game flow in `src/main.py`

## Code Style

- Follow PEP 8 guidelines
- Use descriptive variable and function names
- Add comments for complex logic
- Keep functions small and focused

## Testing

- Test your changes thoroughly before submitting a pull request
- Ensure the game runs without errors
- Check that all mini-games work correctly

## Submitting Changes

1. Commit your changes: `git commit -m "Add feature: your feature description"`
2. Push to your fork: `git push origin feature/your-feature-name`
3. Create a pull request from your fork to the main repository

## Additional Resources

- [Pygame Documentation](https://www.pygame.org/docs/)
- [Python PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)

Thank you for contributing!
