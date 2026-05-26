from datetime import datetime


SUPPORTED_FORMATS = [
    "%Y-%m-%d",
    "%d/%m/%Y",
    "%m-%d-%Y",
]


def parse_date(date_str):
    for fmt in SUPPORTED_FORMATS:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue

    raise ValueError(f"Unsupported date format: {date_str}")