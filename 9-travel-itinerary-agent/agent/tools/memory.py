"""Memory tools for tracking user preferences and trip details."""

from datetime import datetime
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools import ToolContext


def memorize(key: str, value: str, tool_context: ToolContext):
    """
    Memorize pieces of information, one key-value pair at a time.
    
    Args:
        key: The label indexing the memory to store the value.
        value: The information to be stored.
        tool_context: The ADK tool context.
        
    Returns:
        A status message confirming storage.
    """
    tool_context.state[key] = value
    return {"status": f'Stored "{key}": "{value}"'}


def memorize_list(key: str, value: str, tool_context: ToolContext):
    """
    Memorize pieces of information by appending to a list.
    
    Args:
        key: The label indexing the memory list.
        value: The information to be added to the list.
        tool_context: The ADK tool context.
        
    Returns:
        A status message confirming addition.
    """
    if key not in tool_context.state:
        tool_context.state[key] = []
    if value not in tool_context.state[key]:
        tool_context.state[key].append(value)
    return {"status": f'Added "{value}" to "{key}"'}


def recall_memory(key: str, tool_context: ToolContext):
    """
    Retrieve stored memory by key.
    
    Args:
        key: The label of the memory to retrieve.
        tool_context: The ADK tool context.
        
    Returns:
        The stored value or a message indicating no memory found.
    """
    value = tool_context.state.get(key)
    if value is None:
        return {"result": "No memory found", "key": key}
    return {"result": value, "key": key}


def forget(key: str, tool_context: ToolContext):
    """
    Remove a memory from the session state.
    
    Args:
        key: The label of the memory to remove.
        tool_context: The ADK tool context.
        
    Returns:
        A status message confirming removal.
    """
    if key in tool_context.state:
        del tool_context.state[key]
        return {"status": f'Forgot "{key}"'}
    return {"status": f'"{key}" not found in memory'}


def initialize_memory(callback_context: CallbackContext):
    """
    Initialize session state with memory structure.
    Sets up the initial memory buckets for tracking user preferences and trip details.
    
    Args:
        callback_context: The ADK callback context.
    """
    state = callback_context.state
    
    # Only initialize once per session
    if "_memory_initialized" not in state:
        state["_memory_initialized"] = True
        state["_session_start_time"] = str(datetime.now())
        
        # User preferences
        state["user_preferences"] = {}
        state["interests"] = []
        state["budget_style"] = ""  # budget/mid-range/luxury
        state["travel_style"] = ""  # relaxed/moderate/fast-paced
        state["origin_city"] = ""
        
        # Trip details
        state["destinations_discussed"] = []
        state["flight_searches"] = []
        state["hotel_searches"] = []
        state["activities_viewed"] = []
        state["current_itinerary"] = {}
        
        print(f"\n✅ Memory initialized at {state['_session_start_time']}")

