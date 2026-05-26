from datetime import datetime


def parse_date(date_string):

    if not date_string:
        return None

    formats = [
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%m/%d/%Y",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(
                date_string,
                fmt
            ).date()
        except:
            pass

    return None