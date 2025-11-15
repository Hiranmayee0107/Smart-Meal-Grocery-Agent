# 1. USER PROFILE

USER_PROFILE = {
    "user_id": "demo_user_01",
    "servings": 2,                      # Number of people per meal
    "age_group": "adult",
    "dietary_constraints": ["vegetarian"],     # Can be "vegan", "keto", "lactose-free", etc.
    "allergies": ["peanuts"],                  # Example: user is allergic to peanuts
    "forbidden": ["pork", "tuna"],             # User will NOT eat these
    "budget": 80,                               # Weekly grocery budget (more realistic)
    "goals": {
        "meal_variety": True,
        "prefer_quick_meals": True,
        "healthy_focus": True,
        "avoid_repetitive_ingredients": True
    },
    "preferred_cuisines": ["Indian", "Italian", "Asian"],
    "cooking_skill": "intermediate"             # Affects recipe complexity later
}

# 2. PANTRY SAMPLE

PANTRY_SAMPLE = {
    "items": [
        {"name": "eggs", "qty": 12, "unit": "pcs"},
        {"name": "onion", "qty": 5, "unit": "pcs"},
        {"name": "milk", "qty": 1000, "unit": "ml"},
        {"name": "rice", "qty": 2000, "unit": "g"},
        {"name": "spinach", "qty": 300, "unit": "g"},
        {"name": "tomato", "qty": 4, "unit": "pcs"},
        {"name": "potato", "qty": 3, "unit": "pcs"},
        {"name": "carrot", "qty": 3, "unit": "pcs"},
        {"name": "cheese", "qty": 150, "unit": "g"},
        {"name": "paneer", "qty": 200, "unit": "g"},
        {"name": "bread", "qty": 8, "unit": "slices"},
        {"name": "pasta", "qty": 400, "unit": "g"},
        {"name": "oats", "qty": 500, "unit": "g"},
        {"name": "yogurt", "qty": 250, "unit": "g"},
        {"name": "banana", "qty": 3, "unit": "pcs"},
        {"name": "olive oil", "qty": 200, "unit": "ml"},
        {"name": "salt", "qty": 500, "unit": "g"},
        {"name": "pepper", "qty": 50, "unit": "g"}
    ]
}


# 3. RECIPES_SAMPLE

