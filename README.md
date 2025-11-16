# Smart-Meal-Grocery-Agent
A multi-agent system that generates a personalized 7-day meal plan, checks your pantry inventory, and produces an optimized grocery list that avoids duplicates and reduces food waste.

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

# Architecture Diagram

                    +---------------------+
                    |     Orchestrator    |
                    |       app.py        |
                    +---------------------+
                       /       |        \
                      v        v         v
         +----------------+ +-------------------+ +------------------------+
         | Meal Planner   | | Pantry Checker    | | Grocery Optimizer      |
         |     Agent      | |      Agent        | |        Agent           |
         +----------------+ +-------------------+ +------------------------+
                                 |
                                 v
                          +---------------+
                          |  Evaluator    |
                          +---------------+
                                 |
                                 v
                          +----------------+
                          | Output Writer  |
                          +----------------+


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
