import unittest
from unittest import mock

from energoton import DeterministicEnergoton, NonDeterministicEnergoton
from energoton.planner import Planner
from work import Alternative, Blocking, Pool, Task, WorkDone
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
