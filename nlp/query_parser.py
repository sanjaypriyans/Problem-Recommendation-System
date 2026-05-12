import re

# A simple query parser for difficulty and topic extraction
topics = {
    "array": "Array",
    "graph": "Graph",
    "dynamic programming": "Dynamic Programming",
    "dp": "Dynamic Programming",
    "tree": "Tree",
    "string": "String",
    "linked list": "Linked List",
}

difficulties = {
    "easy": "Easy",
    "medium": "Medium",
    "hard": "Hard",
}


def parse_query(query: str) -> dict:
    """Return a dictionary with detected topic and difficulty (if any).

    The function lowercases the query, strips punctuation, and checks if any of
    the known topics or difficulties are mentioned.  For a college project the
    logic is intentionally simple and rule-based.
    """
    normalized = re.sub(r"[^a-z0-9 ]+", " ", query.lower())
    tokens = normalized.split()

    detected = {"topic": None, "difficulty": None, "raw": query}

    # look for difficulties first
    for word, label in difficulties.items():
        if word in tokens:
            detected["difficulty"] = label
            break

    # look for topics by checking tokens or phrases
    for phrase, label in topics.items():
        if phrase in normalized:
            detected["topic"] = label
            break

    return detected
