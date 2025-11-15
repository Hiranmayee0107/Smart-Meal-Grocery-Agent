AC1: The system must generate a complete 7-day meal plan (7 breakfast/lunch/dinner or 7 meals depending on design).
AC2: Every recommended recipe must respect the user’s dietary constraints (e.g., vegetarian).
AC3: The meal plan must exclude any allergens listed in USER_PROFILE.
AC4: No single recipe may repeat more than once unless variety=False.
AC5: Meal plan generation must complete within 3 iterations of the planner loop.
AC6: The agent must adjust ingredient quantities automatically based on the servings value.
AC7: At least 40% of planned meals must use ≥1 pantry ingredient.
AC8: Pantry quantities must decrease when used (internal update or simulated).
AC9: The agent must list missing ingredients for each recipe.
AC10: If an ingredient exists in pantry, the system must NOT add it to the grocery list.
AC11: The grocery list must include only missing ingredients.
AC12: Quantities must be merged correctly across all 7 days (e.g., onions 1 + 2 + 1 = 4).
AC13: Ingredient quantities must be converted to consistent units (g/ml/pcs).
AC14: Final list must be exported as a CSV file.
AC15: The agent must assign a meal plan quality score between 0.0 and 1.0.
AC16: If score < threshold (default 0.8), the planner must re-run automatically.
AC17: The agent must explain major reasons for a low evaluation score.
AC18: The system must generate a human-readable JSON file for the meal plan.
AC19: All outputs must be created inside an /outputs folder.
AC20: The system must produce at least one log entry per agent (planner, pantry checker, optimizer).
