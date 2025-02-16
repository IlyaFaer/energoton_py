class NoPriority:
    def __init__(self):
        self.label = "No Priority"
        self.value = 1


class ExponentialPriority:
    exp_values = {
        "Lowest": 1,
        "Low": 2,
        "Medium": 4,
        "High": 8,
        "Highest": 16,
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
