# Run the backend

source .venv/bin/activate
uvicorn backend:app --reload

# simple backend test

curl -X POST http://localhost:8000/chat \
 -H "Content-Type: application/json" \
 -d '{"message": "Show me all your clothing products."}'
