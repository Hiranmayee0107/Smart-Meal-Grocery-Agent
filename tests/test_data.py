USER_PROFILE = {
    "user_id": "test_user_01",
    "servings": 2,
    "dietary_constraints": ["vegetarian"],
    "allergies": [],
    "forbidden": [],
    "budget": 100,
    "goals": {
        "meal_variety": True,
        "prefer_quick_meals": True
    },
    "preferred_cuisines": ["Indian"],
    "cooking_skill": "beginner"
}

PANTRY_SAMPLE = {
    "items": [
        {"name": "rice", "qty": 100, "unit": "g"},
        {"name": "onion", "qty": 1, "unit": "pcs"}
    ]
}

RECIPES_SAMPLE = [
    {
        "recipe_id": "t1",
        "title": "Test Rice Dish",
        "ingredients": [
            {"name": "rice", "qty": 200, "unit": "g"},
            {"name": "onion", "qty": 1, "unit": "pcs"}
        ],
        "category": "vegetarian"
    },
    {
        "recipe_id": "t2",
        "title": "Test Spinach Dish",
        "ingredients": [
            {"name": "spinach", "qty": 100, "unit": "g"}
        ],
        "category": "vegetarian"
    }
]
