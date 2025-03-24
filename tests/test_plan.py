import unittest
from unittest import mock

from work import Task, Priority, WorkDone
from energoton.planner import Plan


class TestPlan(unittest.TestCase):
    def test_energy_spent(self):
        work = [WorkDone(None, mock.Mock(), 8, mock.Mock()) for _ in range(5)]
        plan = Plan(work)

        self.assertEqual(plan.energy_spent, 40)

    def test_value(self):
        tasks = (
            Task(5, priority=Priority("lowest")),
            Task(5, priority=Priority("low")),
            Task(5, priority=Priority("normal")),
            Task(5, priority=Priority("high")),
            Task(5, priority=Priority("highest")),
        )

        work_done = [WorkDone(None, t, 5, mock.Mock()) for t in tasks]
        plan = Plan(work_done)

        self.assertEqual(plan.value, 31)
