"""Reading Material Generation Tool"""

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


def generate_reading_material(
    topic: str,
    difficulty: str = "intermediate",
    length: str = "medium"
) -> str:
    """
    Generate comprehensive reading material on a given topic.
    
    Args:
        topic: The subject to create reading material about
        difficulty: Level of complexity (beginner, intermediate, advanced)
        length: Desired length (short, medium, long)
    
    Returns:
        Generated reading material as formatted text
    """
    
    # Define length guidelines
    length_guide = {
        "short": "500-800 words, 5-10 minute read",
        "medium": "1000-1500 words, 10-20 minute read",
        "long": "2000-3000 words, 20-30 minute read"
    }
    
    prompt = f"""Create comprehensive reading material about: {topic}

Difficulty Level: {difficulty}
Target Length: {length_guide.get(length, length_guide['medium'])}

Structure the content with:
1. **Introduction** - Overview and importance of the topic
2. **Main Content** - Detailed explanation broken into logical sections
3. **Key Concepts** - Important terms and definitions
4. **Examples** - Real-world applications or examples
5. **Summary** - Recap of main points
6. **Further Reading** - Suggestions for deeper learning

Guidelines:
- Use clear, {difficulty}-level language
- Include relevant examples
- Break complex ideas into digestible parts
- Use headings and subheadings for organization
- Make it engaging and educational

Generate the reading material:"""

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
        return f"Error generating reading material: {str(e)}"

