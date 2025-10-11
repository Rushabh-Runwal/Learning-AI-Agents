"""Main entry point for the course generator system"""

from course_generator_agent import root_agent
import os
import json

def generate_course_topic(topic: str, output_dir: str = None):
    """
    Generate a complete course topic with games
    
    Args:
        topic: The topic to generate (e.g., "trigonometry")
        output_dir: Output directory (defaults to public/topics/<topic>)
    """
    if output_dir is None:
        output_dir = f"public/topics/{topic.lower().replace(' ', '-')}"
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate the course content using the agent
    result = root_agent.generate_course(topic)
    
    return result

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python main.py <topic>")
        sys.exit(1)
    
    topic = sys.argv[1]
    print(f"Generating course for topic: {topic}")
    
    try:
        result = generate_course_topic(topic)
        print(f"Successfully generated course for '{topic}'")
        print(f"Generated {len(result.get('games', []))} games")
    except Exception as e:
        print(f"Error generating course: {e}")
        sys.exit(1)