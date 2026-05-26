HEADER_MAPPINGS = {
    "Fuel Qty": "fuel_quantity",
    "Fuel_Quantity": "fuel_quantity",
    "Kraftstoffmenge": "fuel_quantity",

    "Werk": "plant_code",
    "Plant": "plant_code",

    "Datum": "date",
    "Date": "date",
}


def normalize_headers(row):
    normalized = {}

    for key, value in row.items():
        mapped_key = HEADER_MAPPINGS.get(key, key)
        normalized[mapped_key] = value

    return normalized