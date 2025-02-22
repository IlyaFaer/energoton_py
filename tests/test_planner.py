import unittest
from unittest import mock

from energoton import DeterministicEnergoton, NonDeterministicEnergoton
from energoton.planner import Planner
from work import Alternative, Blocking, Pool, Task
from work.priority import ExponentialPriority


class TestPlanner(unittest.TestCase):
    def test_ignore_task_order(self):
        pool = Pool(name="Pool")
        t1 = Task(5, id_=1, name="Task 1")
        t2 = Task(2, id_=2, name="Task 2")
        t3 = Task(4, id_=3, name="Task 3")
        t4 = Task(2, id_=4, name="Task 4")
        t5 = Task(6, id_=5, name="Task 5")

        pool.add(t1)
        pool.add(t2)
        pool.add(t3)
        pool.add(t4)
        pool.add(t5)

        e = DeterministicEnergoton(8, name="energoton")

        planner = Planner([e], pool)
        planner.build_plans()
        plans = planner.filter_plans(ignore_task_order=True, sort_by=None)

        self.assertEqual(
            plans,
            ([t1, t2], [t1, t4], [t2, t3, t4], [t2, t5], [t4, t5]),
        )

    def test_sort_by_length(self):
        pool = Pool(name="Pool")
        t1 = Task(5, id_=1, name="Task 1")
        t2 = Task(2, id_=2, name="Task 2")
        t3 = Task(4, id_=3, name="Task 3")
        t4 = Task(2, id_=4, name="Task 4")
        t5 = Task(6, id_=5, name="Task 5")

        pool.add(t1)
        pool.add(t2)
        pool.add(t3)
        pool.add(t4)
        pool.add(t5)

        e = DeterministicEnergoton(8, name="energoton")

        planner = Planner([e], pool)
        planner.build_plans()
        plans = planner.filter_plans(ignore_task_order=True, sort_by="length")

        self.assertEqual(
            plans,
            ([t2, t3, t4], mock.ANY, mock.ANY, mock.ANY, mock.ANY),
        )

        plans = planner.filter_plans(
            ignore_task_order=True, sort_by="length", only_best=True
        )
        self.assertEqual(plans, ([t2, t3, t4],))

    def test_sort_by_value(self):
        pool = Pool(name="Pool")
        t1 = Task(
            5,
            id_=1,
            name="Task 1",
            priority=ExponentialPriority("high"),
        )
        t2 = Task(
            2,
            id_=2,
            name="Task 2",
            priority=ExponentialPriority("low"),
        )
        t3 = Task(
            4,
            id_=3,
            name="Task 3",
            priority=ExponentialPriority("normal"),
        )
        t4 = Task(
            2,
            id_=4,
            name="Task 4",
            priority=ExponentialPriority("highest"),
        )
        t5 = Task(
            6,
            id_=5,
            name="Task 5",
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
                [t1, t4],
                [t2, t3, t4],
                [t4, t5],
                [t1, t2],
                [t2, t5],
            ),
        )

        plans = planner.filter_plans(
            ignore_task_order=True, sort_by="value", only_best=True
        )
        self.assertEqual(plans, ([t1, t4],))

    def test_sort_by_energy_spent(self):
        pool = Pool(name="Pool")
        t1 = Task(5, id_=1, name="Task 1")
        t2 = Task(2, id_=2, name="Task 2")
        t3 = Task(4, id_=3, name="Task 3")
        t4 = Task(2, id_=4, name="Task 4")
        t5 = Task(6, id_=5, name="Task 5")

        pool.add(t1)
        pool.add(t2)
        pool.add(t3)
        pool.add(t4)
        pool.add(t5)

        e = DeterministicEnergoton(8, name="energoton")

        planner = Planner([e], pool)
        planner.build_plans()
        plans = planner.filter_plans(
            ignore_task_order=True, sort_by="energy_spent"
        )

        self.assertEqual(
            plans,
            (
                [t2, t3, t4],
                [t2, t5],
                [t4, t5],
                [t1, t2],
                [t1, t4],
            ),
        )

        plans = planner.filter_plans(
            ignore_task_order=True, sort_by="energy_spent", only_best=True
        )
        self.assertEqual(
            plans,
            (
                [t2, t3, t4],
                [t2, t5],
                [t4, t5],
            ),
        )

    def test_pool_after_plan(self):
        pool1 = Pool(name="Pool 1")
        t1 = Task(5, id_="1", name="Task 1")
        t2 = Task(3, id_="2", name="Task 2")
        pool1.add(t1)
        pool1.add(t2)

        root_pool = Pool(name="root_pool")
        t3 = Task(4, id_="3", name="Task 3")
        root_pool.add(t3)
        root_pool.add(pool1)

        e = NonDeterministicEnergoton(8)

        planner = Planner([e], root_pool)
        planner.build_plans()
        plans = planner.filter_plans(
            ignore_task_order=True, sort_by="length", only_best=True
        )

        result_pool = planner.pool_after_plan(plans[0])
        self.assertEqual(result_pool.get(pool1.id).get(t1.id).spent, 1)

    def test_pool_after_plan_dropped_solved_pools(self):
        pool1 = Pool(name="Pool 1")
        t1 = Task(5, id_="1", name="Task 1")
        t2 = Task(3, id_="2", name="Task 2")

        pool1.add(t1)
        pool1.add(t2)

        root_pool = Pool(name="root_pool")
        root_pool.add(pool1)

        e = DeterministicEnergoton(8)
        planner = Planner([e], root_pool)
        planner.build_plans()

        plans = planner.filter_plans(ignore_task_order=True)
        result_pool = planner.pool_after_plan(plans[0])

        self.assertEqual(len(result_pool), 0)
