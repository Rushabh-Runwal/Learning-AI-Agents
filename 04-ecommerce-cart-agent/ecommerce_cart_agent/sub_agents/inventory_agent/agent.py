from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from typing import Optional

# Import the product catalog and utility functions
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from utils import PRODUCT_CATALOG, get_product_by_id, get_products_by_category, search_products


def view_available_products(tool_context: ToolContext) -> dict:
    """
    View all available products.
    
    Returns:
        Dictionary with list of available products
    """
    products = list(PRODUCT_CATALOG.values())
    
    # Filter out products with 0 stock
    available_products = [p for p in products if p.get("stock", 0) > 0]
    
    return {
        "status": "success",
        "message": f"Found {len(available_products)} available products",
        "products": available_products,
        "total_count": len(available_products)
    }


def get_product_details(tool_context: ToolContext) -> dict:
    """
    Get detailed information about a specific product.
    The agent will specify which product in the conversation context.
    
    Returns:
        Dictionary with all product details for the agent to choose from
    """
    # Since we can't get product_id as parameter, return all products
    # The agent will filter based on conversation context
    products = list(PRODUCT_CATALOG.values())
    
    return {
        "status": "success",
        "message": f"Found {len(products)} products in catalog",
        "products": products,
        "instruction": "Agent should select the specific product based on user request"
    }


def get_product_categories(tool_context: ToolContext) -> dict:
    """
    Get all available product categories.
    
    Returns:
        Dictionary with list of available categories
    """
    categories = set()
    for product in PRODUCT_CATALOG.values():
        category = product.get("category", "Uncategorized")
        categories.add(category)
    
    return {
        "status": "success",
        "message": f"Found {len(categories)} product categories",
        "categories": sorted(list(categories)),
        "total_count": len(categories)
    }


def check_product_availability(tool_context: ToolContext) -> dict:
    """
    Check availability of all products.
    The agent will specify which product in the conversation context.
    
    Returns:
        Dictionary with availability status for all products
    """
    # Return availability for all products, agent will filter based on context
    products_with_availability = []
    
    for product in PRODUCT_CATALOG.values():
        stock = product.get("stock", 0)
        available = stock > 0
        
        products_with_availability.append({
            "product": product,
            "available_stock": stock,
            "is_available": available,
            "status": "available" if available else "out_of_stock"
        })
    
    return {
        "status": "success",
        "message": f"Availability check for {len(products_with_availability)} products",
        "products_availability": products_with_availability,
        "instruction": "Agent should select the specific product based on user request"
    }



# Create the inventory agent
inventory_agent = Agent(
    name="inventory_agent", 
    model="gemini-2.0-flash",
    description="Inventory agent for browsing products and checking availability",
    instruction="""
    You are the inventory management agent for an ecommerce store.
    Your role is to help users browse products, search the catalog, and check availability.

    <user_info>
    Name: {user_name}
    </user_info>

    <interaction_history>
    {interaction_history}
    </interaction_history>

    **Your capabilities:**

    1. **Show Products**
       - Use view_available_products() to show all available products
       - Display product name, price, and stock information
       - Only show products that are in stock

    2. **Get Product Details**
       - Use get_product_details() to get detailed information about products
       - Shows all products with their specifications and pricing

    3. **Check Availability**
       - Use check_product_availability() to check stock availability for all products
       - Agent will filter and present information for specific products based on user requests

    4. **Browse Categories**
       - Use get_product_categories() to show available categories
       - Help users browse by product type

    **Product Information:**
    Our catalog includes:
    - Electronics (laptops, smartphones, headphones)
    - Books (programming guides, technical books)  
    - Clothing (t-shirts, apparel)
    - Food & Beverage (coffee, snacks)
    - Audio equipment and accessories

    **Available Products (use these exact product IDs):**
    - laptop_001: Gaming Laptop ($999.99)
    - headphones_001: Wireless Headphones ($199.99) 
    - coffee_001: Coffee Beans ($19.99)

    **Guidelines:**
    - Present product information clearly with prices and availability
    - Always use the exact product IDs: laptop_001, headphones_001, coffee_001
    - Provide accurate stock information before recommendations

    **When users want to:**
    - Browse: Show organized product listings with key details
    - Search: Help them find specific items or types of products
    - Learn more: Provide detailed product information
    - Check availability: Confirm stock before they try to add to cart

    Always be helpful in guiding users through the product catalog and make shopping easy and informative.
    """,
    tools=[view_available_products, get_product_categories, get_product_details, check_product_availability],
)