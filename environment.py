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

        # reduce time
        self.state_data["deadline"] -= 1

        # Action 1: Read logs
        if action == "read_logs":
            if len(self.state_data["logs"]) > 0:
                reward = 0.5
            else:
                reward = -0.2

        # Action 2: Fix bug
        elif action == "fix_bug":
            if self.state_data["bugs"] > 0:
                self.state_data["bugs"] -= 1

                if len(self.state_data["logs"]) > 0:
                    self.state_data["logs"].pop(0)
                    reward = 1
                else:
                    reward = 0.3
            else:
                reward = -0.5

        # Action 3: Write feature
        elif action == "write_feature":
            self.state_data["features"] += 1
            self.state_data["bugs"] += 1
            reward = 1

        # Action 4: Refactor code
        elif action == "refactor_code":
            self.state_data["code_quality"] += 10
            reward = 0.5

        # Action 5: Do nothing
        else:
            reward = -1

        # done condition
        done = self.state_data["deadline"] <= 0

        return self.state_data, reward, done

    def state(self):
        return self.state_data