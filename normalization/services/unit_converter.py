def normalize_unit(quantity, unit):

    if quantity is None:
        quantity = 0

    quantity = float(quantity)

    if not unit:
        return quantity, "unknown"

    unit = unit.lower()

    conversions = {
        "liters": ("liters", 1),
        "l": ("liters", 1),
        "kg": ("kg", 1),
    }

    if unit in conversions:

        normalized_unit, multiplier = conversions[unit]

        return quantity * multiplier, normalized_unit

    return quantity, unit