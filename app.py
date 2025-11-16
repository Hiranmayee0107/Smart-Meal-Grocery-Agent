"""
app.py — Orchestrator for Smart Meal & Grocery Agent (Phase 3 Step 9)

Responsibilities:
- Run Meal Planner, Pantry Checker, Grocery Optimizer in sequence
- Call Evaluator with the 5 rules:
    * score >= 0.9
    * completeness >= 0.98
    * forbidden_found == 0
    * average loops <= 3 (enforced via loop_count penalty)
    * runtime < 10s (penalty if exceeded)
- Persist outputs to /output/
- Emit traces/logs

This orchestrator uses simple rule-based agent implementations included below as minimal stubs.
Replace agents with more advanced implementations later in Phase 4.
"""

import time
import json
import csv
import os
from copy import deepcopy
from typing import Dict, Any, List

# import your embedded data
from data import USER_PROFILE, PANTRY_SAMPLE, RECIPES_SAMPLE, get_recipe

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------
# Simple helper utilities
# -------------------------
def normalize_name(name: str) -> str:
    return name.strip().lower()

def convert_to_base(qty: float, unit: str, name: str = None):
    """
    Minimal unit conversion for orchestrator use.
    For the prototype, handle pcs, g, ml, liter, kg.
    """
    unit = (unit or "").lower()
    if unit in ("g", "gram", "grams"): return qty, "g"
    if unit in ("kg",): return qty * 1000, "g"
    if unit in ("ml", "milliliter", "millilitre"): return qty, "ml"
    if unit in ("l", "liter", "litre"): return qty * 1000, "ml"
    if unit in ("pcs", "piece", "pieces", "count"): return qty, "pcs"
    # fallback: return raw
    return qty, unit or "pcs"

# -------------------------
# Simple Agents (stubs)
# -------------------------
class MealPlannerAgent:
    """Simple rule-based meal planner: round-robin select recipes respecting forbidden/diet"""
    def __init__(self, recipes: List[Dict[str,Any]]):
        self.recipes = recipes

    def generate_plan(self, user_profile: Dict[str,Any], context: Dict[str,Any]):
        # produce a 7-day dinner-only plan for simplicity
        days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        plan = {"user_id": user_profile.get("user_id"), "week_start": context.get("week_start"), "plan": []}
        # filter by dietary constraints & forbidden
        forbidden = set([normalize_name(x) for x in user_profile.get("forbidden", [])])
        diet = set([normalize_name(x) for x in user_profile.get("dietary_constraints", [])])
        candidates = []
        for r in self.recipes:
            cat = normalize_name(r.get("category",""))
            rid = r.get("recipe_id")
            # enforce forbidden check via ingredient names
            ing_names = set(normalize_name(i["name"]) for i in r.get("ingredients",[]))
            if ing_names & forbidden:
                continue
            # if dietary constraints present, require recipe category to match OR be neutral
            if diet and cat and not (cat in diet or cat == "vegetarian" and "vegetarian" in diet):
                continue
            candidates.append(r)
        if not candidates:
            # fallback to all recipes
            candidates = self.recipes

        ix = 0
        for d in days:
            r = candidates[ix % len(candidates)]
            servings = user_profile.get("servings", 2)
            plan["plan"].append({"day": d, "meals":[{"type":"dinner","recipe_id": r["recipe_id"], "title": r.get("title"), "servings": servings, "ingredients": deepcopy(r.get("ingredients",[]))}]})
            ix += 1

        trace = {"agent":"MealPlanner", "selected_count": len(plan["plan"])}
        return plan, trace

class PantryCheckerAgent:
    """Return normalized pantry inventory"""
    def __init__(self, pantry_data: Dict[str,Any]):
        self.pantry = pantry_data

    def read_inventory(self):
        inv = {}
        for item in self.pantry.get("items", []):
            name = normalize_name(item["name"])
            qty_norm, unit_norm = convert_to_base(item.get("qty",0), item.get("unit",""), name)
            inv[name] = {"qty": item.get("qty",0), "unit": item.get("unit",""), "qty_norm": qty_norm, "unit_norm": unit_norm}
        trace = {"agent":"PantryChecker", "items": len(inv)}
        return inv, trace

