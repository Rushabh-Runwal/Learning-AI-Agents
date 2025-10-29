"""Quiz Generation Tool"""

from ..config import CONTENT_GENERATOR_MODEL, DEFAULT_QUIZ_QUESTIONS, USE_VERTEX_AI

# Import appropriate SDK based on configuration
if USE_VERTEX_AI:
    from vertexai.generative_models import GenerativeModel
else:
    import google.generativeai as genai
    from ..config import GOOGLE_API_KEY
    genai.configure(api_key=GOOGLE_API_KEY)


def generate_quiz(
    topic: str,
    num_questions: int = DEFAULT_QUIZ_QUESTIONS,
    difficulty: str = "intermediate"
) -> str:
    """
    Generate a multiple-choice quiz on a given topic.
    
    Args:
        topic: The subject to create quiz questions about
        num_questions: Number of questions to generate (5-20)
        difficulty: Level of complexity (beginner, intermediate, advanced)
    
    Returns:
        Generated quiz with questions, options, and answers
    """
    
    # Validate number of questions
    num_questions = max(5, min(20, num_questions))
    
    prompt = f"""Create a {difficulty}-level multiple-choice quiz about: {topic}

Number of Questions: {num_questions}

For each question:
1. Write a clear, {difficulty}-level question
2. Provide 4 answer options (A, B, C, D)
3. Mark the correct answer
4. Include a brief explanation of why the answer is correct

Format:
**Question X:** [Question text]
A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]

**Correct Answer:** [Letter]
**Explanation:** [Why this is correct]

---

Guidelines:
- Questions should test understanding, not just memorization
- Make distractors (wrong answers) plausible but clearly incorrect
- Cover different aspects of the topic
- Progress from easier to harder questions
- Use clear, unambiguous language

Generate the quiz:"""

    try:
        if USE_VERTEX_AI:
            # Ensure Vertex AI is initialized inside Agent Engine
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
            model = genai.GenerativeModel(CONTENT_GENERATOR_MODEL)
            response = model.generate_content(prompt)
            return response.text
    except Exception as e:
        return f"Error generating quiz: {str(e)}"

