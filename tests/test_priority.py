import unittest

from task.priority import custom_priority
from task.task import Task


class TestPriority(unittest.TestCase):
    def test_custom_priority(self):
        priority_values = {
            "Lowest": 1,
            "Low": 2,
            "Medium": 3,
            "High": 4,
            "Highest": 5,
        }

        CustomPriority = custom_priority(priority_values)

        priority = CustomPriority("Medium")

        self.assertEqual(priority.label, "Medium")
        self.assertEqual(priority.value, priority_values["Medium"])
