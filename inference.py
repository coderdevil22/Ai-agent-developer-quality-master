import os
import requests
from openai import OpenAI

# 🔥 ENV VARIABLES
LLM_BASE_URL = os.environ.get("API_BASE_URL", "https://api.openai.com/v1")
API_KEY = os.environ.get("API_KEY")             # provided by hackathon
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-4o-mini")

# 🔥 YOUR ENV SERVER (OpenEnv)
ENV_BASE_URL = "http://127.0.0.1:7860"

if not LLM_BASE_URL:
    raise ValueError("API_BASE_URL is required")

if not API_KEY:
    raise ValueError("API_KEY is required")

# 🔥 OpenAI Client (MANDATORY for proxy usage)
client = OpenAI(
    base_url=LLM_BASE_URL,
    api_key=API_KEY
)

def safe_request(method, url, **kwargs):
    try:
        res = requests.request(method, url, timeout=5, **kwargs)
        res.raise_for_status()
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

        if action not in ["read_logs", "fix_bug", "write_feature", "refactor_code"]:
            return "fix_bug"

        return action

    except Exception:
        return "fix_bug"

def main():
    steps = 0
    rewards_list = []
    success = False

    print(f"[START] task=dev-debug env=openenv model={MODEL_NAME}")

    try:
        # ✅ RESET (OpenEnv API)
        state, err = safe_request("POST", f"{ENV_BASE_URL}/reset")
        if err:
            print(f"[STEP] step=0 action=reset reward=0.00 done=false error={err}")
            return

        done = False

        while not done and steps < 10:
            # 🔥 LLM decides action
            action = get_action_from_llm()

            # ✅ STEP (OpenEnv API)
            data, err = safe_request(
                "POST",
                f"{ENV_BASE_URL}/step",
                json={"action": action}
            )

            if err:
                print(f"[STEP] step={steps} action={action} reward=0.00 done=false error={err}")
                success = False
                break

            reward = float(data.get("reward", 0))
            done = data.get("done", False)

            rewards_list.append(f"{reward:.2f}")

            print(
                f"[STEP] step={steps} action={action} "
                f"reward={reward:.2f} done={str(done).lower()} error=null"
            )

            steps += 1

        success = True

    except Exception as e:
        print(f"[STEP] step={steps} action=error reward=0.00 done=true error={str(e)}")
        success = False

    finally:
        rewards_str = ",".join(rewards_list)
        print(f"[END] success={str(success).lower()} steps={steps} rewards={rewards_str}")

if __name__ == "__main__":
    main()
