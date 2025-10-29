from datetime import datetime
from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

# Import utilities
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from utils import get_product_by_id, calculate_cart_total


def add_item_to_cart(tool_context: ToolContext, product_id: str, quantity: int) -> dict:
    """Add an item to the shopping cart."""
    product = get_product_by_id(product_id)
    if not product:
        return {"status": "error", "message": f"Product '{product_id}' not found."}
    
    if quantity <= 0:
        return {"status": "error", "message": "Quantity must be greater than 0."}
    
    if quantity > product.get("stock", 0):
        return {"status": "error", "message": f"Only {product.get('stock', 0)} items available."}
    
    current_cart = tool_context.state.get("cart_items", [])
    new_cart = []
    item_exists = False
    
    for item in current_cart:
        if item.get("id") == product_id:
            new_quantity = item.get("quantity", 0) + quantity
            if new_quantity > product.get("stock", 0):
                return {"status": "error", "message": "Not enough stock available."}
            new_cart.append({
                "id": product_id,
                "name": product["name"],
                "price": product["price"],
                "quantity": new_quantity
            })
            item_exists = True
        else:
            new_cart.append(item)
    
    if not item_exists:
        new_cart.append({
            "id": product_id,
            "name": product["name"],
            "price": product["price"],
            "quantity": quantity
        })
    
    tool_context.state["cart_items"] = new_cart
    tool_context.state["total_amount"] = calculate_cart_total(new_cart)
    
    return {
        "status": "success",
        "message": f"Added {quantity} x {product['name']} to cart."
    }


def remove_item_from_cart(tool_context: ToolContext, product_id: str) -> dict:
    """Remove an item from the shopping cart."""
    current_cart = tool_context.state.get("cart_items", [])
    new_cart = []
    removed_item = None
    
    for item in current_cart:
        if item.get("id") == product_id:
            removed_item = item
        else:
            new_cart.append(item)
    
    if not removed_item:
        return {"status": "error", "message": f"Product '{product_id}' not found in cart."}
    
    tool_context.state["cart_items"] = new_cart
    tool_context.state["total_amount"] = calculate_cart_total(new_cart)
    
    return {
        "status": "success",
        "message": f"Removed {removed_item['name']} from cart."
    }


def view_cart(tool_context: ToolContext) -> dict:
    """View the current shopping cart contents."""
    cart_items = tool_context.state.get("cart_items", [])
    total_amount = tool_context.state.get("total_amount", 0.0)
    
    if not cart_items:
        return {"status": "empty", "message": "Your cart is empty.", "cart_items": [], "total_amount": 0.0}
    
    item_count = sum(item.get("quantity", 0) for item in cart_items)
    return {
        "status": "success",
        "message": f"Your cart contains {item_count} items.",
        "cart_items": cart_items,
        "total_amount": total_amount
    }


def clear_cart(tool_context: ToolContext) -> dict:
    """Clear all items from the shopping cart."""
    tool_context.state["cart_items"] = []
    tool_context.state["total_amount"] = 0.0
    return {"status": "success", "message": "Cart has been cleared."}


# Create the cart manager agent
cart_manager_agent = Agent(
    name="cart_manager",
    model="gemini-2.0-flash",
    description="Cart management agent for adding, removing, and viewing cart items",
    instruction="""You are the cart management agent for an ecommerce store.

Available Products:
- laptop_001: Gaming Laptop ($999.99)
- headphones_001: Wireless Headphones ($199.99) 
- mobile_001: Smartphone ($599.99)

Your tools:
- add_item_to_cart(product_id, quantity): Add items to cart
- remove_item_from_cart(product_id): Remove items from cart
- view_cart(): Show cart contents
- clear_cart(): Empty the cart

Product ID Mapping:
- laptop → laptop_001
- headphones → headphones_001  
- mobile/phone → mobile_001

Be helpful and validate all operations.""",
    tools=[add_item_to_cart, remove_item_from_cart, view_cart, clear_cart],
)
