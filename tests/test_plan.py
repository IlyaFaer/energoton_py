import unittest

from work import Pool, Task, ExponentialPriority
from energoton.planner import Plan


class TestPlan(unittest.TestCase):
    def test_energy_spent(self):
        tasks = [Task(cost=8) for _ in range(5)]
        plan = Plan(tasks)

        self.assertEqual(plan.energy_spent, 0)

        for t in tasks:
            t.spent = 5

        self.assertEqual(plan.energy_spent, 25)

    def test_value(self):
        tasks = [
            Task(5, priority=ExponentialPriority("lowest")),
            Task(5, priority=ExponentialPriority("low")),
            Task(5, priority=ExponentialPriority("normal")),
            Task(5, priority=ExponentialPriority("high")),
            Task(5, priority=ExponentialPriority("highest")),
        ]
        plan = Plan(tasks)

        self.assertEqual(plan.value, 31)

    def test_len(self):
        tasks = [Task(10) for _ in range(5)]
        plan1 = Plan(tasks)
        self.assertEqual(len(plan1), 5)

        pool = Pool(children=tasks)
        plan = Plan([pool])
        self.assertEqual(len(plan), 5)

        pool.add(Task(10, id_=6, name="Task 6"))
        self.assertEqual(len(plan), 6)
