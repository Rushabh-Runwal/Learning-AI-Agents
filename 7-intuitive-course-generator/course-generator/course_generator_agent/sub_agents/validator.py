"""Validator agent that works in a loop until games pass validation"""

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from ..prompts import VALIDATOR_PROMPT
import json
from pathlib import Path
from typing import Dict, Any, List
import re

MODEL = "gemini-2.5-pro"


"""Keep function signatures simple for ADK auto-calling. Internal structures remain plain dicts."""

def _slugify(text: str) -> str:
    """Simple kebab-case slugifier to match generator paths."""
    s = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return s or "topic"


def validate_game_files(topic: str, games_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates generated game files and returns validation results
    
    Args:
        topic: The topic name
        games_data: Dictionary containing game information from generator
        
    Returns:
        dict: Validation results with pass/fail status and fixes needed
    """
    # Use slug to match generator output directory
    topic_dir = Path(f"public/topics/{_slugify(topic)}")
    validation_results: Dict[str, Any] = {
        "validation_passed": True,
        "issues_found": [],
        "fixes_applied": [],
        "games_validated": []
    }
    
    if not topic_dir.exists():
        validation_results["validation_passed"] = False
        validation_results["issues_found"].append(f"Topic directory {topic_dir} does not exist")
        return validation_results
    
    # Check metadata.json
    metadata_file = topic_dir / "metadata.json"
    if not metadata_file.exists():
        validation_results["validation_passed"] = False
        validation_results["issues_found"].append("metadata.json missing")
    else:
        try:
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
                
            # Validate metadata structure
            required_fields = ["topic", "games", "createdAt"]
            for field in required_fields:
                if field not in metadata:
                    validation_results["validation_passed"] = False
                    validation_results["issues_found"].append(f"Missing field '{field}' in metadata.json")
                    
        except json.JSONDecodeError as e:
            validation_results["validation_passed"] = False
            validation_results["issues_found"].append(f"Invalid JSON in metadata.json: {e}")
    
    # Validate each game file
    if "games" in games_data:
        for game in games_data["games"]:
            game_slug = game.get("slug", "")
            game_file = topic_dir / f"game-{game_slug}.html"
            
            game_validation = {
                "slug": game_slug,
                "file_exists": game_file.exists(),
                "html_valid": False,
                "score_valid": False,
                "js_valid": False
            }
            
            if game_file.exists():
                try:
                    with open(game_file, 'r') as f:
                        content = f.read()
                    
                    # Basic HTML validation
                    required_elements = [
                        '<html', '<head>', '<body>', 
                        'id="game-container"', 'id="score-display"',
                        'window.__GAME_OK__'
                    ]
                    
                    missing_elements = []
                    for element in required_elements:
                        if element not in content:
                            missing_elements.append(element)
                    
                    if not missing_elements:
                        game_validation["html_valid"] = True
                        game_validation["js_valid"] = True
                    else:
                        validation_results["issues_found"].append(
                            f"Game {game_slug} missing elements: {missing_elements}"
                        )
                    
                    # Validate score range (5-10 points)
                    max_score = game.get("maxScore", 0)
                    if 5 <= max_score <= 10:
                        game_validation["score_valid"] = True
                    else:
                        validation_results["issues_found"].append(
                            f"Game {game_slug} has invalid maxScore: {max_score} (should be 5-10)"
                        )
                    
                    # Content quality checks to reject placeholders
                    if 'Placeholder question' in content or 'Concept A' in content or 'Def A' in content:
                        validation_results["issues_found"].append(
                            f"Game {game_slug} appears to include placeholder content. Provide topic-specific questions and options."
                        )
                        validation_results["validation_passed"] = False
                        
                except Exception as e:
                    validation_results["issues_found"].append(
                        f"Error reading game file {game_slug}: {e}"
                    )
            else:
                validation_results["issues_found"].append(f"Game file {game_slug} does not exist")
            
            validation_results["games_validated"].append(game_validation)
            
            # If any game validation failed, overall validation fails
            if not all(game_validation.values()):
                validation_results["validation_passed"] = False
    
    return validation_results

def fix_validation_issues(topic: str, validation_results: Dict[str, Any], games_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Attempts to fix validation issues found
    
    Args:
        topic: The topic name
        validation_results: Results from validation check
        games_data: Original games data for reference
        
    Returns:
        dict: Updated validation results after fixes
    """
    # Normalize structure to avoid KeyError if LLM/tool passed partial data
    if not isinstance(validation_results, dict):
        validation_results = {}
    if "validation_passed" not in validation_results:
        validation_results = {
            "validation_passed": False,
            "issues_found": validation_results.get("issues_found", []) if isinstance(validation_results, dict) else [],
            "fixes_applied": [],
            "games_validated": [],
        }
    if validation_results["validation_passed"]:
        return validation_results
    
    topic_dir = Path(f"public/topics/{_slugify(topic)}")
    fixes_applied = []
    
    # Fix missing metadata.json
    if "metadata.json missing" in validation_results["issues_found"]:
        try:
            metadata = {
                "topic": topic,
                "games": games_data.get("games", []),
                "createdAt": "2025-10-08T00:00:00Z"
            }
            
            with open(topic_dir / "metadata.json", 'w') as f:
                json.dump(metadata, f, indent=2)
                
            fixes_applied.append("Created missing metadata.json")
            
        except Exception as e:
            fixes_applied.append(f"Failed to create metadata.json: {e}")
    
    # Fix invalid maxScore values
    for issue in validation_results["issues_found"]:
        if "invalid maxScore" in issue:
            # Extract game slug and fix the score
            try:
                # This is a simplified fix - in a real implementation,
                # you'd need to parse and modify the HTML file
                fixes_applied.append(f"Attempted to fix maxScore issue: {issue}")
            except Exception as e:
                fixes_applied.append(f"Failed to fix maxScore: {e}")
    
    # Re-run validation to see if issues are resolved
    updated_results = validate_game_files(topic, games_data)
    updated_results["fixes_applied"] = fixes_applied
    
    return updated_results

validator_agent = Agent(
    name="validator",
    model=MODEL,
    description="Validates generated game files and fixes issues until validation passes",
    instruction=VALIDATOR_PROMPT,
    tools=[
        FunctionTool(validate_game_files),
        FunctionTool(fix_validation_issues),
    ],
    output_key="validator_results"
)