"""
Unit Conversion Utilities

This module provides:
- normalize units
- convert qty + unit to a base unit
Used by PantryCheckerAgent and GroceryOptimizerAgent.
"""

def normalize_unit(unit: str) -> str:
    """
    Normalize raw units to canonical units.
    Supports g, kg -> g
    Supports ml, liter -> ml
    Supports pcs / piece
    """
    if not unit:
        return "pcs"

    u = unit.strip().lower()

    # weight
    if u in ("g", "gram", "grams"):
        return "g"
    if u in ("kg", "kilogram", "kilograms"):
        return "g"

    # volume
    if u in ("ml", "milliliter", "millilitre"):
        return "ml"
    if u in ("l", "liter", "litre"):
        return "ml"

    # pieces
    if u in ("pcs", "piece", "pieces", "count"):
        return "pcs"

    # fallback
    return u


def convert_to_base(qty: float, unit: str):
    """
    Convert unit to its base:
    - kg -> g
    - g  -> g
    - L  -> ml
    - ml -> ml
    - pcs stays pcs

    Returns:
        qty_norm, unit_norm
    """
    unit_norm = normalize_unit(unit)

    # weight conversions
    if unit_norm == "g":
        if unit.lower() == "kg":
            return qty * 1000, "g"
        return qty, "g"

    # volume conversions
    if unit_norm == "ml":
        if unit.lower() in ("l", "liter", "litre"):
            return qty * 1000, "ml"
        return qty, "ml"

    # piece count
    if unit_norm == "pcs":
        return qty, "pcs"

    # fallback (no conversion)
    return qty, unit_norm

