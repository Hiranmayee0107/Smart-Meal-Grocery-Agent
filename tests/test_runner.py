import tests.test_data as test_data
from agents.meal_planner import MealPlannerAgent
from agents.pantry_checker import PantryCheckerAgent
from agents.grocery_optimizer import GroceryOptimizerAgent
from evaluator import evaluate_plan

def run_test():
    print("\n=== Running Test Version (using tests/test_data.py) ===\n")

    planner = MealPlannerAgent(test_data.RECIPES_SAMPLE)
    pantry_agent = PantryCheckerAgent(test_data.PANTRY_SAMPLE)
    optimizer = GroceryOptimizerAgent()

    # Generate plan
    plan, trace_planner = planner.generate_plan(test_data.USER_PROFILE, {})

    # Pantry
    inventory, trace_pantry = pantry_agent.read_inventory()

    # Grocery optimizer
    aggregated = optimizer.aggregate_ingredients(plan)
    missing = optimizer.compute_missing(aggregated, inventory)
    shopping_list = optimizer.build_shopping_list(missing)

    # Evaluation
    eval_result = evaluate_plan(plan, shopping_list, inventory, test_data.USER_PROFILE, 1, 0.5)

    # Output
    print("Generated 7-Day Test Meal Plan:\n", plan)
    print("\nMissing Items:\n", missing)
    print("\nShopping List:\n", shopping_list)
    print("\nEvaluator Score:\n", eval_result)

if __name__ == "__main__":
    run_test()
