import json
from pathlib import Path
from typing import List, Dict, Optional

# Global products list
PRODUCTS: List[Dict] = []


def filter_products(category: Optional[str] = None, min_price: Optional[float] = None, max_price: Optional[float] = None) -> List[Dict]:
    print(f"Filtering products for category: {category}, min_price: {min_price}, max_price: {max_price}")
    
    filtered = PRODUCTS.copy()
    
    # Filter by category
    if category is not None:
        category_lower = category.lower()
        filtered = [p for p in filtered if p.get("category", "").lower() == category_lower]
    
    # Filter by price
    if min_price is not None:
        filtered = [p for p in filtered if p.get("price") >= min_price]
    
    if max_price is not None:
        filtered = [p for p in filtered if p.get("price") <= max_price]
    
    return filtered


def assign_category(product: Dict) -> str:
    name = product.get("name", "").lower()
    description = product.get("description", "").lower()
    text = f"{name} {description}"
    
    # Clothing keywords
    clothing_keywords = ["hoodie", "jacket", "shirt", "t-shirt", "shoes", "running shoes", "denim"]
    if any(keyword in text for keyword in clothing_keywords):
        return "clothing"
    
    # Electronics keywords
    electronics_keywords = ["macbook", "laptop", "bluetooth", "headphones", "smartwatch", "usb", "hub", "watch"]
    if any(keyword in text for keyword in electronics_keywords):
        return "electronics"
    
    # Food keywords
    food_keywords = ["apples", "bread", "milk", "rice", "almond"]
    if any(keyword in text for keyword in food_keywords):
        return "food"
    
    # Default to other
    return "other"


def load_products(json_path: str = "data.json") -> List[Dict]:
    file_path = Path(json_path)
    if not file_path.exists():
        raise FileNotFoundError(f"Product data file not found: {json_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    # Add category field to each product
    for product in products:
        if "category" not in product:
            product["category"] = assign_category(product)
    
    return products


def initialize_products(json_path: str) -> None:
    global PRODUCTS
    PRODUCTS = load_products(json_path)
    print(f"Loaded {len(PRODUCTS)} products")