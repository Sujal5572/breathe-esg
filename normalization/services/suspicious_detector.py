def detect_suspicious_record(record):
    reasons = []

    quantity = record.get("quantity")

    if quantity is not None:
        try:
            quantity = float(quantity)

            if quantity <= 0:
                reasons.append("Quantity must be greater than zero")

            if quantity > 1000000:
                reasons.append("Unusually large quantity detected")

        except ValueError:
            reasons.append("Invalid quantity format")

    if not record.get("source_unit"):
        reasons.append("Missing source unit")

    return {
        "suspicious": len(reasons) > 0,
        "reasons": reasons,
    }