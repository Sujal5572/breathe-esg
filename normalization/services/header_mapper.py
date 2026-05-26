def normalize_headers(row):

    mapped = {}

    for key, value in row.items():

        normalized_key = key.strip().lower()

        if normalized_key == "einheit":
            normalized_key = "unit"

        mapped[normalized_key] = value

    return mapped