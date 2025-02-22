import unittest

from energoton import DeterministicEnergoton, NonDeterministicEnergoton
from work import Alternative, Blocking, Pool, Task


class TestEnergoton(unittest.TestCase):
    def test_can_solve(self):
        e = DeterministicEnergoton(10, name="energoton")
        t = Task(5, name="Task")
        self.assertTrue(e.can_solve(t))

        e.energy_left = 0
        self.assertFalse(e.can_solve(t))

    def test_work(self):
        e = DeterministicEnergoton(10, name="energoton")
        t = Task(5, name="Task")
        e.work(t)

        self.assertEqual(t.spent, 5)
        self.assertEqual(e.energy_left, 5)

    def test_build_plans_deterministic(self):
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
        plans = e.build_plans(pool)
        self.assertEqual(
            plans,
            [
                [t1, t2],
                [t1, t4],
                [t2, t3, t4],
                [t2, t5],
                [t2, t4, t3],
                [t2, t1],
                [t3, t4, t2],
                [t3, t2, t4],
                [t4, t5],
                [t4, t1],
                [t4, t2, t3],
                [t4, t3, t2],
                [t5, t2],
                [t5, t4],
            ],
        )

    def test_build_plans_non_deterministic(self):
        pool = Pool(name="Pool")
        t1 = Task(5, id_="1", name="Task 1")
        t2 = Task(2, id_="2", name="Task 2")
        t3 = Task(4, id_="3", name="Task 3")

        pool.add(t1)
        pool.add(t2)
        pool.add(t3)

        e = NonDeterministicEnergoton(8, name="energoton")
        plans = e.build_plans(pool)

        t3_part = t3.part(part_done=1)
        self.assertIn([t1, t2, t3_part], plans)
        t3.drop_part(t3_part)

        t3_part = t3.part(part_done=3)
        self.assertIn([t1, t3_part], plans)
        t3.drop_part(t3_part)

        t1_part = t1.part(part_done=2)
        self.assertIn([t2, t3, t1_part], plans)
        t1.drop_part(t1_part)

        t3_part = t3.part(part_done=1)
        self.assertIn([t2, t1, t3_part], plans)
        t3.drop_part(t3_part)

        t1_part = t1.part(part_done=4)
        self.assertIn([t3, t1_part], plans)
        t1.drop_part(t1_part)

        t1_part = t1.part(part_done=2)
        self.assertIn([t3, t2, t1_part], plans)
        t1.drop_part(t1_part)

    def test_build_plans_blocked(self):
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

        Blocking(t5, t3)

        e = DeterministicEnergoton(8, name="energoton")
        plans = e.build_plans(pool)
        self.assertEqual(
            plans,
            [
                [t1, t2],
                [t1, t4],
                [t2, t5],
                [t2, t4],
                [t2, t1],
                [t4, t5],
                [t4, t1],
                [t4, t2],
                [t5, t2],
                [t5, t4],
            ],
        )

    def test_build_plans_alternative(self):
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

        Alternative(t1, t2)

        e = DeterministicEnergoton(8, name="energoton")
        plans = list(e.build_plans(pool))
        self.assertEqual(
            plans,
            [
                [t1, t4],
                [t2, t3, t4],
                [t2, t5],
                [t2, t4, t3],
                [t3, t4, t2],
                [t3, t2, t4],
                [t4, t1],
                [t4, t5],
                [t4, t2, t3],
                [t4, t3, t2],
                [t5, t2],
                [t5, t4],
            ],
        )
