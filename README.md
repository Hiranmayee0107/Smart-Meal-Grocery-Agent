# Smart-Meal-Grocery-Agent: A multi-agent system that generates a personalized 7-day meal plan, checks your pantry inventory, and produces an optimized grocery list that avoids duplicates and reduces food waste.

# Problem
Weekly meal planning and grocery list creation take 1–2 hours every week.
People often:
* Buy duplicate ingredients
* Forget to check pantry
* Waste food
* Repeat the same meals
* Get overwhelmed planning meals manually

# Solution
The Smart Meal & Grocery Agent is a multi-agent system that:
* Creates a 7-day meal plan based on dietary constraints
* Reads pantry inventory
* Uses ingredients you already have
* Generates a clean, optimized grocery list
* Minimizes waste and saves time

# Core Value
* Saves 1–2 hours per week
* Reduces food waste
* Personalized meal planning
* Consolidated, optimized shopping list
* respects allergies + restrictions

# Inputs
Embedded inside data.py:
* USER_PROFILE
* PANTRY_SAMPLE
* RECIPES_SAMPLE
No JSON uploads required.

# Outputs
Generated into /output/:
* meal_plan.json
* shopping_list.csv

# User Stories
https://github.com/Hiranmayee0107/Smart-Meal-Grocery-Agent/blob/main/user_stories.md

# Acceptance Criteria
https://github.com/Hiranmayee0107/Smart-Meal-Grocery-Agent/blob/main/Acceptance_criteria.md

## Agent Responsibilities

1. Meal Planner Agent
* Selects recipes
* Builds 7-day plan
* Applies dietary rules and forbidden foods

2. Pantry Checker Agent
* Normalizes pantry items
* Checks quantities
* Converts units
  
3. Grocery Optimizer Agent
* Aggregates ingredients
* Subtracts pantry
* Rounds to package sizes
* Builds final CSV list

4. Evaluator Agent
* Scores completeness, constraints, forbidden items, runtime
* Decides if loop continues

## Architecture Diagram 

# 1. Orchestrator(app.py)
# Role: Central Controller
1. This is the brain of the whole system.
2. It controls the sequence of operations.
3. It calls all other agents in order.
4. It also manages the evaluation loop until a satisfactory plan (score ≥ 0.9) is produced.

# Responsibilities:
1. Trigger Meal Planner
2. Trigger Pantry Checker
3. Trigger Grocery Optimizer
4. Send results to Evaluator
5. Check score and decide whether to stop or retry
6. Save final outputs
The Orchestrator ensures all agents work together smoothly.

# 2. Meal Planner Agent
# Role: Create the 7-day meal plan
1.Reads user profile (dietary constraints, forbidden foods, servings, etc.)
2. Selects valid recipes (vegetarian in your case)
3.Builds a 7-day structured meal plan
4. Ensures all meals follow restrictions

# Output:
A Python dictionary containing 7 days of meals and their ingredients.

# 3.Pantry Checker Agent
# Role: Normalize pantry data
1. Reads pantry items from data.py
2. Converts units into standard forms (kg → g, L → ml, etc.)
3. Cleans ingredient names (lowercase, trimmed)
4. Produces a normalized, machine-readable inventory

# Output:
A dictionary of pantry ingredients with cleaned quantities.

# 4. Grocery Optimizer Agent
# Role: Compute what the user needs to buy
1. This agent works in 3 steps:
Aggregate ingredients
Combine all ingredients from the weekly meal plan
(e.g., total onions needed = 1 + 2 + 1 = 4 onions)

Subtract pantry
Compare planned requirements with inventory
(if pantry has enough, it will NOT appear in the shopping list)

Optimize quantities
Rounds items to real-world package sizes
(e.g., if 130g spinach needed → chooses a 250g pack)

# Output:
A clean grocery list containing only what the user needs to buy.

# 5. Evaluator
# Role: Quality checking and scoring
It checks the solution based on 5 rules:
1. Completeness (all 7 days present)
2. No forbidden ingredients (pork/tuna)
3. Pantry usage score
4. Loop count ≤ 3
5. Runtime < 10 seconds
6. It returns:
a. score (0 to 1)
b. feedback messages
c. forbidden ingredient count
If score ≥ 0.9 → accept plan
Else → Orchestrator runs another loop.

# 6. Output Writer
# Role: Save final results
1. When a good solution is found:
a. Saves meal_plan.json
b. Saves shopping_list.csv
c. Saves traces.json for debugging/explainability
These files are stored inside the /output folder.
# Orchestrator Loop
Ensures multi-agent, sequential, loop-based architecture

# Project Structure
/project-root
    app.py
    data.py
    agents/
        meal_planner.py
        pantry_checker.py
        grocery_optimizer.py
    evaluator.py
    utils/
        conversions.py
        normalizer.py
    output/
    README.md

# How to Run
1. Run the orchestrator

python app.py

2. Outputs will appear in /output/:
* meal_plan.json
* shopping_list.csv

# Orchestrator Workflow
1. Generate 7-day meal plan (Meal Planner Agent)
2. Read pantry & normalize items (Pantry Checker Agent)
3. Compute missing ingredients & optimize (Grocery Optimizer Agent)
4. Score plan (Evaluator)
5. If score ≥ 0.9 → SAVE & STOP
6. Else → Loop again with feedback
