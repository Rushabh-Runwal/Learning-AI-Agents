"""Topic planner agent that produces a compact plan with a quiz per subtopic."""

import json
import os
from pathlib import Path
from typing import Dict, Any, List, TypedDict
import re

from google.adk.agents import Agent
from google.adk.tools import FunctionTool

from ..prompts import TOPIC_PLANNER_PROMPT

MODEL = "gemini-2.5-pro"
class Question(TypedDict):
    question: str
    options: List[str]
    correct: int


class GameSpec(TypedDict, total=False):
    type: str
    title: str
    slug: str
    description: str
    questions: List[Question]
    estimatedTime: str
    maxScore: int


class SubtopicSpec(TypedDict):
    title: str
    learningGoals: List[str]
    recommendedGames: List[GameSpec]


class LearningPlan(TypedDict):
    topic: str
    description: str
    subtopics: List[SubtopicSpec]
    totalEstimatedTime: str
    difficultyLevel: str
def _slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return s or "topic"



def plan_topic(plan: Dict[str, Any]) -> Dict[str, Any]:
    """
    Finalize a learning plan crafted by the model.

    The LLM must think and produce the full JSON plan per TOPIC_PLANNER_PROMPT,
    then call this tool with that plan. This function only validates basics and
    returns the plan unchanged so downstream agents can use it.
    """
    if not isinstance(plan, dict) or not plan.get("subtopics"):
        raise ValueError("plan is required and must include 'subtopics'. Provide the full JSON per the prompt.")

    # Minimal normalization: keep provided display topic; ensure subtopics array
    if not isinstance(plan["subtopics"], list):
        raise ValueError("'subtopics' must be an array.")

    # Cross-agent contract: enforce per-type shape with >=5 entries
    ALLOWED_TYPES = {"quiz", "drag-match", "fill-in", "ordering", "target-number", "flash"}
    for sub in plan["subtopics"]:
        games = sub.get("recommendedGames") or []
        if not isinstance(games, list):
            raise ValueError("'recommendedGames' must be an array if present.")
        for game in games:
            gtype = game.get("type")
            if gtype not in ALLOWED_TYPES:
                raise ValueError(f"Unsupported game type: {gtype}. Allowed: {sorted(ALLOWED_TYPES)}")
            # Require a slug
            if not isinstance(game.get("slug"), str) or not game["slug"].strip():
                raise ValueError("Each game must include a non-empty 'slug' (kebab-case recommended).")
            # Enforce maxScore range if provided
            if "maxScore" in game and not (5 <= int(game["maxScore"]) <= 10):
                raise ValueError("maxScore must be between 5 and 10.")

            if gtype == "quiz":
                questions = game.get("questions")
                if not isinstance(questions, list) or len(questions) < 5:
                    raise ValueError("Quiz must include at least 5 questions.")
                for q in questions[:5]:
                    if not isinstance(q, dict) or not q.get("question") or not isinstance(q.get("options"), list) or len(q["options"]) != 4:
                        raise ValueError("Each quiz question must have 'question', 4 'options', and 'correct' index.")
                    if not isinstance(q.get("correct"), int) or q["correct"] not in (0,1,2,3):
                        raise ValueError("'correct' must be an integer 0..3.")
            elif gtype == "drag-match":
                pairs = game.get("pairs")
                if not isinstance(pairs, list) or len(pairs) < 5:
                    raise ValueError("drag-match must include at least 5 pairs.")
                for p in pairs[:5]:
                    if not isinstance(p, dict) or not p.get("term") or not p.get("match"):
                        raise ValueError("Each pair needs 'term' and 'match'.")
            elif gtype == "fill-in":
                items = game.get("items")
                if not isinstance(items, list) or len(items) < 5:
                    raise ValueError("fill-in must include at least 5 items.")
                for it in items[:5]:
                    if not isinstance(it, dict) or not it.get("prompt") or not it.get("answer"):
                        raise ValueError("Each item needs 'prompt' and 'answer'.")
            elif gtype == "ordering":
                items = game.get("items")
                correct = game.get("correctOrder")
                if not isinstance(items, list) or len(items) < 2:
                    raise ValueError("ordering must include at least 2 items.")
                # Auto-generate or repair correctOrder instead of failing
                if not isinstance(correct, list) or len(correct) != len(items):
                    game["correctOrder"] = list(range(len(items)))
            elif gtype == "target-number":
                problems = game.get("problems")
                if not isinstance(problems, list) or len(problems) < 5:
                    raise ValueError("target-number must include at least 5 problems.")
                for pr in problems[:5]:
                    if not isinstance(pr, dict) or not pr.get("prompt") or not (isinstance(pr.get("answerNumber"), (int, float))):
                        raise ValueError("Each problem needs 'prompt' and numeric 'answerNumber'.")
            elif gtype == "flash":
                statements = game.get("statements")
                if not isinstance(statements, list) or len(statements) < 5:
                    raise ValueError("flash must include at least 5 statements.")
                for st in statements[:5]:
                    if not isinstance(st, dict) or not st.get("text") or not isinstance(st.get("isTrue"), bool):
                        raise ValueError("Each statement needs 'text' and boolean 'isTrue'.")

    return plan


def save_learning_plan(plan: Dict[str, Any], output_dir: str = "public/topics") -> Dict[str, Any]:
    topic = plan.get("topic", "unknown")
    out_dir = Path(output_dir) / _slugify(topic)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "learning_plan.json"
    path.write_text(json.dumps(plan, indent=2), encoding="utf-8")
    return {"path": str(path), "plan": plan}


topic_planner_agent = Agent(
    name="topic_planner",
    model=MODEL,
    description="Breaks a topic into subtopics and recommends games",
    instruction=TOPIC_PLANNER_PROMPT,
    tools=[
        FunctionTool(plan_topic),
        FunctionTool(save_learning_plan),
    ],
    output_key="learning_plan",
)