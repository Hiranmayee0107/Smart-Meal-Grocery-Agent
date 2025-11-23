"""
Meal Planner Agent

Responsibilities:
- Generate a 7-day meal plan using RECIPES_SAMPLE (from data.py)
- Respect dietary_constraints
- Avoid forbidden ingredients
- Output plan structure exactly as required by orchestrator
"""

from typing import Dict, Any, List
from copy import deepcopy
from utils.normalizer import normalize_name


class MealPlannerAgent:
    """Simple rule-based meal planner."""

    def __init__(self, recipes: List[Dict[str, Any]]):
        self.recipes = recipes

    def generate_plan(self, user_profile: Dict[str, Any], context: Dict[str, Any]):
        """
        Generates a 7-day dinner-only meal plan.
        Output shape:

        {
          "user_id": "...",
          "week_start": "...",
          "plan": [
              {
                   "day": "Mon",
                   "meals": [
                       {
                         "type": "dinner",
                         "recipe_id": 1,
                         "title": "Spinach Rice",
                         "servings": 2,
                         "ingredients": [...]
                       }
                   ]
              },
              ...
          ]
        }
        """

        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        forbidden = set(normalize_name(x) for x in user_profile.get("forbidden", []))
        diet = set(normalize_name(x) for x in user_profile.get("dietary_constraints", []))
        servings = user_profile.get("servings", 2)

        # -------------------------------
        # 1. Filter recipes by rules
        # -------------------------------
        candidates = []

        for recipe in self.recipes:
            category = normalize_name(recipe.get("category", ""))

            # forbidden check
            ing_names = {normalize_name(i["name"]) for i in recipe.get("ingredients", [])}
            if ing_names & forbidden:
                continue

            # dietary constraint check
            if diet and category not in diet:
                # allow vegetarian ↔ veg
                if not ("vegetarian" in diet and category == "vegetarian"):
                    continue

            candidates.append(recipe)

        # fallback if filtering removed everything
        if not candidates:
            candidates = self.recipes

        # ------------------------------
        # 2. Build final 7-day plan
        # ------------------------------
        plan = {
            "user_id": user_profile.get("user_id"),
            "week_start": context.get("week_start"),
            "plan": []
        }

        idx = 0
        for day in days:
            selected = candidates[idx % len(candidates)]
            idx += 1

            plan["plan"].append({
                "day": day,
                "meals": [
                    {
                        "type": "dinner",
                        "recipe_id": selected["recipe_id"],
                        "title": selected["title"],
                        "servings": servings,
                        "ingredients": deepcopy(selected["ingredients"])
                    }
                ]
            })

        trace = {
            "agent": "MealPlanner",
            "generated_days": len(plan["plan"])
        }

        return plan, trace
