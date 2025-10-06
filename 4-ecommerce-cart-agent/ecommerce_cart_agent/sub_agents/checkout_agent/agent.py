from datetime import datetime
import uuid
from typing import Optional

from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

# Import utility functions
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from utils import calculate_cart_total


def calculate_checkout_summary(tool_context: ToolContext) -> dict:
    """
    Calculate checkout summary including taxes and shipping.
    
    Returns:
        Dictionary with checkout breakdown
    """
    cart_items = tool_context.state.get("cart_items", [])
    
    if not cart_items:
        return {
            "status": "error",
            "message": "Cannot checkout with an empty cart."
        }
    
    subtotal = calculate_cart_total(cart_items)
    tax_rate = 0.08  # 8% tax
    tax_amount = subtotal * tax_rate
    
    # Free shipping over $50, otherwise $9.99
    shipping_cost = 0.0 if subtotal >= 50.0 else 9.99
    
    total_amount = subtotal + tax_amount + shipping_cost
    
    return {
        "status": "success",
        "message": "Checkout summary calculated",
        "summary": {
            "subtotal": subtotal,
            "tax_rate": tax_rate,
            "tax_amount": tax_amount,
            "shipping_cost": shipping_cost,
            "total_amount": total_amount,
            "free_shipping_eligible": subtotal >= 50.0
        },
        "cart_items": cart_items,
        "item_count": sum(item.get("quantity", 0) for item in cart_items)
    }


def process_checkout(tool_context: ToolContext) -> dict:
    """
    Process the checkout and create an order.
    Agent will specify payment method and address in conversation context.
    
    Returns:
        Dictionary with checkout status and available options
    """
    cart_items = tool_context.state.get("cart_items", [])
    
    if not cart_items:
        return {
            "status": "error",
            "message": "Cannot checkout with an empty cart."
        }
    
    # Calculate checkout summary
    summary_result = calculate_checkout_summary(tool_context)
    if summary_result["status"] != "success":
        return summary_result
    
    checkout_summary = summary_result["summary"]
    
    # Return checkout readiness status for agent to process
    return {
        "status": "ready_for_checkout",
        "message": "Ready to process checkout. Agent should specify payment method in conversation.",
        "checkout_summary": checkout_summary,
        "available_payment_methods": ["credit_card", "paypal", "apple_pay"],
        "instruction": "Agent should specify payment method and process order based on user selection"
    }
    
    # Add to order history
    current_orders = tool_context.state.get("order_history", [])
    current_orders.append(order)
    tool_context.state["order_history"] = current_orders
    
    # Clear the cart
    tool_context.state["cart_items"] = []
    tool_context.state["total_amount"] = 0.0
    
    # Add to interaction history
    current_history = tool_context.state.get("interaction_history", [])
    current_history.append({
        "action": "checkout_completed",
        "order_id": order_id,
        "total_amount": checkout_summary["total_amount"],
        "timestamp": order_date
    })
    tool_context.state["interaction_history"] = current_history
    
    return {
        "status": "success",
        "message": f"Order {order_id} has been successfully placed!",
        "order": order,
        "estimated_delivery": "3-5 business days"
    }


def view_order_history(tool_context: ToolContext) -> dict:
    """
    View the user's order history.
    
    Returns:
        Dictionary with order history
    """
    order_history = tool_context.state.get("order_history", [])
    
    if not order_history:
        return {
            "status": "empty",
            "message": "No previous orders found.",
            "orders": []
        }
    
    # Sort orders by date (newest first)
    sorted_orders = sorted(order_history, key=lambda x: x.get("order_date", ""), reverse=True)
    
    return {
        "status": "success",
        "message": f"Found {len(sorted_orders)} previous orders",
        "orders": sorted_orders,
        "total_orders": len(sorted_orders)
    }


def get_order_details(tool_context: ToolContext) -> dict:
    """
    Get detailed information about orders.
    Agent will specify which order in conversation context.
    
    Returns:
        Dictionary with all order details
    """
    order_history = tool_context.state.get("order_history", [])
    
    return {
        "status": "success",
        "message": f"Order history with {len(order_history)} orders",
        "order_history": order_history,
        "instruction": "Agent should select specific order based on user request"
    }



    discount_amount = 0
    
    if discount["type"] == "percentage":
        discount_amount = subtotal * discount["value"]
    elif discount["type"] == "fixed":
        discount_amount = min(discount["value"], subtotal)  # Don't exceed cart value
    
    # Store discount in state
    tool_context.state["applied_discount"] = {
        "code": discount_code.upper(),
        "type": discount["type"],
        "description": discount["description"],
        "discount_amount": discount_amount
    }
    
    return {
        "status": "success", 
        "message": f"Discount code '{discount_code}' applied successfully!",
        "discount": discount,
        "discount_amount": discount_amount,
        "original_subtotal": subtotal,
        "new_subtotal": max(0, subtotal - discount_amount)
    }


# Create the checkout agent
checkout_agent = Agent(
    name="checkout_agent",
    model="gemini-2.0-flash", 
    description="Checkout agent for processing orders and managing checkout flow",
    instruction="""
    You are the checkout agent for an ecommerce store.
    Your role is to help users complete their purchases, manage orders, and handle the checkout process.

    <user_info>
    Name: {user_name}
    </user_info>

    <cart_info>
    Cart Items: {cart_items}
    Total Amount: ${total_amount:.2f}
    </cart_info>

    <order_history>
    Order History: {order_history}
    </order_history>

    <interaction_history>
    {interaction_history}
    </interaction_history>

    **Your capabilities:**

    1. **Checkout Process**
       - Use calculate_checkout_summary() to show order breakdown with taxes and shipping
       - Use process_checkout() to complete orders - specify payment method in conversation
       - Handle payment methods: credit_card, paypal, apple_pay

    2. **Order Management**
       - Use view_order_history() to show past orders
       - Use get_order_details() to get order information - specify order_id in conversation

    **Checkout Rules:**
    - Free shipping on orders over $50
    - 8% tax applied to all orders
    - Standard shipping cost: $9.99
    - Estimated delivery: 3-5 business days

    **Guidelines:**
    - Always show order summary before processing checkout
    - Verify cart has items before attempting checkout
    - Confirm payment method details
    - Provide clear order confirmation with order ID
    - Handle errors gracefully with helpful messages

    **When users want to:**
    - Checkout: Show summary, confirm details, process order
    - View orders: Show organized order history with details

    **Payment Methods:**
    - credit_card
    - paypal
    - apple_pay

    Always ensure a smooth checkout experience and provide clear confirmation of successful orders.
    """,
    tools=[calculate_checkout_summary, process_checkout, view_order_history, get_order_details],
)