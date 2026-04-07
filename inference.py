import os
import requests
from openai import OpenAI

# Environment variables
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")

# OpenAI client
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

ENV_BASE_URL = "http://127.0.0.1:7860"
ALLOWED_ACTIONS = ["read_logs", "fix_bug", "write_feature", "refactor_code"]

def safe_request(method, url, **kwargs):
    try:
        res = requests.request(method, url, timeout=5, **kwargs)
        res.raise_for_status()
        # Some endpoints may return non-JSON, but OpenEnv should return JSON
        return res.json(), None
    except Exception as e:
        return None, str(e)

def get_action_from_llm():
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a developer agent."},
                {"role": "user", "content": "Choose one action: read_logs, fix_bug, write_feature, refactor_code. Reply with only the action."}
            ]
        )

        action = response.choices[0].message.content.strip().lower()
        if action not in ALLOWED_ACTIONS:
            return "fix_bug"
        return action
    except Exception:
        return "fix_bug"

def main():
    steps = 0
    rewards = []
    success = False
    last_error = None

    print(f"[START] task=dev-debug env=openenv model={MODEL_NAME}")

    try:
        # Reset environment
        _, err = safe_request("POST", f"{ENV_BASE_URL}/reset")
        if err:
            last_error = err
            print(f"[STEP] step=1 action=reset reward=0.00 done=false error={err}")
            return

        done = False

        while not done and steps < 10:
            action = get_action_from_llm()

            data, err = safe_request(
                "POST",
                f"{ENV_BASE_URL}/step",
                json={"action": action}
            )

            if err:
                last_error = err
                print(f"[STEP] step={steps + 1} action={action} reward=0.00 done=false error={err}")
                return

            reward = float(data.get("reward", 0))
            done = bool(data.get("done", False))

            rewards.append(reward)

            print(
                f"[STEP] step={steps + 1} action={action} "
                f"reward={reward:.2f} done={str(done).lower()} error=null"
            )

            steps += 1

        success = done

    except Exception as e:
        last_error = str(e)
        print(f"[STEP] step={steps + 1} action=error reward=0.00 done=true error={str(e)}")
        success = False

    finally:
        rewards_str = ",".join(f"{r:.2f}" for r in rewards)
        print(f"[END] success={str(success).lower()} steps={steps} rewards={rewards_str}")

if __name__ == "__main__":
    main()
