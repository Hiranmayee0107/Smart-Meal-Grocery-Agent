# tests/test_data.py

USER_PROFILE = {
    "diet": "vegetarian",
    "forbidden": ["pork", "tuna"],
    "servings": 2
}

PANTRY_SAMPLE = {
    "items": [
        {"name": "rice", "qty": 50, "unit": "g"},      # small quantity → triggers missing items
        {"name": "milk", "qty": 50, "unit": "ml"},
        {"name": "onion", "qty": 0, "unit": "pcs"}     # empty → missing
    ]
}

RECIPES_SAMPLE = [
    {
        "name": "Paneer Butter Masala",
        "ingredients": [
            {"ingredient": "paneer", "qty": 200, "unit": "g"},
            {"ingredient": "milk", "qty": 100, "unit": "ml"},
            {"ingredient": "onion", "qty": 1, "unit": "pcs"}
        ]
    },
    {
        "name": "Veg Fried Rice",
        "ingredients": [
            {"ingredient": "rice", "qty": 200, "unit": "g"},
            {"ingredient": "carrot", "qty": 1, "unit": "pcs"},
            {"ingredient": "beans", "qty": 50, "unit": "g"}
        ]
    }
]
