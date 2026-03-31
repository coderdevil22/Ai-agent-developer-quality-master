def grade_easy(state):
    if state["bugs"] == 0:
        return 1.0
    return 0.0


def grade_medium(state):
    if state["features"] >= 2 and state["bugs"] <= 2:
        return 1.0
    elif state["features"] >= 1:
        return 0.5
    return 0.0


def grade_hard(state):
    score = 0

    if state["features"] >= 3:
        score += 0.3
    if state["bugs"] <= 1:
        score += 0.3
    if state["code_quality"] >= 70:
        score += 0.2
    if state["deadline"] > 0:
        score += 0.2

    return score