class DevEnv:
    def __init__(self):
        self.state_data = {}

    def reset(self):
        self.state_data = {
            "bugs": 3,
            "code_quality": 50,
            "features": 0,
            "deadline": 20,
            "logs": ["NullPointerError", "API Timeout"]
        }
        return self.state_data

    def step(self, action):
        reward = 0
        self.state_data["deadline"] -= 1

        if action == "read_logs":
            reward = 0.5

        elif action == "fix_bug":
            if self.state_data["bugs"] > 0:
                self.state_data["bugs"] -= 1
                reward = 1.0
                if self.state_data["logs"]:
                    self.state_data["logs"].pop(0)
            else:
                reward = -0.5

        elif action == "write_feature":
            self.state_data["features"] += 1
            self.state_data["bugs"] += 1
            reward = 1.0

        elif action == "refactor_code":
            self.state_data["code_quality"] += 10
            reward = 0.5

        else:
            reward = -1

        done = self.state_data["deadline"] <= 0

        return self.state_data, reward, done

    def state(self):
        return self.state_data
