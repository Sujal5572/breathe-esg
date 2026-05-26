UNIT_CONVERSIONS = {
    ("gallons", "liters"): 3.78541,
    ("mwh", "kwh"): 1000,
}


def normalize_unit(value, from_unit):
    if value is None or from_unit is None:
        return value, from_unit

    from_unit = from_unit.lower().strip()

    if from_unit == "gallons":
        return round(float(value) * 3.78541, 2), "liters"

    if from_unit == "mwh":
        return round(float(value) * 1000, 2), "kwh"

    return value, from_unit