def detect_suspicious_record(data):

    reasons = []

    quantity = data.get("quantity", 0)

    if quantity < 0:
        reasons.append(
            "Negative quantity detected"
        )

    return {
        "suspicious": len(reasons) > 0,
        "reasons": reasons,
    }