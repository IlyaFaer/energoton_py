import unittest
from unittest import mock

from energoton import DeterministicEnergoton, NonDeterministicEnergoton
from energoton.planner import Planner
from work import Pool, Task, WorkDone
from work.priority import ExponentialPriority


class TestPlanner(unittest.TestCase):
    def test_ignore_task_order(self):
        pool = Pool()
        t1 = Task(5, id_="1")
        t2 = Task(2, id_="2")
        t3 = Task(4, id_="3")
        t4 = Task(2, id_="4")
        t5 = Task(6, id_="5")

        pool.add(t1)
        pool.add(t2)
        pool.add(t3)
        pool.add(t4)
        pool.add(t5)

        e = DeterministicEnergoton(8)

        planner = Planner([e], pool)
        planner.build_plans()
        plans = planner.filter_plans(ignore_task_order=True, sort_by=None)

        self.assertEqual(
            plans,
            (
                [WorkDone(None, t1, 5, e), WorkDone(None, t2, 2, e)],
                [WorkDone(None, t1, 5, e), WorkDone(None, t4, 2, e)],
                [
                    WorkDone(None, t2, 2, e),
                    WorkDone(None, t3, 4, e),
                    WorkDone(None, t4, 2, e),
                ],
                [WorkDone(None, t2, 2, e), WorkDone(None, t5, 6, e)],
                [WorkDone(None, t4, 2, e), WorkDone(None, t5, 6, e)],
            ),
        )

    def test_sort_by_length(self):
        pool = Pool()
        t1 = Task(5, id_="1")
        t2 = Task(2, id_="2")
        t3 = Task(4, id_="3")
        t4 = Task(2, id_="4")
        t5 = Task(6, id_="5")

        pool.add(t1)
        pool.add(t2)
        pool.add(t3)
        pool.add(t4)
        pool.add(t5)

        e = DeterministicEnergoton(8)

        planner = Planner([e], pool)
        planner.build_plans()
        plans = planner.filter_plans(ignore_task_order=True, sort_by="length")

        self.assertEqual(
            plans,
            (
                [
                    WorkDone(None, t2, 2, e),
                    WorkDone(None, t3, 4, e),
                    WorkDone(None, t4, 2, e),
                ],
                mock.ANY,
                mock.ANY,
                mock.ANY,
                mock.ANY,
            ),
        )

        plans = planner.filter_plans(
            ignore_task_order=True, sort_by="length", only_best=True
        )
        self.assertEqual(
            plans,
            (
                [
                    WorkDone(None, t2, 2, e),
                    WorkDone(None, t3, 4, e),
                    WorkDone(None, t4, 2, e),
                ],
            ),
        )

    def test_sort_by_value(self):
        pool = Pool()
        t1 = Task(
            5,
            id_=1,
            priority=ExponentialPriority("high"),
        )
        t2 = Task(
            2,
            id_=2,
            priority=ExponentialPriority("low"),
        )
        t3 = Task(
            4,
            id_=3,
            priority=ExponentialPriority("normal"),
        )
        t4 = Task(
            2,
            id_=4,
            priority=ExponentialPriority("highest"),
        )
        t5 = Task(
            6,
            id_=5,
            priority=ExponentialPriority("lowest"),
        )

        pool.add(t1)
        pool.add(t2)
        pool.add(t3)
        pool.add(t4)
        pool.add(t5)

        e = DeterministicEnergoton(8, name="energoton")

        planner = Planner([e], pool)
        planner.build_plans()
        plans = planner.filter_plans(ignore_task_order=True, sort_by="value")

        self.assertEqual(
            plans,
            (
                [WorkDone(None, t1, 5, e), WorkDone(None, t4, 2, e)],
                [
                    WorkDone(None, t2, 2, e),
                    WorkDone(None, t3, 4, e),
                    WorkDone(None, t4, 2, e),
                ],
                [WorkDone(None, t4, 2, e), WorkDone(None, t5, 6, e)],
                [WorkDone(None, t1, 5, e), WorkDone(None, t2, 2, e)],
                [WorkDone(None, t2, 2, e), WorkDone(None, t5, 6, e)],
            ),
        )

        plans = planner.filter_plans(
            ignore_task_order=True, sort_by="value", only_best=True
        )
        self.assertEqual(
            plans, ([WorkDone(None, t1, 5, e), WorkDone(None, t4, 2, e)],)
        )

    def test_sort_by_energy_spent(self):
        pool = Pool()
        t1 = Task(5, id_="1")
        t2 = Task(2, id_="2")
        t3 = Task(4, id_="3")
        t4 = Task(2, id_="4")
        t5 = Task(6, id_="5")

        pool.add(t1)
        pool.add(t2)
        pool.add(t3)
        pool.add(t4)
        pool.add(t5)

        e = DeterministicEnergoton(8)

        planner = Planner([e], pool)
        planner.build_plans()
        plans = planner.filter_plans(
            ignore_task_order=True, sort_by="energy_spent"
        )

        self.assertEqual(
            plans,
            (
                [
                    WorkDone(None, t2, 2, e),
                    WorkDone(None, t3, 4, e),
                    WorkDone(None, t4, 2, e),
                ],
                [WorkDone(None, t2, 2, e), WorkDone(None, t5, 6, e)],
                [WorkDone(None, t4, 2, e), WorkDone(None, t5, 6, e)],
                [WorkDone(None, t1, 5, e), WorkDone(None, t2, 2, e)],
                [WorkDone(None, t1, 5, e), WorkDone(None, t4, 2, e)],
            ),
        )

        plans = planner.filter_plans(
            ignore_task_order=True, sort_by="energy_spent", only_best=True
        )
        self.assertEqual(
            plans,
            (
                [
                    WorkDone(None, t2, 2, e),
                    WorkDone(None, t3, 4, e),
                    WorkDone(None, t4, 2, e),
                ],
                [WorkDone(None, t2, 2, e), WorkDone(None, t5, 6, e)],
                [WorkDone(None, t4, 2, e), WorkDone(None, t5, 6, e)],
            ),
        )

    def test_pool_after_plan(self):
        pool1 = Pool()
        t1 = Task(5, id_="1")
        t2 = Task(3, id_="2")
        pool1.add(t1)
        pool1.add(t2)

        root_pool = Pool()
        t3 = Task(4, id_="3")
        root_pool.add(t3)
        root_pool.add(pool1)

        e = NonDeterministicEnergoton(8)

        planner = Planner([e], root_pool)
        planner.build_plans()
        plans = planner.filter_plans(
            ignore_task_order=True, sort_by="length", only_best=True
        )

        result_pool = planner.pool_after_plan(plans[0])
        self.assertTrue(result_pool.children[t3.id].is_solved)
        self.assertFalse(result_pool.children[pool1.id].is_solved)

        self.assertEqual(
            result_pool.children[pool1.id].children[t1.id].spent, 1
        )

    def test_pool_two_energotons(self):
        pool1 = Pool()
        t1 = Task(5, id_="1")
        t2 = Task(3, id_="2")
        pool1.add(t1)
        pool1.add(t2)

        root_pool = Pool()
        t3 = Task(4, id_="3")
        root_pool.add(t3)
        root_pool.add(pool1)

        planner = Planner(
            [
                DeterministicEnergoton(8, id_="1"),
                DeterministicEnergoton(8, id_="2"),
            ],
            root_pool,
        )
        planner.build_plans()
        plans = planner.filter_plans(
            ignore_task_order=True, sort_by="length", only_best=True
        )

        for plan, result in zip(
            plans,
            (
                [("2", "1", 5), ("1", "2", 3), ("1", "3", 4)],
                [("1", "1", 5), ("1", "2", 3), ("2", "3", 4)],
            ),
        ):
            work_done = []
            for work in plan:
                work_done.append((work.assignee.id, work.task.id, work.amount))

            self.assertEqual(work_done, result)

    def test_several_cycles(self):
        pool = Pool()

        t1 = Task(5, id_="1")
        t2 = Task(2, id_="2")
        t3 = Task(4, id_="3")
        t4 = Task(2, id_="4")
        t5 = Task(6, id_="5")

        pool.add(t1)
        pool.add(t2)
        pool.add(t3)
        pool.add(t4)
        pool.add(t5)

        e = DeterministicEnergoton(8)

        planner = Planner([e], pool)
        planner.build_plans(cycles=2)
        plans = planner.filter_plans(ignore_task_order=True, sort_by=None)

        self.assertEqual(
            plans,
            (
                [
                    WorkDone(None, t1, 5, e, 1),
                    WorkDone(None, t2, 2, e, 1),
                    WorkDone(None, t3, 4, e, 2),
                    WorkDone(None, t4, 2, e, 2),
                ],
                [
                    WorkDone(None, t1, 5, e, 1),
                    WorkDone(None, t2, 2, e, 1),
                    WorkDone(None, t4, 2, e, 2),
                    WorkDone(None, t5, 6, e, 2),
                ],
                [
                    WorkDone(None, t2, 2, e, 1),
                    WorkDone(None, t3, 4, e, 1),
                    WorkDone(None, t4, 2, e, 1),
                    WorkDone(None, t5, 6, e, 2),
                ],
            ),
        )

    def test_by_cycles(self):
        pool = Pool()

        t1 = Task(5, id_="1")
        t2 = Task(2, id_="2")
        t3 = Task(4, id_="3")
        t4 = Task(2, id_="4")
        t5 = Task(6, id_="5")

        pool.add(t1)
        pool.add(t2)
        pool.add(t3)
        pool.add(t4)
        pool.add(t5)

        e = DeterministicEnergoton(8)

        planner = Planner([e], pool)
        planner.build_plans(cycles=2)
        plans = planner.filter_plans(ignore_task_order=True, sort_by=None)

        by_cycles = planner.by_cycles(plans)
        self.assertEqual(
            by_cycles,
            [
                {
                    1: [
                        WorkDone(None, t1, 5, e, 1),
                        WorkDone(None, t2, 2, e, 1),
                    ],
                    2: [
                        WorkDone(None, t3, 4, e, 2),
                        WorkDone(None, t4, 2, e, 2),
                    ],
                },
                {
                    1: [
                        WorkDone(None, t1, 5, e, 1),
                        WorkDone(None, t2, 2, e, 1),
                    ],
                    2: [
                        WorkDone(None, t4, 2, e, 2),
                        WorkDone(None, t5, 6, e, 2),
                    ],
                },
                {
                    1: [
                        WorkDone(None, t2, 2, e, 1),
                        WorkDone(None, t3, 4, e, 1),
                        WorkDone(None, t4, 2, e, 1),
                    ],
                    2: [WorkDone(None, t5, 6, e, 2)],
                },
            ],
        )

    def test_by_assignees(self):
        pool = Pool()

        t1 = Task(5, id_="1")
        t2 = Task(2, id_="2")
        t3 = Task(4, id_="3")
        t4 = Task(2, id_="4")
        t5 = Task(6, id_="5")

        pool.add(t1)
        pool.add(t2)
        pool.add(t3)
        pool.add(t4)
        pool.add(t5)

        e1 = DeterministicEnergoton(4, id_="1")
        e2 = DeterministicEnergoton(4, id_="2")

        planner = Planner([e1, e2], pool)
        planner.build_plans()
        plans = planner.filter_plans(ignore_task_order=True, sort_by=None)

        by_assignees = planner.by_assignees(plans)

        self.assertEqual(
            by_assignees,
            [
                {
                    "1": [
                        WorkDone(None, t2, 2, e1),
                        WorkDone(None, t4, 2, e1),
                    ],
                    "2": [WorkDone(None, t3, 4, e2)],
                },
                {
                    "2": [
                        WorkDone(None, t2, 2, e2),
                        WorkDone(None, t4, 2, e2),
                    ],
                    "1": [WorkDone(None, t3, 4, e1)],
                },
            ],
        )
