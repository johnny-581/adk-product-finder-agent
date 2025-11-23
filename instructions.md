Build a lightweight AI-driven Category Finder Agent capable of reading a product dataset and returning category-based product recommendations through a simple UI.

The goal is to demonstrate your ability to structure data, define clear agent boundaries, and implement fully deterministic product retrieval without using embeddings, RAG, or multi-agent orchestration.

Instructions:
Use the provided JSON dataset (linked below).
Design and implement a simple agent using Google’s ADK that can:
Load and interpret the dataset
Understand user requests for product categories
Return category-filtered results deterministically
Build a simple chatbot-style UI of your choice (any web framework is allowed) that interacts with your ADK agent.

Examples of Supported Questions

USER-INPUT: “Show me all your clothing products.”

AGENT-OUTPUT: "Here are all the clothing products we have:"
UBC Hoodie, T-Shirt, Denim Jacket, Running Shoes as Product Cards with their name, description, price, and image.

USER-INPUT: “What clothing items are available under $50?”
AGENT-BEHAVIOUR: The agent should apply both category filtering and price filtering, then return product cards.

NOTE: You may use any frontend or backend web framework you prefer for the UI. However, the agent logic itself must be implemented using Google’s ADK. No fancy UI needed.

Attempt what’s feasible within 3-5 hours and be ready to present with a simple walk through. Feel free to use ChatGPT if needed, but you must be able to explain your code.

**Goal:**
Build a simple backend (no frontend) using Google ADK + FastAPI that returns products filtered by **derived categories** and **price**.

1. **Data loader**

   - Load `products.json` on startup.
   - Add a deterministic `category` field using simple keyword rules (e.g., hoodie/jacket/shirt → "clothing"; macbook/laptop → "electronics"; else "other").
   - Four categories: clothing, electronics, food, other.

2. **Filtering function**

   - Implement `filter_products(category=None, min_price=None, max_price=None)` that filters the global `PRODUCTS` list.

3. **ADK root agent** (`agent.py`)

   - Single agent.
   - Parse user requests for:

     - category (“clothing”, “electronics”, “other”)
     - price constraints (“under $X”, “over $X”, “between X and Y”, "equals to X").

   - Must call only the provided `filter_products` action.
   - Must not invent products.
   - Output a short explanation + list of matching products.

4. **Backend** (`backend.py`)

   - Use FastAPI.
   - Set up ADK `InMemorySessionService` + `Runner`.
   - Implement `POST /chat` that:

     - Accepts `{ "message": "..." }`.
     - Runs the agent with `runner.run_async(...)`.
     - Returns `{ "reply": "<agent text>" }`.
