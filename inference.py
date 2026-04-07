import os
import requests
from openai import OpenAI

# ENV
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:7860")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN is required")

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

def safe_request(method, url, **kwargs):
    try:
        res = requests.request(method, url, timeout=5, **kwargs)
        res.raise_for_status()
        return res.json(), None
    except Exception as e:
        return None, str(e)

def main():
    steps = 0
    rewards_list = []
    success = False

    print(f"[START] task=dev-debug env=openenv model={MODEL_NAME}")

    try:
        # RESET
        state, err = safe_request("POST", f"{API_BASE_URL}/reset")
        if err:
            print(f"[STEP] step=0 action=reset reward=0.00 done=false error={err}")
            return

        done = False

        while not done and steps < 10:
            action = "fix_bug"

            data, err = safe_request(
                "POST",
                f"{API_BASE_URL}/step",
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

        # success only if no error
        if not err:
            success = True

    except Exception as e:
        print(f"[STEP] step={steps} action=error reward=0.00 done=true error={str(e)}")
        success = False

    finally:
        rewards_str = ",".join(rewards_list)
        print(f"[END] success={str(success).lower()} steps={steps} rewards={rewards_str}")

if __name__ == "__main__":
    main()
