import unittest
from unittest import mock

from work import Pool, Task, ExponentialPriority, WorkDone
from energoton.planner import Plan


class TestPlan(unittest.TestCase):
    def test_energy_spent(self):
        work = [WorkDone(None, mock.Mock(), 8, mock.Mock()) for _ in range(5)]
        plan = Plan(work)

        self.assertEqual(plan.energy_spent, 40)

    def test_value(self):
        tasks = (
            Task(5, priority=ExponentialPriority("lowest")),
            Task(5, priority=ExponentialPriority("low")),
            Task(5, priority=ExponentialPriority("normal")),
            Task(5, priority=ExponentialPriority("high")),
            Task(5, priority=ExponentialPriority("highest")),
        )

        work_done = [WorkDone(None, t, 5, mock.Mock()) for t in tasks]
        plan = Plan(work_done)

        self.assertEqual(plan.value, 31)

    def test_len(self):
        tasks = [Task(10) for _ in range(5)]
        plan1 = Plan(tasks)
        self.assertEqual(len(plan1), 5)

        pool = Pool(children=tasks)
        plan = Plan([pool])
        self.assertEqual(len(plan), 5)

        pool.add(Task(10, id_=6))
        self.assertEqual(len(plan), 6)
