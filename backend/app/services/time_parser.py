from datetime import datetime, timedelta


def parse_time_range(query: str):

    query = query.lower()
    now = datetime.utcnow()

    # Today
    if "today" in query:
        start = now
        end = now.replace(hour=23, minute=59, second=59)

    # Tomorrow
    elif "tomorrow" in query:
        tomorrow = now + timedelta(days=1)
        start = tomorrow.replace(hour=0, minute=0, second=0)
        end = tomorrow.replace(hour=23, minute=59, second=59)

    # This week
    elif "week" in query:
        start = now
        end = now + timedelta(days=7)

    # Default (next 3 days)
    else:
        start = now
        end = now + timedelta(days=3)

    return start.isoformat() + "Z", end.isoformat() + "Z"
