"""
app.py — Orchestrator for Smart Meal & Grocery Agent  
(Phase 3 — Step 9)

Responsibilities:
- Run Meal Planner → Pantry Checker → Grocery Optimizer
- Call Evaluator using the 5 rules:
    ✔ score >= 0.9
    ✔ completeness >= 98%
    ✔ forbidden ingredients == 0
    ✔ average loops <= 3
    ✔ runtime < 10 seconds
- Save outputs to /output/
- Maintain traces/logs for explainability
"""

import time
import json
import csv
import os

# Import embedded data
from data import USER_PROFILE, PANTRY_SAMPLE, RECIPES_SAMPLE

# Import Agents
from agents.meal_planner import MealPlannerAgent
from agents.pantry_checker import PantryCheckerAgent
from agents.grocery_optimizer import GroceryOptimizerAgent

# Import Evaluator
from evaluator import evaluate_plan

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# -----------------------------
# File Saving Helpers
# -----------------------------
def save_meal_plan(plan, filename):
    with open(filename, "w") as f:
        json.dump(plan, f, indent=2)


def save_shopping_csv(shopping_list, filename):
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["ingredient", "qty", "unit"])
        writer.writeheader()
        for item in shopping_list:
            writer.writerow(item)


# -----------------------------
# ORCHESTRATOR LOOP
# -----------------------------
def run_orchestrator(max_loops=5, threshold=0.9):

    context = {"week_start": time.strftime("%Y-%m-%d")}
    planner = MealPlannerAgent(RECIPES_SAMPLE)
    pantry_agent = PantryCheckerAgent(PANTRY_SAMPLE)
    optimizer = GroceryOptimizerAgent()

    loop_count = 0
    traces = []
    best_result = None

    while loop_count < max_loops:
        loop_count += 1
        loop_start = time.time()

        print(f"\n[Orchestrator] Loop {loop_count} starting...")

        # 1) Generate 7-day plan
        plan = planner.generate_plan(USER_PROFILE, context)

        # 2) Read and normalize pantry
        inventory = pantry_agent.read_inventory()

        # 3) Aggregate ingredients and calculate missing items
        aggregated = optimizer.aggregate_ingredients(plan)
        missing = optimizer.compute_missing(aggregated, inventory)
        shopping_list = optimizer.build_shopping_list(missing)

        loop_runtime = time.time() - loop_start

        # 4) Evaluate the plan
        eval_result = evaluate_plan(
            plan=plan,
            shopping_list=shopping_list,
            inventory=inventory,
            user_profile=USER_PROFILE,
            loop_count=loop_count,
            runtime=loop_runtime
        )

        print(f"[Orchestrator] Score: {eval_result['score']:.3f}, "
              f"Completeness: {eval_result['completeness']:.3f}, "
              f"Forbidden: {eval_result['forbidden_found']}, "
              f"Runtime: {loop_runtime:.2f}s")

        # Save trace
        traces.append({
            "loop": loop_count,
            "aggregated_count": len(aggregated),
            "missing_count": len(missing),
            "shopping_count": len(shopping_list),
            "eval": eval_result,
            "runtime": loop_runtime
        })

        # Track best result for fallback
        if best_result is None or eval_result["score"] > best_result["eval"]["score"]:
            best_result = {
                "plan": plan,
                "shopping": shopping_list,
                "eval": eval_result,
                "loop": loop_count
            }

        # Stop if threshold reached
        if eval_result["score"] >= threshold:
            print("[Orchestrator] Threshold reached. Saving output...")
            save_meal_plan(plan, os.path.join(OUTPUT_DIR, "meal_plan.json"))
            save_shopping_csv(shopping_list, os.path.join(OUTPUT_DIR, "shopping_list.csv"))

            with open(os.path.join(OUTPUT_DIR, "traces.json"), "w") as f:
                json.dump(traces, f, indent=2)

            return {
                "status": "success",
                "loops": loop_count,
                "eval": eval_result
            }

        print("[Orchestrator] Below threshold — retrying...\n")

    # If max loops hit → save best one
    print("[Orchestrator] Max loops reached. Saving best available plan...")

    save_meal_plan(best_result["plan"], os.path.join(OUTPUT_DIR, "meal_plan.json"))
    save_shopping_csv(best_result["shopping"], os.path.join(OUTPUT_DIR, "shopping_list.csv"))

    with open(os.path.join(OUTPUT_DIR, "traces.json"), "w") as f:
        json.dump(traces, f, indent=2)

    return {
        "status": "max_loops",
        "loops": loop_count,
        "eval": best_result["eval"]
    }


# -----------------------------
# MAIN EXECUTION
# -----------------------------
if __name__ == "__main__":
    result = run_orchestrator()
    print("\n=== ORCHESTRATOR FINISHED ===")
    print(json.dumps(result, indent=2))