class GroceryOptimizerAgent:
    """Aggregate ingredients across plan, subtract pantry, and build shopping list"""
    PACKAGE_SIZES = {
        "eggs": {"pcs":[6,12]},
        "milk": {"ml":[500,1000]},
        "rice": {"g":[500,1000]},
        "spinach": {"g":[100,250]},
    }

    def aggregate_ingredients(self, plan: Dict[str,Any]):
        agg = {}
        for day in plan.get("plan", []):
            for meal in day.get("meals", []):
                for ing in meal.get("ingredients", []):
                    name = normalize_name(ing["name"])
                    qty = ing.get("qty", 1)
                    unit = ing.get("unit", "pcs")
                    qty_norm, unit_norm = convert_to_base(qty, unit, name)
                    key = name
                    if key not in agg:
                        agg[key] = {"qty_norm": 0.0, "unit_norm": unit_norm, "entries": []}
                    agg[key]["qty_norm"] += qty_norm
                    agg[key]["entries"].append({"qty": qty, "unit": unit})
        return agg

    def compute_missing(self, aggregated: Dict[str,Any], inventory: Dict[str,Any]):
        missing = {}
        for name, info in aggregated.items():
            have = inventory.get(name, {}).get("qty_norm", 0)
            need = max(0.0, info["qty_norm"] - have)
            if need > 0:
                missing[name] = {"need_norm": need, "unit_norm": info["unit_norm"]}
        return missing

    def round_to_package(self, name: str, need_norm: float, unit_norm: str):
        pkg = self.PACKAGE_SIZES.get(name)
        if not pkg:
            return need_norm, unit_norm
        # find matching unit list
        units = pkg.get(unit_norm) or next(iter(pkg.values()))
        for p in sorted(units):
            if p >= need_norm:
                return p, unit_norm
        # otherwise multiples
        largest = max(units)
        times = int((need_norm + largest - 1) // largest)
        return largest * times, unit_norm

    def build_shopping_list(self, missing: Dict[str,Any]):
        shopping = []
        for name, info in missing.items():
            qty, unit = self.round_to_package(name, info["need_norm"], info["unit_norm"])
            shopping.append({"ingredient": name, "qty": qty, "unit": unit})
        return shopping

# -------------------------
# Evaluator (as per Phase 2/Step 7 rules)
# -------------------------
def evaluate_plan(plan: Dict[str,Any], shopping_list: List[Dict[str,Any]], inventory: Dict[str,Any],
                  user_profile: Dict[str,Any], loop_count: int, runtime: float):
    """
    Returns dict: {score, completeness, forbidden_found, feedback}
    Implements the five evaluator criteria and a simple scoring rubric.
    """
    feedback = []
    # 1) completeness: fraction of meal slots filled (7 days * meals per day). Here we expect 7 dinners.
    expected_slots = 7
    actual_slots = len(plan.get("plan", []))
    completeness = actual_slots / expected_slots if expected_slots else 1.0

    # 2) forbidden ingredients
    forbidden_list = set(normalize_name(x) for x in user_profile.get("forbidden", []))
    forbidden_found = 0
    for day in plan.get("plan", []):
        for meal in day.get("meals", []):
            for ing in meal.get("ingredients", []):
                if normalize_name(ing.get("name","")) in forbidden_list:
                    forbidden_found += 1

    # 3) pantry usage fraction: fraction of aggregated ingredients that are at least partially in pantry
    optimizer = GroceryOptimizerAgent()
    aggregated = optimizer.aggregate_ingredients(plan)
    missing = optimizer.compute_missing(aggregated, inventory)
    total_agg_items = len(aggregated) if aggregated else 0
    used_from_pantry = (total_agg_items - len(missing)) if total_agg_items else 0
    pantry_usage = (used_from_pantry / total_agg_items) if total_agg_items else 1.0

    # base score 1.0, then apply penalties as described earlier
    score = 1.0
    if completeness < 0.98:
        score -= 0.3
        feedback.append(f"Low completeness: {completeness:.2f}")
    if forbidden_found > 0:
        feedback.append(f"Forbidden ingredients found: {forbidden_found}")
        return {"score": 0.0, "completeness": completeness, "forbidden_found": forbidden_found, "feedback": feedback}
    if pantry_usage < 0.4:
        score -= 0.1
        feedback.append(f"Low pantry usage: {pantry_usage:.2f}")
    if loop_count > 3:
        score -= 0.2
        feedback.append(f"High loop count: {loop_count}")
    if runtime > 10.0:
        score -= 0.3
        feedback.append(f"Slow runtime: {runtime:.2f}s")
    score = max(0.0, score)
    return {"score": score, "completeness": completeness, "forbidden_found": forbidden_found, "feedback": feedback}

# -------------------------
# Persistence helpers
# -------------------------
def save_meal_plan(plan: Dict[str,Any], filename: str):
    with open(filename, "w") as f:
        json.dump(plan, f, indent=2)

def save_shopping_csv(shopping: List[Dict[str,Any]], filename: str):
    fieldnames = ["ingredient","qty","unit"]
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in shopping:
            writer.writerow(item)

# -------------------------
# Orchestrator main
# -------------------------
def run_orchestrator(max_loops: int = 5, threshold: float = 0.9):
    context = {"week_start": time.strftime("%Y-%m-%d")}
    planner = MealPlannerAgent(RECIPES_SAMPLE)
    pantry_agent = PantryCheckerAgent(PANTRY_SAMPLE)
    optimizer = GroceryOptimizerAgent()

    best_result = None
    loop_count = 0
    start_total = time.time()
    traces = []

    while loop_count < max_loops:
        loop_count += 1
        loop_start = time.time()
        print(f"[Orchestrator] Loop {loop_count} starting...")

        # 1) plan
        plan, trace_planner = planner.generate_plan(USER_PROFILE, context)

        # 2) pantry
        inventory, trace_pantry = pantry_agent.read_inventory()

        # 3) aggregate & compute missing
        aggregated = optimizer.aggregate_ingredients(plan)
        missing = optimizer.compute_missing(aggregated, inventory)
        shopping = optimizer.build_shopping_list(missing)

        loop_runtime = time.time() - loop_start

        # 4) evaluate
        eval_res = evaluate_plan(plan, shopping, inventory, USER_PROFILE, loop_count, loop_runtime)
        traces.append({"loop": loop_count, "planner": trace_planner, "pantry": trace_pantry, "aggregated_count": len(aggregated), "missing_count": len(missing), "shopping_count": len(shopping), "eval": eval_res, "runtime": loop_runtime})

        print(f"[Orchestrator] Loop {loop_count} eval score: {eval_res['score']:.3f}, completeness: {eval_res['completeness']:.3f}, forbidden: {eval_res['forbidden_found']}, runtime: {loop_runtime:.2f}s")

        # keep best result for fallback
        if not best_result or eval_res["score"] > best_result["eval"]["score"]:
            best_result = {"plan": plan, "shopping": shopping, "eval": eval_res, "loop": loop_count}

        # check threshold
        if eval_res["score"] >= threshold:
            print(f"[Orchestrator] Threshold met (score {eval_res['score']:.3f}). Saving outputs.")
            save_meal_plan(plan, os.path.join(OUTPUT_DIR, "meal_plan.json"))
            save_shopping_csv(shopping, os.path.join(OUTPUT_DIR, "shopping_list.csv"))
            # save traces
            with open(os.path.join(OUTPUT_DIR, "traces.json"), "w") as f:
                json.dump(traces, f, indent=2)
            return {"status":"success","loops": loop_count, "plan": plan, "shopping": shopping, "eval": eval_res, "traces": traces}

        print("[Orchestrator] Threshold not met, applying simple feedback (none) and retrying...\n")
        # optional: modify context/constraints based on eval_res["feedback"] before next loop

    # if max loops exhausted, save best_result
    print("[Orchestrator] Max loops reached. Saving best available plan.")
    if best_result:
        save_meal_plan(best_result["plan"], os.path.join(OUTPUT_DIR, "meal_plan.json"))
        save_shopping_csv(best_result["shopping"], os.path.join(OUTPUT_DIR, "shopping_list.csv"))
        with open(os.path.join(OUTPUT_DIR, "traces.json"), "w") as f:
            json.dump(traces, f, indent=2)
        return {"status":"max_loops","loops": loop_count, "plan": best_result["plan"], "shopping": best_result["shopping"], "eval": best_result["eval"], "traces": traces}
    else:
        return {"status":"no_result","loops": loop_count, "traces": traces}


if __name__ == "__main__":
    res = run_orchestrator(max_loops=5, threshold=0.9)
    print("Orchestrator finished. Summary:")
    print(json.dumps({"status":res.get("status"), "loops": res.get("loops"), "score": res.get("eval", res.get('plan', {})).get("score") if res.get("eval") or res.get("plan") else None}, indent=2))
