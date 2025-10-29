"""Video Content Generation Tool"""

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


def generate_video_content(
    topic: str,
    duration: str = "medium",
    difficulty: str = "intermediate"
) -> str:
    """
    Generate a complete video script with timestamps and visual suggestions.
    
    Args:
        topic: The subject to create video content about
        duration: Target video length (short=3-5min, medium=8-12min, long=15-20min)
        difficulty: Level of complexity (beginner, intermediate, advanced)
    
    Returns:
        Generated video script with timestamps and production notes
    """
    
    # Define duration guidelines
    duration_guide = {
        "short": "3-5 minutes",
        "medium": "8-12 minutes",
        "long": "15-20 minutes"
    }
    
    prompt = f"""Create a comprehensive video script about: {topic}

Target Duration: {duration_guide.get(duration, duration_guide['medium'])}
Difficulty Level: {difficulty}

Include:

1. **VIDEO TITLE**: Catchy, descriptive title

2. **VIDEO HOOK (0:00-0:30)**
   - Opening statement to grab attention
   - Why viewers should watch
   - What they'll learn

3. **INTRODUCTION (0:30-1:00)**
   - Brief overview of the topic
   - Context and relevance

4. **MAIN CONTENT**
   - Break into 3-5 major sections
   - Each section with timestamp
   - Clear explanations
   - Visual suggestions (e.g., [SHOW: diagram], [ANIMATION: process])

5. **EXAMPLES/DEMONSTRATIONS**
   - Practical applications
   - Step-by-step demonstrations

6. **SUMMARY & CALL-TO-ACTION**
   - Recap key points
   - Encourage engagement (like, subscribe, comment)

Format each section with:
**[TIMESTAMP]** Section Title
- Script text
- [VISUAL: description of what to show on screen]
- [B-ROLL: suggested supplementary footage]

Guidelines:
- Use conversational, engaging tone
- Keep explanations clear and concise
- Suggest specific visuals and animations
- Include pauses for emphasis
- Match {difficulty} level
- Make it entertaining and educational

Generate the video script:"""

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
        return f"Error generating video content: {str(e)}"

