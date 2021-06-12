class TrainServer():
    def __init__(self, config):
        self.config = config
        self.progress = 0

    def start(self):
        pass

    def close(self):
        pass

    def get_status(self):
        self.progress += 10
        state = "IDLE"
        if self.progress > 10 and self.progress < 100:
            state = "RUNNING"
        if self.progress >= 100:
            state = "FINISHED"

        return {
            "task": "TrainServer",
            "progress": self.progress,
            "state": state,
            "aiTaskIdList": [
                "1623116143661",
                ""
            ]
        }


class AnomalyServer():
    def __init__(self, config):
        self.config = config
        self.progress = 0

    def start(self):
        pass

    def close(self):
        pass

    def get_status(self):
        self.progress += 10
        state = "IDLE"
        if self.progress > 10 and self.progress < 100:
            state = "RUNNING"
        if self.progress >= 100:
            state = "FINISHED"

        return {
            "task": "AnomalyServer",
            "progress": self.progress,
            "state": state
        }
