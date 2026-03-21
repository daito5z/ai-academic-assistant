def classify_query(query: str):

    query = query.lower()

    if any(word in query for word in ["email", "mail", "professor", "sent", "gmail"]):
        return "gmail"

    if any(word in query for word in ["pdf", "document", "paper", "notes"]):
        return "pdf"

    if any(word in query for word in ["previous", "earlier", "before"]):
        return "memory"

    return "all"
