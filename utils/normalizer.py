"""
Ingredient & Name Normalization Utilities

This module provides:
- normalize_name: clean ingredient names
- safe_compare: compare ingredients consistently
"""

import re

def normalize_name(name: str) -> str:
    """
    Normalize ingredient / recipe names.
    Removes:
        - extra spaces
        - hyphens / underscores
        - plural 's'
        - trailing dots
        - capitalization differences

    Examples:
        " Tomatoes "   -> "tomato"
        "ONIONS"       -> "onion"
        "rice-grain"   -> "rice grain"
        "EGGS."        -> "egg"
    """
    if not name:
        return ""

    n = name.strip().lower()

    # replace hyphens & underscores with space
    n = n.replace("-", " ").replace("_", " ")

    # remove trailing punctuation
    n = re.sub(r"[.,;:!?]*$", "", n)

    # collapse multiple spaces
    n = re.sub(r"\s+", " ", n).strip()

    # singularize (simple heuristic)
    if n.endswith("s") and len(n) > 3:
        n = n[:-1]

    return n


def safe_compare(a: str, b: str) -> bool:
    """
    Case-insensitive, punctuation-insensitive comparison.
    Uses normalize_name() internally.
    """
    return normalize_name(a) == normalize_name(b)
