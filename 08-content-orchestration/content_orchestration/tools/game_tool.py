"""Educational Game Generation Tool"""

from ..config import CONTENT_GENERATOR_MODEL

# Prefer Vertex AI in deployed environments; fall back to GenAI if needed
_use_genai_fallback = False
try:
    from vertexai.generative_models import GenerativeModel  # type: ignore
except Exception:
    _use_genai_fallback = True
    import google.generativeai as genai  # type: ignore
    from ..config import GOOGLE_API_KEY
    genai.configure(api_key=GOOGLE_API_KEY)


def generate_game(
    topic: str,
    game_type: str = "interactive",
    difficulty: str = "intermediate"
) -> str:
    """
    Generate an educational game design on a given topic.
    
    Args:
        topic: The subject to create a game about
        game_type: Type of game (quiz, puzzle, simulation, interactive)
        difficulty: Level of complexity (beginner, intermediate, advanced)
    
    Returns:
        Generated game design with rules, mechanics, and implementation guide
    """
    
    prompt = f"""Design an engaging educational game about: {topic}

Game Type: {game_type}
Difficulty Level: {difficulty}

Create a complete game design including:

1. **GAME TITLE & CONCEPT**
   - Catchy name
   - One-sentence pitch
   - Learning objectives

2. **GAME MECHANICS**
   - How the game works
   - Core gameplay loop
   - Progression system
   - Scoring/reward system

3. **RULES**
   - How to play
   - Win/loss conditions
   - Constraints and limitations

4. **CONTENT & CHALLENGES**
   - Types of questions/puzzles
   - Difficulty progression
   - Example challenges (3-5)

5. **VISUAL DESIGN**
   - UI layout suggestions
   - Color scheme
   - Graphics/icons needed
   - Screen flow

6. **EDUCATIONAL VALUE**
   - What players will learn
   - How the game reinforces concepts
   - Assessment methods

7. **IMPLEMENTATION GUIDE**
   - Recommended platform (web, mobile, paper)
   - Technology stack (if digital)
   - Development steps
   - Estimated complexity

8. **SAMPLE GAMEPLAY**
   - Walk through a typical play session
   - Example scenarios

Guidelines:
- Make it fun and engaging
- Balance education with entertainment
- Match {difficulty} level
- Ensure clear learning outcomes
- Include replay value
- Make it accessible

Generate the game design:"""

    try:
        if not _use_genai_fallback:
            # Vertex AI path
            import os
            import vertexai
            vertexai.init(
                project=os.getenv("GOOGLE_CLOUD_PROJECT"),
                location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
            )
            model = GenerativeModel(CONTENT_GENERATOR_MODEL)
            response = model.generate_content(prompt)
            return response.text
        else:
            # GenAI fallback
            model = genai.GenerativeModel(CONTENT_GENERATOR_MODEL)
            response = model.generate_content(prompt)
            return response.text
    except Exception as e:
        return f"Error generating game: {str(e)}"