RECIPES_SAMPLE = [
    {
        "recipe_id": "v1",
        "title": "Vegetable Stir Fry",
        "ingredients": [
            {"name": "onion", "qty": 1, "unit": "pcs"},
            {"name": "spinach", "qty": 100, "unit": "g"},
            {"name": "rice", "qty": 150, "unit": "g"}
        ],
        "category": "vegetarian"
    },
    {
        "recipe_id": "v2",
        "title": "Simple Omelette",
        "ingredients": [
            {"name": "eggs", "qty": 2, "unit": "pcs"},
            {"name": "milk", "qty": 30, "unit": "ml"}
        ],
        "category": "vegetarian"
    },
    {
        "recipe_id": "v3",
        "title": "Spinach Rice Bowl",
        "ingredients": [
            {"name": "rice", "qty": 200, "unit": "g"},
            {"name": "spinach", "qty": 100, "unit": "g"}
        ],
        "category": "vegetarian"
    },
    {
        "recipe_id": "v4",
        "title": "Onion Soup",
        "ingredients": [
            {"name": "onion", "qty": 2, "unit": "pcs"},
            {"name": "milk", "qty": 100, "unit": "ml"}
        ],
        "category": "vegetarian"
    },
    {
        "recipe_id": "v5",
        "title": "Vegetable Fried Rice",
        "ingredients": [
            {"name": "rice", "qty": 180, "unit": "g"},
            {"name": "onion", "qty": 1, "unit": "pcs"},
            {"name": "spinach", "qty": 80, "unit": "g"}
        ],
        "category": "vegetarian"
    },
    {
        "recipe_id": "v6",
        "title": "Paneer Stir Fry",
        "ingredients": [
            {"name": "paneer", "qty": 150, "unit": "g"},
            {"name": "onion", "qty": 1, "unit": "pcs"}
        ],
        "category": "vegetarian"
    },
    {
        "recipe_id": "v7",
        "title": "Cheese Omelette",
        "ingredients": [
            {"name": "eggs", "qty": 2, "unit": "pcs"},
            {"name": "milk", "qty": 20, "unit": "ml"}
        ],
        "category": "vegetarian"
    },
    {
        "recipe_id": "v8",
        "title": "Spinach Omelette",
        "ingredients": [
            {"name": "eggs", "qty": 2, "unit": "pcs"},
            {"name": "spinach", "qty": 50, "unit": "g"}
        ],
        "category": "vegetarian"
    },
    {
        "recipe_id": "v9",
        "title": "Vegetable Soup",
        "ingredients": [
            {"name": "onion", "qty": 1, "unit": "pcs"},
            {"name": "spinach", "qty": 70, "unit": "g"},
            {"name": "milk", "qty": 50, "unit": "ml"}
        ],
        "category": "vegetarian"
    },
    {
        "recipe_id": "v10",
        "title": "Rice & Egg Bowl",
        "ingredients": [
            {"name": "rice", "qty": 150, "unit": "g"},
            {"name": "eggs", "qty": 1, "unit": "pcs"}
        ],
        "category": "vegetarian"
    },
    {
        "recipe_id": "v11",
        "title": "Spinach Pancake",
        "ingredients": [
            {"name": "spinach", "qty": 80, "unit": "g"},
            {"name": "milk", "qty": 50, "unit": "ml"}
        ],
        "category": "vegetarian"
    },
    {
        "recipe_id": "v12",
        "title": "Cheesy Rice",
        "ingredients": [
            {"name": "rice", "qty": 180, "unit": "g"},
            {"name": "milk", "qty": 40, "unit": "ml"}
        ],
        "category": "vegetarian"
    },
    {
        "recipe_id": "v13",
        "title": "Spinach Scramble",
        "ingredients": [
            {"name": "eggs", "qty": 2, "unit": "pcs"},
            {"name": "spinach", "qty": 60, "unit": "g"}
        ],
        "category": "vegetarian"
    },
    {
        "recipe_id": "v14",
        "title": "Vegetarian Curry",
        "ingredients": [
            {"name": "onion", "qty": 1, "unit": "pcs"},
            {"name": "spinach", "qty": 100, "unit": "g"}
        ],
        "category": "vegetarian"
    },
    {
        "recipe_id": "v15",
        "title": "Mushroom Rice Pilaf",
        "ingredients": [
            {"name": "rice", "qty": 200, "unit": "g"},
            {"name": "mushroom", "qty": 100, "unit": "g"}
        ],
        "category": "vegetarian"
    },



    {
        "recipe_id": "n1",
        "title": "Chicken Fried Rice",
        "ingredients": [
            {"name": "rice", "qty": 200, "unit": "g"},
            {"name": "chicken", "qty": 150, "unit": "g"},
            {"name": "onion", "qty": 1, "unit": "pcs"}
        ],
        "category": "non-vegetarian"
    },
    {
        "recipe_id": "n2",
        "title": "Chicken Omelette",
        "ingredients": [
            {"name": "eggs", "qty": 2, "unit": "pcs"},
            {"name": "chicken", "qty": 50, "unit": "g"}
        ],
        "category": "non-vegetarian"
    },
    {
        "recipe_id": "n3",
        "title": "Chicken Soup",
        "ingredients": [
            {"name": "chicken", "qty": 150, "unit": "g"},
            {"name": "onion", "qty": 1, "unit": "pcs"}
        ],
        "category": "non-vegetarian"
    },
    {
        "recipe_id": "n4",
        "title": "Chicken Spinach Rice",
        "ingredients": [
            {"name": "rice", "qty": 180, "unit": "g"},
            {"name": "spinach", "qty": 80, "unit": "g"},
            {"name": "chicken", "qty": 100, "unit": "g"}
        ],
        "category": "non-vegetarian"
    },
    {
        "recipe_id": "n5",
        "title": "Chicken Curry",
        "ingredients": [
            {"name": "chicken", "qty": 200, "unit": "g"},
            {"name": "onion", "qty": 1, "unit": "pcs"}
        ],
        "category": "non-vegetarian"
    },
    {
        "recipe_id": "n6",
        "title": "Egg & Chicken Rice",
        "ingredients": [
            {"name": "rice", "qty": 200, "unit": "g"},
            {"name": "eggs", "qty": 1, "unit": "pcs"},
            {"name": "chicken", "qty": 80, "unit": "g"}
        ],
        "category": "non-vegetarian"
    },
    {
        "recipe_id": "n7",
        "title": "Chicken Sandwich",
        "ingredients": [
            {"name": "chicken", "qty": 100, "unit": "g"},
            {"name": "onion", "qty": 1, "unit": "pcs"}
        ],
        "category": "non-vegetarian"
    },
    {
        "recipe_id": "n8",
        "title": "Chicken Omelette Wrap",
        "ingredients": [
            {"name": "eggs", "qty": 2, "unit": "pcs"},
            {"name": "chicken", "qty": 70, "unit": "g"}
        ],
        "category": "non-vegetarian"
    },
    {
        "recipe_id": "n9",
        "title": "Chicken & Rice Bowl",
        "ingredients": [
            {"name": "rice", "qty": 200, "unit": "g"},
            {"name": "chicken", "qty": 120, "unit": "g"}
        ],
        "category": "non-vegetarian"
    },
    {
        "recipe_id": "n10",
        "title": "Chicken Spinach Stir Fry",
        "ingredients": [
            {"name": "chicken", "qty": 120, "unit": "g"},
            {"name": "spinach", "qty": 80, "unit": "g"}
        ],
        "category": "non-vegetarian"
    },
    {
        "recipe_id": "n11",
        "title": "Garlic Chicken",
        "ingredients": [
            {"name": "chicken", "qty": 180, "unit": "g"},
            {"name": "onion", "qty": 1, "unit": "pcs"}
        ],
        "category": "non-vegetarian"
    },
    {
        "recipe_id": "n12",
        "title": "Egg Chicken Curry",
        "ingredients": [
            {"name": "chicken", "qty": 150, "unit": "g"},
            {"name": "eggs", "qty": 1, "unit": "pcs"}
        ],
        "category": "non-vegetarian"
    },
    {
        "recipe_id": "n13",
        "title": "Chicken Milk Soup",
        "ingredients": [
            {"name": "chicken", "qty": 150, "unit": "g"},
            {"name": "milk", "qty": 50, "unit": "ml"}
        ],
        "category": "non-vegetarian"
    },
    {
        "recipe_id": "n14",
        "title": "Chicken Rice Porridge",
        "ingredients": [
            {"name": "rice", "qty": 150, "unit": "g"},
            {"name": "chicken", "qty": 120, "unit": "g"}
        ],
        "category": "non-vegetarian"
    },
    {
        "recipe_id": "n15",
        "title": "Chicken Spinach Omelette",
        "ingredients": [
            {"name": "eggs", "qty": 2, "unit": "pcs"},
            {"name": "spinach", "qty": 60, "unit": "g"},
            {"name": "chicken", "qty": 70, "unit": "g"}
        ],
        "category": "non-vegetarian"
    }
]


# 4. Helper
def get_all_recipe_ids():
    """Return a list of all recipe IDs in the dataset."""
    return [r["recipe_id"] for r in RECIPES_SAMPLE]

# 5. Get recipe by ID

def get_recipe(recipe_id: str):
    """Retrieve a recipe by its ID."""
    for recipe in RECIPES_SAMPLE:
        if recipe["recipe_id"] == recipe_id:
            return recipe
    return None
