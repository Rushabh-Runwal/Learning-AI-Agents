from datetime import datetime

from google.genai import types


# ANSI color codes for terminal output
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"


def update_interaction_history(session_service, app_name, user_id, session_id, entry):
    """Add an entry to the interaction history in state.

    Args:
        session_service: The session service instance
        app_name: The application name
        user_id: The user ID
        session_id: The session ID
        entry: A dictionary containing the interaction data
            - requires 'action' key (e.g., 'user_query', 'agent_response')
            - other keys are flexible depending on the action type
    """
    try:
        # Get current session
        session = session_service.get_session(
            app_name=app_name, user_id=user_id, session_id=session_id
        )

        # Get current interaction history
        current_history = session.state.get("interaction_history", [])

        # Add timestamp to entry if not present
        if "timestamp" not in entry:
            entry["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Create new history list
        updated_history = current_history + [entry]

        # Create updated state
        updated_state = session.state.copy()
        updated_state["interaction_history"] = updated_history

        # Create a new session with updated state
        session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id,
            state=updated_state,
        )

        return True

    except Exception as e:
        print(f"Error updating interaction history: {e}")
        return False


def add_user_query_to_history(session_service, app_name, user_id, session_id, query):
    """Add a user query to the interaction history.

    Args:
        session_service: The session service instance
        app_name: The application name
        user_id: The user ID
        session_id: The session ID
        query: The user's query string
    """
    entry = {"action": "user_query", "query": query}

    return update_interaction_history(
        session_service, app_name, user_id, session_id, entry
    )


def add_agent_response_to_history(
    session_service, app_name, user_id, session_id, agent_name, response
):
    """Add an agent response to the interaction history.

    Args:
        session_service: The session service instance
        app_name: The application name
        user_id: The user ID
        session_id: The session ID
        agent_name: The name of the agent that responded
        response: The agent's response string
    """
    entry = {"action": "agent_response", "agent": agent_name, "response": response}

    return update_interaction_history(
        session_service, app_name, user_id, session_id, entry
    )


def add_tool_usage_to_history(
    session_service, app_name, user_id, session_id, tool_name, result
):
    """Add tool usage to the interaction history.

    Args:
        session_service: The session service instance
        app_name: The application name
        user_id: The user ID
        session_id: The session ID
        tool_name: The name of the tool that was used
        result: The result of the tool usage
    """
    entry = {"action": "tool_usage", "tool": tool_name, "result": str(result)}

    return update_interaction_history(
        session_service, app_name, user_id, session_id, entry
    )


def display_state(
    session_service, app_name, user_id, session_id, label="Current State"
):
    """Display the current session state in a formatted way."""
    try:
        session = session_service.get_session(
            app_name=app_name, user_id=user_id, session_id=session_id
        )

        print(f"\n{'-' * 10} {label} {'-' * 10}")

        # Handle user name
        user_name = session.state.get("user_name", "Unknown")
        print(f"👤 User: {user_name}")

        # Handle cart items
        cart_items = session.state.get("cart_items", [])
        if cart_items:
            print("🛒 Cart Items:")
            for item in cart_items:
                if isinstance(item, dict):
                    name = item.get("name", "Unknown")
                    quantity = item.get("quantity", 0)
                    price = item.get("price", 0)
                    print(f"  - {name} x{quantity} @ ${price:.2f}")
        else:
            print("🛒 Cart Items: Empty")

        # Handle total amount
        total_amount = session.state.get("total_amount", 0.0)
        print(f"💰 Total Amount: ${total_amount:.2f}")

        # Handle interaction history in a readable way
        interaction_history = session.state.get("interaction_history", [])
        if interaction_history:
            print("📝 Recent Interactions:")
            # Show only last 3 interactions to keep output manageable
            recent_interactions = interaction_history[-3:] if len(interaction_history) > 3 else interaction_history
            for idx, interaction in enumerate(recent_interactions, 1):
                if isinstance(interaction, dict):
                    action = interaction.get("action", "interaction")
                    timestamp = interaction.get("timestamp", "unknown time")

                    if action == "user_query":
                        query = interaction.get("query", "")
                        # Truncate long queries for display
                        if len(query) > 50:
                            query = query[:47] + "..."
                        print(f'  {idx}. User query: "{query}"')
                    elif action == "agent_response":
                        agent = interaction.get("agent", "unknown")
                        response = interaction.get("response", "")
                        # Truncate very long responses for display
                        if len(response) > 50:
                            response = response[:47] + "..."
                        print(f'  {idx}. {agent} response: "{response}"')
                    else:
                        print(f"  {idx}. {action}")
        else:
            print("📝 Interactions: None")

        print("-" * (22 + len(label)))
    except Exception as e:
        print(f"Error displaying state: {e}")


