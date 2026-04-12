def grade_easy(state):
    # reward for reducing bugs
    score = 1 - (state["bugs"] / 5)
    return max(0.1, min(0.9, score))


def grade_medium(state):
    score = 0

    # features progress
    score += min(state["features"] * 0.2, 0.4)

    # bugs penalty
    score += max(0, (2 - state["bugs"]) * 0.2)

    return max(0.1, min(0.9, score))


def grade_hard(state):
    score = 0

    if state["features"] >= 2:
        score += 0.3

    if state["bugs"] <= 1:
        score += 0.3

    if state["code_quality"] >= 70:
        score += 0.3

    return max(0.1, min(0.9, score))
