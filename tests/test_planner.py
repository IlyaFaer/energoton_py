import unittest
from unittest import mock

from energoton import DeterministicEnergoton, NonDeterministicEnergoton
from energoton.planner import Planner, Plan
from work import Pool, Priority, Task, WorkDone


class TestPlanner(unittest.TestCase):
    def test_sort_by_value(self):
        pool = Pool()
        t1 = Task(
            5,
            id_=1,
            priority=Priority("high"),
        )
        t2 = Task(
            2,
            id_=2,
            priority=Priority("low"),
        )
        t3 = Task(
            4,
            id_=3,
            priority=Priority("normal"),
        )
        t4 = Task(
            2,
            id_=4,
            priority=Priority("highest"),
        )
        t5 = Task(
            6,
            id_=5,
            priority=Priority("lowest"),
        )

        pool.add(t1)
        pool.add(t2)
        pool.add(t3)
        pool.add(t4)
        pool.add(t5)

        e = DeterministicEnergoton(8, name="energoton")

        planner = Planner(pool)
        plans = planner.build_plans([e])

        p = Plan([WorkDone(t1, 5, e), WorkDone(t4, 2, e)])
        p.commit()

        self.assertEqual(plans, (p,))

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

        planner = Planner(root_pool)
        plans = planner.build_plans([e])

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

        planner = Planner(root_pool)
        plans = planner.build_plans(
            [
                DeterministicEnergoton(8, id_="1"),
                DeterministicEnergoton(8, id_="2"),
            ]
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

        pool.add(t1)
        pool.add(t2)
        pool.add(t3)
        pool.add(t4)

        e = DeterministicEnergoton(8)

        planner = Planner(pool)
        plans = planner.build_plans([e], cycles=2)

        p = Plan(
            [
                WorkDone(t1, 5, e, 2),
                WorkDone(t2, 2, e, 1),
                WorkDone(t3, 4, e, 1),
                WorkDone(t4, 2, e, 1),
            ]
        )
        p.commit()

        self.assertEqual(plans, (p,))

    def test_by_cycles(self):
        pool = Pool()

        t1 = Task(5, id_="1")
        t2 = Task(2, id_="2")
        t3 = Task(4, id_="3")

        pool.add(t1)
        pool.add(t2)
        pool.add(t3)

        e = DeterministicEnergoton(8)

        planner = Planner(pool)
        plans = planner.build_plans([e], cycles=2)

        by_cycles = planner.by_cycles(plans)
        self.assertEqual(
            by_cycles,
            [
                {
                    1: [
                        WorkDone(t1, 5, e, 1),
                        WorkDone(t2, 2, e, 1),
                    ],
                    2: [
                        WorkDone(t3, 4, e, 2),
                    ],
                },
            ],
        )

    def test_by_assignees(self):
        pool = Pool()

        t1 = Task(2, id_="1")
        t2 = Task(4, id_="2")
        t3 = Task(2, id_="3")

        pool.add(t1)
        pool.add(t2)
        pool.add(t3)

        e1 = DeterministicEnergoton(4, id_="1")
        e2 = DeterministicEnergoton(4, id_="2")

        planner = Planner(pool)
        plans = planner.build_plans([e1, e2])

        by_assignees = planner.by_assignees(plans)

        self.assertEqual(
            by_assignees,
            [
                {
                    "1": [
                        WorkDone(t1, 2, e1),
                        WorkDone(t3, 2, e1),
                    ],
                    "2": [WorkDone(t2, 4, e2)],
                },
            ],
        )
