# Ecommerce Cart Agent - Stateful Multi-Agent System

📹 **[Watch Tutorial](https://youtube.com/shorts/9cNMWPo7rNM?si=xHMv135kl8-Yr4Uz)**

This example demonstrates a comprehensive ecommerce shopping cart system built with ADK (Agent Development Kit). It showcases how to create a stateful multi-agent system that manages the complete shopping experience from product browsing to order completion.

## What is this System?

The Ecommerce Cart Agent is a sophisticated multi-agent system that combines:

1. **Stateful Session Management**: Persists cart contents, user information, and shopping history
2. **Multi-Agent Architecture**: Specialized agents handle different aspects of the shopping experience
3. **Product Catalog Management**: In-memory product database with categories and inventory
4. **Complete Shopping Flow**: Browse → Add to Cart → Checkout → Order Management

## Key Features

✅ **Product Browsing**: Search and filter products by category  
✅ **Cart Management**: Add, remove, modify items with quantity tracking  
✅ **Inventory Tracking**: Real-time stock availability checking  
✅ **Checkout Process**: Tax calculation, shipping, discount codes  
✅ **Order History**: Complete order tracking and management  
✅ **Persistent State**: Cart and user data preserved across sessions  

## Project Structure

```
13-ecommerce-cart-agent/
│
├── ecommerce_cart_agent/           # Main agent package
│   ├── __init__.py                 # Package initialization
│   ├── agent.py                    # Root ecommerce cart agent
│   └── sub_agents/                 # Specialized shopping agents
│       ├── cart_manager/           # Cart operations (add/remove/view)
│       │   ├── __init__.py
│       │   └── agent.py
│       ├── inventory_agent/        # Product browsing and search
│       │   ├── __init__.py  
│       │   └── agent.py
│       └── checkout_agent/         # Order processing and history
│           ├── __init__.py
│           └── agent.py
│
├── main.py                         # Application entry point
├── utils.py                        # Helper functions and product catalog
└── README.md                       # This documentation
```

## Available Products

The system includes a sample product catalog with:

### Electronics
- **Gaming Laptop Pro** - $1,299.99 (15 in stock)
- **Smartphone X** - $899.99 (25 in stock)  
- **Wireless Headphones** - $199.99 (30 in stock)

### Books
- **Python Programming Guide** - $49.99 (100 in stock)

### Clothing  
- **Cotton T-Shirt** - $24.99 (50 in stock)

### Food & Beverage
- **Premium Coffee Beans** - $19.99 (75 in stock)

## Agent Architecture

### 1. Main Ecommerce Cart Agent
- **Role**: Central coordinator and user interface
- **Capabilities**: Understanding user intent, routing to specialists, providing shopping guidance
- **Responsibilities**: Welcome users, explain features, manage shopping flow

### 2. Inventory Agent  
- **Role**: Product catalog management
- **Tools**:
  - `view_available_products(category?)` - Browse products by category
  - `get_product_details(product_id)` - Get detailed product information
  - `search_products_by_name(search_term)` - Search products by name/description
  - `get_product_categories()` - List all available categories
  - `check_product_availability(product_id, quantity)` - Verify stock levels

### 3. Cart Manager Agent
- **Role**: Shopping cart operations
- **Tools**:
  - `add_item_to_cart(product_id, quantity)` - Add items with quantity validation
  - `remove_item_from_cart(product_id, quantity?)` - Remove items or reduce quantities  
  - `view_cart()` - Display current cart contents and totals
  - `clear_cart()` - Remove all items from cart

### 4. Checkout Agent
- **Role**: Order processing and management  
- **Tools**:
  - `calculate_checkout_summary()` - Show order breakdown with tax/shipping
  - `process_checkout(payment_method, shipping_address?)` - Complete the order
  - `view_order_history()` - Show past orders
  - `get_order_details(order_id)` - Get specific order information
  - `apply_discount_code(code)` - Apply promotional discounts

## State Management

The system maintains persistent state across interactions:

```python
initial_state = {
    "user_name": "John Doe",
    "cart_items": [],           # Current shopping cart
    "interaction_history": [],  # All user interactions
    "total_amount": 0.0,       # Current cart total
    "order_history": [],       # Completed orders
}
```

### Cart Item Structure
```python
cart_item = {
    "id": "laptop_001",
    "name": "Gaming Laptop Pro", 
    "price": 1299.99,
    "quantity": 1
}
```

### Order Structure  
```python
order = {
    "order_id": "ORD-A1B2C3D4",
    "order_date": "2024-01-15 14:30:00",
    "items": [...],           # Cart items at time of purchase
    "subtotal": 1299.99,
    "tax_amount": 104.00,
    "shipping_cost": 0.0,     # Free shipping over $50
    "total_amount": 1403.99,
    "payment_method": "credit_card",
    "status": "confirmed"
}
```

## Usage Examples

### 1. Browsing Products
```
You: "What products do you have?"
You: "Show me electronics under $1000"
You: "Search for headphones"  
You: "Tell me about laptop_001"
```

### 2. Managing Cart
```
You: "Add the gaming laptop to my cart"
You: "Add 2 coffee to cart" 
You: "Show my cart"
You: "Remove headphones from cart"
You: "Clear my cart"
```

### 3. Checkout Process
```
You: "I'm ready to checkout"
You: "Apply discount code WELCOME10"
You: "Process my order with PayPal"
You: "Show my order history"
```

## Pricing & Policies

- **Tax Rate**: 8% on all orders
- **Shipping**: FREE over $50, otherwise $9.99
- **Payment Methods**: Credit Card, PayPal, Apple Pay
- **Delivery Time**: 3-5 business days
- **Discount Codes**:
  - `WELCOME10` - 10% off your order
  - `SAVE20` - 20% off your order  
  - `FREESHIP` - Free shipping
  - `NEWUSER` - $15 off your order

## Getting Started

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Environment**:
   ```bash
   # Create .env file with your API keys
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

3. **Run the Application**:
   ```bash
   cd 13-ecommerce-cart-agent
   python main.py
   ```

4. **Start Shopping**:
   ```
   Welcome to the Ecommerce Shopping Cart!
   You can browse products, add items to cart, manage your cart, and checkout.
   Type 'exit' or 'quit' to end the session.

   You: What products do you have?
   ```

## Example Shopping Session

```bash
You: What products are available?
Agent: I'll show you our available products...

You: Add the gaming laptop to my cart
Agent: Added 1 x Gaming Laptop Pro to cart. ($1,299.99)

You: Also add 2 coffee
Agent: Added 2 x Premium Coffee Beans to cart. 

You: Show my cart
Agent: Cart Contents:
- Gaming Laptop Pro x1 @ $1,299.99 = $1,299.99  
- Premium Coffee Beans x2 @ $19.99 = $39.98
Total: $1,339.97

You: Apply discount code WELCOME10
Agent: Discount code 'WELCOME10' applied successfully! 10% off your order.

You: Checkout with credit card
Agent: Order ORD-A1B2C3D4 has been successfully placed!
```

## Advanced Features

### Dynamic Inventory Management
- Real-time stock checking prevents overselling
- Out-of-stock items are filtered from searches
- Quantity validation during cart operations

### Smart Routing
- Natural language understanding for user intent
- Automatic routing to appropriate specialist agents
- Context-aware suggestions and guidance

### Comprehensive Order Tracking
- Unique order IDs for each purchase
- Complete order history with details
- Status tracking and delivery estimates

## Customization

### Adding Products
Edit the `PRODUCT_CATALOG` in `utils.py`:

```python
PRODUCT_CATALOG["new_item_001"] = {
    "id": "new_item_001",
    "name": "Your Product Name",
    "price": 99.99,
    "category": "Your Category", 
    "description": "Product description",
    "stock": 25
}
```

### Modifying Pricing Rules
Update pricing logic in `checkout_agent.py`:
- Tax rates in `calculate_checkout_summary()`
- Shipping thresholds and costs
- Discount code values and types

### Extending Agent Capabilities
Add new tools to existing agents or create additional specialist agents for features like:
- Wishlist management
- Product reviews and ratings  
- Recommendation engine
- Customer support chat

## Learning Outcomes

This example demonstrates:
- **Multi-Agent Coordination**: How specialized agents work together
- **State Management**: Persistent data across user interactions
- **Tool Integration**: Complex business logic in agent tools
- **User Experience**: Natural language shopping interface
- **System Architecture**: Scalable agent-based design patterns

Perfect for learning how to build sophisticated, stateful applications with the Agent Development Kit!