async def process_agent_response(event):
    """Process and display agent response events, filtering out non-text parts."""
    final_response = None
    
    # Check all parts for text content
    if event.content and event.content.parts:
        for part in event.content.parts:
            # Only process text parts, ignore non-text parts like 'thought_signature', 'function_call'
            if hasattr(part, "text") and part.text and not part.text.isspace():
                text_content = part.text.strip()
                
                # If this is a final response, format and display it properly
                if event.is_final_response():
                    final_response = text_content
                    # Display the final response with formatting
                    print(
                        f"\n{Colors.BG_BLUE}{Colors.WHITE}{Colors.BOLD}AGENT:{Colors.RESET}"
                    )
                    print(f"{Colors.CYAN}{Colors.BOLD}{final_response}{Colors.RESET}")

                    break
                else:
                    # For non-final responses, just print the text
                    print(f"  Text: '{text_content}'")

    # Handle case where final response has no text content
    if event.is_final_response() and not final_response:
        print(
            f"\n{Colors.BG_RED}{Colors.WHITE}{Colors.BOLD}==> Final Agent Response: [No text content in final event]{Colors.RESET}\n"
        )

    return final_response


async def call_agent_async(runner, user_id, session_id, query):
    """Call the agent asynchronously with the user's query, properly handling responses."""
    content = types.Content(role="user", parts=[types.Part(text=query)])
    final_response_text = None
    agent_name = None

    # Process the message

    try:
        async for event in runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content
        ):
            # Capture the agent name from the event if available
            if event.author:
                agent_name = event.author

            response = await process_agent_response(event)
            if response:
                final_response_text = response
    except Exception as e:
        print(f"{Colors.BG_RED}{Colors.WHITE}ERROR during agent run: {e}{Colors.RESET}")

    # Add the agent response to interaction history if we got a final response
    if final_response_text and agent_name:
        add_agent_response_to_history(
            runner.session_service,
            runner.app_name,
            user_id,
            session_id,
            agent_name,
            final_response_text,
        )

    # Processing completed
    return final_response_text


def format_cart_summary(cart_items):
    """Format cart items for display.
    
    Args:
        cart_items: List of cart items with {id, name, price, quantity}
    
    Returns:
        Formatted string representation of the cart
    """
    if not cart_items:
        return "Cart is empty"
    
    summary = "Cart Contents:\n"
    total = 0.0
    
    for item in cart_items:
        item_total = item.get("price", 0) * item.get("quantity", 0)
        total += item_total
        summary += f"- {item.get('name', 'Unknown')} x{item.get('quantity', 0)} @ ${item.get('price', 0):.2f} = ${item_total:.2f}\n"
    
    summary += f"\nTotal: ${total:.2f}"
    return summary


def calculate_cart_total(cart_items):
    """Calculate the total amount for items in cart.
    
    Args:
        cart_items: List of cart items with {id, name, price, quantity}
    
    Returns:
        Total amount as float
    """
    total = 0.0
    for item in cart_items:
        total += item.get("price", 0) * item.get("quantity", 0)
    return total


# Sample product catalog for the ecommerce store
PRODUCT_CATALOG = {
    "laptop_001": {
        "id": "laptop_001",
        "name": "Gaming Laptop",
        "price": 999.99,
        "category": "Electronics",
        "description": "High-performance gaming laptop",
        "stock": 10
    },
    "headphones_001": {
        "id": "headphones_001",
        "name": "Wireless Headphones",
        "price": 199.99,
        "category": "Electronics",
        "description": "Premium wireless headphones",
        "stock": 20
    },
    "mobile_001": {
        "id": "mobile_001",
        "name": "Smartphone",
        "price": 599.99,
        "category": "Electronics",
        "description": "Latest smartphone with advanced features",
        "stock": 15
    }
}


def get_product_by_id(product_id):
    """Get product details by ID.
    
    Args:
        product_id: The product ID to lookup
        
    Returns:
        Product dictionary or None if not found
    """
    return PRODUCT_CATALOG.get(product_id)


def get_products_by_category(category=None):
    """Get products filtered by category.
    
    Args:
        category: Category to filter by (optional)
        
    Returns:
        List of products matching the category
    """
    if not category:
        return list(PRODUCT_CATALOG.values())
    
    return [product for product in PRODUCT_CATALOG.values() 
            if product.get("category", "").lower() == category.lower()]


def search_products(search_term):
    """Search products by name or description.
    
    Args:
        search_term: Term to search for
        
    Returns:
        List of matching products
    """
    search_term = search_term.lower()
    matching_products = []
    
    for product in PRODUCT_CATALOG.values():
        if (search_term in product.get("name", "").lower() or 
            search_term in product.get("description", "").lower()):
            matching_products.append(product)
    
    return matching_products