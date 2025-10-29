"""Sub-agents package.

Avoid eager imports here to prevent circular imports and to ensure
broken modules don't crash package import. Import sub-agents directly
from their modules where needed, e.g.

	from .topic_planner import topic_planner_agent
	from .game_generator import game_generator_agent
	from .validator import validator_agent
"""

__all__ = []