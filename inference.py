import requests
from grader import grade_easy, grade_medium, grade_hard

BASE = "http://127.0.0.1:8000"

# RESET
res = requests.post(BASE + "/reset")

if res.status_code != 200:
    print("Error in RESET:", res.text)
    exit()

reset_data = res.json()
print("RESET:", reset_data)

# ACTIONS (smarter flow)
actions = [
    "read_logs",
    "fix_bug",
    "fix_bug",
    "fix_bug",     
    "refactor_code",
    "write_feature",
    "write_feature"
]

total_reward = 0
final_state = None

for action in actions:
    res = requests.post(BASE + "/step", json={"action": action})

    if res.status_code != 200:
        print("Error in STEP:", res.text)
        break

    data = res.json()

    print(f"\nAction: {action}")
    print("State:", data["observation"])
    print("Reward:", data["reward"])

    total_reward += data["reward"]
    final_state = data["observation"]

    if data["done"]:
        print("\nEpisode finished")
        break

# GRADING
if final_state:
    print("\n---- TASK SCORES ----")
    print("Easy:", grade_easy(final_state))
    print("Medium:", grade_medium(final_state))
    print("Hard:", grade_hard(final_state))

print("\nTOTAL REWARD:", total_reward)
