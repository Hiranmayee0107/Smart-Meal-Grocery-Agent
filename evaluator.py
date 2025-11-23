"""
evaluator.py — Evaluation Engine for Smart Meal & Grocery Agent
---------------------------------------------------------------

Implements the 5 official evaluator rules from Phase 2:

1. Evaluator score ≥ 0.9
2. Completeness ≥ 98%
3. Forbidden ingredients = 0
4. Average loops ≤ 3   (penalty if exceeded)
5. Runtime < 10 seconds (penalty if exceeded)

Returned object:
{
    "score": float,
    "completeness": float,
    "forbidden_found": int,
    "feedback": [list of reasons]
}
"""

from utils.normalizer import normalize_name
from agents.grocery_optimizer import GroceryOptimizerAgent


def evaluate_plan(
    plan,
    shopping_list,
    inventory,
    user_profile,
    loop_count: int,
    runtime: float
):
    """
    Evaluates a generated meal plan based on the 5 acceptance criteria.

    Parameters:
        plan: dict — 7-day meal plan
        shopping_list: list — optimized missing ingredients
        inventory: dict — pantry after normalization
        user_profile: dict
        loop_count: int — how many loops the orchestrator ran
        runtime: float — seconds per loop

    Returns:
        dict with score, completeness, forbidden_found, feedback
    """

    feedback = []

    # ------------------------------------------------------
    # 1️⃣ COMPLETENESS CHECK
    # ------------------------------------------------------
    expected_days = 7
    actual_days = len(plan.get("plan", []))
    completeness = actual_days / expected_days if expected_days else 1.0

    # penalty if < 0.98
    score = 1.0
    if completeness < 0.98:
        score -= 0.3
        feedback.append(f"Low completeness ({completeness:.2f}) — expected 7 days.")


    # ------------------------------------------------------
    # 2️⃣ FORBIDDEN INGREDIENT CHECK
    # ------------------------------------------------------
    forbidden_list = set(normalize_name(x) for x in user_profile.get("forbidden", []))
    forbidden_found = 0

    for day in plan.get("plan", []):
        for meal in day.get("meals", []):
            for ing in meal.get("ingredients", []):
                if normalize_name(ing.get("name", "")) in forbidden_list:
                    forbidden_found += 1

    if forbidden_found > 0:
        feedback.append(f"Forbidden ingredients detected: {forbidden_found}")
        # automatic fail
        return {
            "score": 0.0,
            "completeness": completeness,
            "forbidden_found": forbidden_found,
            "feedback": feedback
        }


    # ------------------------------------------------------
    # 3️⃣ PANTRY USAGE CHECK (>= 40% is good)
    # ------------------------------------------------------
    optimizer = GroceryOptimizerAgent()
    aggregated = optimizer.aggregate_ingredients(plan)
    missing = optimizer.compute_missing(aggregated, inventory)

    total_items = len(aggregated) if aggregated else 0
    used_from_pantry = (total_items - len(missing)) if total_items else 0

    pantry_usage = (used_from_pantry / total_items) if total_items else 1.0

    if pantry_usage < 0.4:
        score -= 0.1
        feedback.append(f"Low pantry usage ({pantry_usage:.2f}) — try using pantry more.")


    # ------------------------------------------------------
    # 4️⃣ LOOP EFFICIENCY CHECK (≤ 3 recommended)
    # ------------------------------------------------------
    if loop_count > 3:
        score -= 0.2
        feedback.append(f"High loop count ({loop_count}) — exceeds recommended ≤ 3.")


    # ------------------------------------------------------
    # 5️⃣ RUNTIME CHECK (< 10s recommended)
    # ------------------------------------------------------
    if runtime > 10.0:
        score -= 0.3
        feedback.append(f"Slow runtime ({runtime:.2f}s). Must be under 10 seconds.")


    # Final score clamp
    score = max(score, 0.0)

    return {
        "score": score,
        "completeness": completeness,
        "forbidden_found": forbidden_found,
        "feedback": feedback
    }
