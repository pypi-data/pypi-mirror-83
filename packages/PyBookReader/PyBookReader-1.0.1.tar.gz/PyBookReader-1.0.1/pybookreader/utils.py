def truncate_long_text(text, limit=50):
    if len(text) > limit:
        return text[:limit] + "..."
    return text
