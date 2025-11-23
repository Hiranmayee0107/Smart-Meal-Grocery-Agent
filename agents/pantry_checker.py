"""
Pantry Checker Agent

Responsibilities:
- Read pantry inventory from PANTRY_SAMPLE (embedded in data.py)
- Normalize ingredient names
- Convert all units to base units (g, ml, pcs)
- Return consistent pantry dictionary for the orchestrator
"""

from typing import Dict, Any
from utils.conversions import convert_to_base
from utils.normalizer import normalize_name


class PantryCheckerAgent:
    """Reads and normalizes pantry inventory."""

    def __init__(self, pantry_data: Dict[str, Any]):
        self.pantry_data = pantry_data

    def read_inventory(self):
        """
        Returns inventory in the shape:

        {
            "milk": {"qty": 500, "unit": "ml", "qty_norm": 500, "unit_norm": "ml"},
            "eggs": {"qty": 4, "unit": "pcs", "qty_norm": 4, "unit_norm": "pcs"},
            ...
        }
        """

        inventory = {}

        for item in self.pantry_data.get("items", []):
            name = normalize_name(item.get("name", ""))

            qty = item.get("qty", 0)
            unit = item.get("unit", "pcs")

            qty_norm, unit_norm = convert_to_base(qty, unit)

            inventory[name] = {
                "qty": qty,
                "unit": unit,
                "qty_norm": qty_norm,
                "unit_norm": unit_norm
            }

        trace = {
            "agent": "PantryChecker",
            "items": len(inventory)
        }

        return inventory, trace
