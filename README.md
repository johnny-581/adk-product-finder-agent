# Run the backend

source .venv/bin/activate  
uvicorn backend:app --reload

# Simple Backend Test

curl -X POST http://localhost:8000/chat \
 -H "Content-Type: application/json" \
 -d '{"message": "Show me all your clothing products."}'

# Sample Interaction

USER-INPUT: “Show me all your clothing products.”

AGENT-OUTPUT: "Here are all the clothing products we have:"
UBC Hoodie, T-Shirt, Denim Jacket, Running Shoes as Product Cards with their name, description, price, and image.

USER-INPUT: “What clothing items are available under $50?”

AGENT-BEHAVIOUR: The agent should apply both category filtering and price filtering, then return product cards.
