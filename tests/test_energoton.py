import unittest

from energoton import Energoton
from task import Alternative, Blocking, Pool, Task


class TestEnergoton(unittest.TestCase):
    def test_can_solve(self):
        e = Energoton(1, "energoton", 10)
        t = Task(1, "Task", 5)
        self.assertTrue(e.can_solve(t))

        e.energy_left = 0
        self.assertFalse(e.can_solve(t))

    def test_work(self):
        e = Energoton(1, "energoton", 10)
        t = Task(1, "Task", 5)
        e.work(t)

        self.assertEqual(t.spent, 5)
        self.assertEqual(e.energy_left, 5)

    def test_build_plans_deterministic(self):
        pool = Pool(1, "Pool")
        t1 = Task(1, "Task 1", 5)
        t2 = Task(2, "Task 2", 2)
        t3 = Task(3, "Task 3", 4)
        t4 = Task(4, "Task 4", 2)
        t5 = Task(5, "Task 5", 6)
        t6 = Task(6, "Task 6", 3)

        pool.add(t1)
        pool.add(t2)
        pool.add(t3)
        pool.add(t4)
        pool.add(t5)
        pool.add(t6)

        e = Energoton(1, "energoton", 8)
        plans = e.build_plans(pool)
        self.assertEqual(
            plans,
            set(
                (
                    (t1, t4),
                    (t2, t5),
                    (t2, t3, t4),
                    (t4, t5),
                    (t2, t4, t6),
                    (t1, t6),
                    (t1, t2),
                ),
            ),
        )

    def test_build_plans_blocked(self):
        pool = Pool(1, "Pool")
        t1 = Task(1, "Task 1", 5)
        t2 = Task(2, "Task 2", 2)
        t3 = Task(3, "Task 3", 4)
        t4 = Task(4, "Task 4", 2)
        t5 = Task(5, "Task 5", 6)
        t6 = Task(6, "Task 6", 3)

        pool.add(t1)
        pool.add(t2)
        pool.add(t3)
        pool.add(t4)
        pool.add(t5)
        pool.add(t6)

        Blocking(1, t5, t3)

        e = Energoton(1, "energoton", 8)
        plans = e.build_plans(pool)
        self.assertEqual(
            plans,
            set(
                (
                    (t1, t4),
                    (t2, t5),
                    (t4, t5),
                    (t2, t4, t6),
                    (t1, t6),
                    (t1, t2),
                ),
            ),
        )

    def test_build_plans_alternative(self):
        pool = Pool(1, "Pool")
        t1 = Task(1, "Task 1", 5)
        t2 = Task(2, "Task 2", 2)
        t3 = Task(3, "Task 3", 4)
        t4 = Task(4, "Task 4", 2)
        t5 = Task(5, "Task 5", 6)
        t6 = Task(6, "Task 6", 3)

        pool.add(t1)
        pool.add(t2)
        pool.add(t3)
        pool.add(t4)
        pool.add(t5)
        pool.add(t6)

        Alternative(1, t1, t2)

        e = Energoton(1, "energoton", 8)
        plans = e.build_plans(pool)
        self.assertEqual(
            plans,
            set(
                (
                    (t1, t4),
                    (t2, t5),
                    (t2, t4, t6),
                    (t1, t6),
                    (t3, t6),
                    (t2, t3, t4),
                ),
            ),
        )
