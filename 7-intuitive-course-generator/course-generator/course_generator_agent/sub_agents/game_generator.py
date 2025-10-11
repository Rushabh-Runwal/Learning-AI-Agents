"""Game Generator Agent that creates HTML game files from learning plans."""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import re

from google.adk.agents import Agent
from google.adk.tools import FunctionTool

from ..prompts import GAME_GENERATOR_PROMPT

MODEL = "gemini-2.5-pro"


# Keep runtime validation in code; avoid complex typing that breaks ADK tool schema

def _slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return s or "topic"


def create_topic_directory(topic: str) -> Dict[str, Any]:
    """Creates the topic directory structure using a kebab-case slug folder."""
    topic_slug = _slugify(topic)
    topic_dir = Path(f"public/topics/{topic_slug}")
    topic_dir.mkdir(parents=True, exist_ok=True)
    
    # Create assets directory
    assets_dir = topic_dir / "assets"
    assets_dir.mkdir(exist_ok=True)
    
    return {
        "topic": topic,
        "topic_slug": topic_slug,
        "topic_directory": str(topic_dir),
        "assets_directory": str(assets_dir),
        "created": True
    }

def generate_quiz_game(topic: str, game_spec: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates a quiz game HTML file
    
    Args:
        topic: The main topic
        game_spec: Game specification with questions and metadata
        
    Returns:
        dict: Generation results
    """
    topic_slug = _slugify(topic)
    slug = game_spec.get("slug", "quiz")
    title = game_spec.get("title", "Quiz Game")
    questions = game_spec.get("questions", [])
    # Validate content richness before rendering
    if not isinstance(questions, list) or len(questions) < 5:
        raise ValueError(
            "Game spec must include at least 5 well-formed questions. Provide rich, topic-specific content in the plan."
        )
    # Use first 5 for a 10-point quiz (2 points each)
    questions = questions[:5]

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - {topic.title()}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="../../styles/theme.css">
    <script src="../../scripts/common.js"></script>
</head>
<body class="bg-gradient-to-br from-purple-50 to-indigo-100 min-h-screen">
    <div class="container mx-auto px-4 py-8">
        <!-- Header -->
        <header class="text-center mb-8">
            <h1 class="text-3xl font-bold text-purple-800 mb-2">{title}</h1>
            <p class="text-purple-600">Topic: {topic.title()}</p>
            <div id="score-display" class="mt-4">
                <span class="bg-purple-100 text-purple-800 px-4 py-2 rounded-full font-semibold">
                    Score: <span id="current-score">0</span> / 10
                </span>
            </div>
        </header>

        <!-- Game Container -->
        <div id="game-container" class="max-w-2xl mx-auto">
            <div id="question-container" class="bg-white rounded-lg shadow-lg p-6 mb-6">
                <div id="progress-bar" class="w-full bg-gray-200 rounded-full h-2 mb-6">
                    <div id="progress" class="bg-purple-600 h-2 rounded-full" style="width: 0%"></div>
                </div>
                
                <div id="question-content">
                    <!-- Questions will be inserted here -->
                </div>
                <div class="flex justify-between mt-6">
                    <button id="prev-btn" class="btn-secondary" disabled>Previous</button>
                    <button id="next-btn" class="btn-primary">Next</button>
                    <button id="submit-btn" class="btn-primary hidden">Submit Quiz</button>
                </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Game Data
        const questions = {json.dumps(questions, indent=8)};
        
        // Game State
        let currentQuestion = 0;
        let score = 0;
        let answers = [];
        
        // Initialize game
        function initGame() {{
            displayQuestion();
            updateProgress();
            window.__GAME_OK__ = true; // Validation flag
        }}
        
        function displayQuestion() {{
            const question = questions[currentQuestion];
            const container = document.getElementById('question-content');
            
            container.innerHTML = `
                <h3 class="text-xl font-semibold mb-4">${{question.question}}</h3>
                <div class="space-y-3">
                    ${{question.options.map((option, index) => `
                        <label class="flex items-center p-3 border rounded-lg hover:bg-purple-50 cursor-pointer">
                            <input type="radio" name="answer" value="${{index}}" class="mr-3">
                            <span>${{option}}</span>
                        </label>
                    `).join('')}}
                </div>
            `;
            
            // Update button states
            document.getElementById('prev-btn').disabled = currentQuestion === 0;
            document.getElementById('next-btn').style.display = currentQuestion === questions.length - 1 ? 'none' : 'block';
            document.getElementById('submit-btn').style.display = currentQuestion === questions.length - 1 ? 'block' : 'none';
        }}
        
        function updateProgress() {{
            const progress = ((currentQuestion + 1) / questions.length) * 100;
            document.getElementById('progress').style.width = progress + '%';
        }}
        
        function nextQuestion() {{
            saveAnswer();
            if (currentQuestion < questions.length - 1) {{
                currentQuestion++;
                displayQuestion();
                updateProgress();
            }}
        }}
        
        function prevQuestion() {{
            if (currentQuestion > 0) {{
                currentQuestion--;
                displayQuestion();
                updateProgress();
            }}
        }}
        
        function saveAnswer() {{
            const selected = document.querySelector('input[name="answer"]:checked');
            if (selected) {{
                answers[currentQuestion] = parseInt(selected.value);
            }}
        }}
        
        function submitQuiz() {{
            saveAnswer();
            calculateScore();
            showResults();
        }}
        
        function calculateScore() {{
            score = 0;
            questions.forEach((question, index) => {{
                if (answers[index] === question.correct) {{
                    score += 2; // 2 points per question = 10 total
                }}
            }});
            
            document.getElementById('current-score').textContent = score;
        }}
        
        function showResults() {{
            document.getElementById('question-container').classList.add('hidden');
            document.getElementById('results-screen').classList.remove('hidden');
            
            document.getElementById('final-score').textContent = score + ' / 10';
            
            let message = '';
            if (score >= 8) message = '🎉 Excellent work!';
            else if (score >= 6) message = '👍 Good job!';
            else if (score >= 4) message = '📚 Keep studying!';
            else message = '💪 Practice makes perfect!';
            
            document.getElementById('score-message').textContent = message;
            
            // Persist progress so topic page can read it later
            try {{
                const key = '{topic_slug}';
                const existing = (window.CourseGenerator && window.CourseGenerator.loadProgress)
                    ? (window.CourseGenerator.loadProgress(key) || {{ "games": {{}} }})
                    : {{ "games": {{}} }};
                const prev = existing.games['{slug}'] || {{ "attempts": 0, "bestScore": 0 }};
                existing.games['{slug}'] = {{
                    "completed": true,
                    "score": score,
                    "attempts": (prev.attempts || 0) + 1,
                    "bestScore": Math.max(prev.bestScore || 0, score)
                }};
                if (window.CourseGenerator && window.CourseGenerator.saveProgress) {{
                    window.CourseGenerator.saveProgress(key, existing);
                }}
            }} catch (e) {{ /* ignore */ }}
        }}
        
        function retry() {{
            currentQuestion = 0;
            score = 0;
            answers = [];
            document.getElementById('question-container').classList.remove('hidden');
            document.getElementById('results-screen').classList.add('hidden');
            initGame();
        }}
        
        // Event Listeners
        document.getElementById('next-btn').addEventListener('click', nextQuestion);
        document.getElementById('prev-btn').addEventListener('click', prevQuestion);
        document.getElementById('submit-btn').addEventListener('click', submitQuiz);
        document.getElementById('retry-btn').addEventListener('click', retry);
        
        // Initialize when page loads
        document.addEventListener('DOMContentLoaded', initGame);
    </script>
</body>
</html>"""
    
    # Save the HTML file
    topic_dir = Path(f"public/topics/{topic_slug}")
    game_file = topic_dir / f"game-{slug}.html"
    
    try:
        with open(game_file, 'w') as f:
            f.write(html_content)
        
        return {
            "success": True,
            "file_path": str(game_file),
            "game_type": "quiz",
            "slug": slug,
            "title": title,
            "maxScore": 10
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "slug": slug
        }

def _generate_drag_match_game(topic: str, game_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Scaffold: drag-match game (uses styling and validation markers)."""
        topic_slug = _slugify(topic)
        slug = game_spec.get("slug", "drag-match")
        title = game_spec.get("title", "Drag & Match")
        pairs = game_spec.get("pairs", [])
        if not isinstance(pairs, list) or len(pairs) < 5:
                raise ValueError("Game spec must include at least 5 pairs.")

        # Minimal functional placeholder with styling; TODO: implement full drag-drop logic
        html = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
    <title>{title} - {topic.title()}</title>
    <script src=\"https://cdn.tailwindcss.com\"></script>
    <link rel=\"stylesheet\" href=\"../../styles/theme.css\" />
    <script src=\"../../scripts/common.js\"></script>
</head>
<body class=\"bg-gradient-to-br from-purple-50 to-indigo-100 min-h-screen\">
    <div class=\"container mx-auto px-4 py-8\">
        <header class=\"text-center mb-8\">
            <h1 class=\"text-3xl font-bold text-purple-800 mb-2\">{title}</h1>
            <p class=\"text-purple-600\">Topic: {topic.title()}</p>
            <div id=\"score-display\" class=\"mt-4\">
                <span class=\"bg-purple-100 text-purple-800 px-4 py-2 rounded-full font-semibold\">Score: <span id=\"current-score\">0</span> / 10</span>
            </div>
        </header>
        <main id=\"game-container\" class=\"max-w-3xl mx-auto bg-white rounded-lg shadow-lg p-6\">
            <p class=\"mb-4 text-sm text-purple-700\">Drag items from left to their matching definitions on the right. (Prototype)</p>
            <div class=\"grid grid-cols-1 md:grid-cols-2 gap-6\">
                <ul id=\"terms\" class=\"space-y-2\"></ul>
                <ul id=\"matches\" class=\"space-y-2\"></ul>
            </div>
            <div class=\"mt-6 flex justify-end\">
                <button id=\"submit-btn\" class=\"btn-primary\">Check</button>
            </div>
        </main>
    </div>
    <script>
        const pairs = {json.dumps(pairs, indent=2)};
        let score = 0;
        function init() {{
            const t = document.getElementById('terms');
            const m = document.getElementById('matches');
            pairs.forEach((p, i) => {{
                const liT = document.createElement('li');
                liT.className = 'p-3 border rounded bg-purple-50';
                liT.textContent = p.term;
                t.appendChild(liT);
                const liM = document.createElement('li');
                liM.className = 'p-3 border rounded';
                liM.textContent = p.match;
                m.appendChild(liM);
            }});
            window.__GAME_OK__ = true;
        }}
        document.getElementById('submit-btn').addEventListener('click', () => {{
            score = Math.min(10, pairs.length * 2); // placeholder scoring
            document.getElementById('current-score').textContent = score;
        }});
        document.addEventListener('DOMContentLoaded', init);
    </script>
</body>
</html>"""
        topic_dir = Path(f"public/topics/{topic_slug}")
        game_file = topic_dir / f"game-{slug}.html"
        with open(game_file, 'w', encoding='utf-8') as f:
                f.write(html)
        return {"success": True, "file_path": str(game_file), "game_type": "drag-match", "slug": slug, "title": title, "maxScore": 10}


def generate_games_from_plan(learning_plan: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main function to generate all games from a learning plan
    
    Args:
        learning_plan: The learning plan from topic planner
        
    Returns:
        dict: Results of game generation with file paths and metadata
    """
    topic_display = learning_plan.get("topic", "unknown")
    topic_slug = _slugify(topic_display)
    subtopics = learning_plan.get("subtopics", [])
    
    # Create topic directory
    dir_result = create_topic_directory(topic_display)
    
    generated_games = []
    
    # Generate games for each subtopic
    for subtopic in subtopics:
        recommended_games = subtopic.get("recommendedGames", [])
        
        for game_spec in recommended_games:
            gtype = (game_spec.get("type") or '').lower()
            game_result = None
            if gtype == "quiz":
                game_result = generate_quiz_game(topic_display, game_spec)
            elif gtype == "drag-match":
                game_result = _generate_drag_match_game(topic_display, game_spec)
            # TODO: implement fill-in, ordering, target-number, flash
            if game_result and game_result.get("success"):
                generated_games.append({
                    "slug": game_result["slug"],
                    "title": game_result["title"],
                    "type": game_result.get("game_type", gtype or "unknown"),
                    "maxScore": game_result.get("maxScore", 10)
                })
    
    # Create metadata.json
    metadata = {
        "topic": topic_display,
        "games": generated_games,
        "createdAt": datetime.now().isoformat() + "Z"
    }
    
    topic_dir = Path(f"public/topics/{topic_slug}")
    metadata_file = topic_dir / "metadata.json"
    
    try:
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return {
            "success": True,
            "topic": topic_display,
            "games": generated_games,
            "metadata_file": str(metadata_file),
            "total_games": len(generated_games)
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to create metadata: {e}",
            "topic": topic_display,
            "games": generated_games
        }

def save_game_metadata(games: List[Dict[str, Any]], topic: str, output_dir: str) -> str:
    """
    Save metadata file for the topic
    
    Args:
        games: List of generated games
        topic: Topic name
        output_dir: Output directory
        
    Returns:
        str: Path to metadata file
    """
    metadata = {
        'topic': topic,
        'description': f'Interactive learning games for {topic}',
        'games': games,
        'createdAt': '2025-10-08T00:00:00Z'
    }
    
    os.makedirs(output_dir, exist_ok=True)
    metadata_file = os.path.join(output_dir, 'metadata.json')
    
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    return metadata_file

game_generator_agent = Agent(
    name="game_generator",
    model=MODEL,
    description="Generates interactive HTML/CSS/JS game files from learning plans",
    instruction=GAME_GENERATOR_PROMPT,
    tools=[
        FunctionTool(create_topic_directory),
        FunctionTool(generate_quiz_game),
        FunctionTool(generate_games_from_plan),
        FunctionTool(save_game_metadata),
    ],
    output_key="generated_games",
)