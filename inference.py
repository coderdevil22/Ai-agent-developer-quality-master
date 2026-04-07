import requests
import os
from grader import grade_easy, grade_medium, grade_hard

BASE = os.getenv("API_BASE_URL", "http://127.0.0.1:7860")

def safe_request(method, url, **kwargs):
    try:
        res = requests.request(method, url, timeout=5, **kwargs)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print("Request failed:", e)
        return None

# RESET
reset_data = safe_request("POST", BASE + "/reset")
if not reset_data:
    exit(1)

print("RESET:", reset_data)

actions = ["read_logs", "fix_bug", "fix_bug", "write_feature", "refactor_code"]

total_reward = 0
final_state = None

for action in actions:
    data = safe_request("POST", BASE + "/step", json={"action": action})
    
    if not data:
        exit(1)

    print(f"\nAction: {action}")
    print("State:", data["observation"])
    print("Reward:", data["reward"])

    total_reward += data["reward"]
    final_state = data["observation"]

    if data["done"]:
        break

# GRADING
if final_state:
    print("\n---- TASK SCORES ----")
    print("Easy:", grade_easy(final_state))
    print("Medium:", grade_medium(final_state))
    print("Hard:", grade_hard(final_state))

print("\nTOTAL REWARD:", total_reward)
