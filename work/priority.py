class NoPriority:
    def __init__(self):
        self.label = "No Priority"
        self.value = 1


class ExponentialPriority:
    exp_values = {
        "lowest": 1,
        "low": 2,
        "normal": 4,
        "high": 8,
        "highest": 16,
    }

    def __init__(self, label):
        self.label = label
        self.value = self.exp_values[label]


def custom_priority(priority_values):
    class CustomPriority:
        values = priority_values

        def __init__(self, label):
            self.label = label
            self.value = self.values[label]

    return CustomPriority
