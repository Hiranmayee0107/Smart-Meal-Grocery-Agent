"""
Grocery Optimizer Agent

Responsibilities:
- Aggregate total required ingredients from the 7-day meal plan
- Convert all units to base units (g, ml, pcs)
- Subtract pantry quantities
- Round missing quantities to nearest package size
- Return optimized shopping list
"""

from typing import Dict, Any, List
from utils.conversions import convert_to_base
from utils.normalizer import normalize_name


class GroceryOptimizerAgent:
    """
    Aggregates ingredients, subtracts pantry, rounds to package sizes,
    and produces final shopping list.
    """

    # You can expand these later
    PACKAGE_SIZES = {
        "eggs": {"pcs": [6, 12]},
        "milk": {"ml": [500, 1000]},
        "rice": {"g": [500, 1000]},
        "spinach": {"g": [100, 250]},
    }

    # ----------------------------------------
    # Step 1: Aggregate all ingredients from meal plan
    # ----------------------------------------
    def aggregate_ingredients(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        aggregated = {}

        for day in plan.get("plan", []):
            for meal in day.get("meals", []):
                for ing in meal.get("ingredients", []):
                    name = normalize_name(ing["name"])
                    qty = ing.get("qty", 1)
                    unit = ing.get("unit", "pcs")

                    qty_norm, unit_norm = convert_to_base(qty, unit)

                    if name not in aggregated:
                        aggregated[name] = {
                            "qty_norm": 0.0,
                            "unit_norm": unit_norm,
                            "entries": []
                        }

                    aggregated[name]["qty_norm"] += qty_norm
                    aggregated[name]["entries"].append({"qty": qty, "unit": unit})

        return aggregated

    # ----------------------------------------
    # Step 2: Subtract pantry from aggregated
    # ----------------------------------------
    def compute_missing(self, aggregated: Dict[str, Any],
                        pantry: Dict[str, Any]) -> Dict[str, Any]:

        missing = {}

        for name, info in aggregated.items():
            have = pantry.get(name, {}).get("qty_norm", 0)
            need = max(0, info["qty_norm"] - have)

            if need > 0:
                missing[name] = {
                    "need_norm": need,
                    "unit_norm": info["unit_norm"]
                }

        return missing

    # ----------------------------------------
    # Step 3: Round missing quantities to nearest package size
    # ----------------------------------------
    def round_to_package(self, name: str, need_norm: float, unit_norm: str):
        pkg_data = self.PACKAGE_SIZES.get(name)

        if not pkg_data:
            # No known package size → buy exact quantity
            return need_norm, unit_norm

        size_list = pkg_data.get(unit_norm)
        if not size_list:
            # Unit mismatch → still return exact
            return need_norm, unit_norm

        size_list = sorted(size_list)

        # First package that fits the need
        for size in size_list:
            if size >= need_norm:
                return size, unit_norm

        # If need larger than all packages → pick multiples of the largest
        largest = size_list[-1]
        multiplier = (need_norm + largest - 1) // largest
        return int(multiplier * largest), unit_norm

    # ----------------------------------------
    # Step 4: Construct final shopping list
    # ----------------------------------------
    def build_shopping_list(self, missing: Dict[str, Any]) -> List[Dict[str, Any]]:
        shopping = []

        for name, info in missing.items():
            qty, unit = self.round_to_package(
                name,
                info["need_norm"],
                info["unit_norm"]
            )

            shopping.append({
                "ingredient": name,
                "qty": qty,
                "unit": unit
            })

        return shopping
