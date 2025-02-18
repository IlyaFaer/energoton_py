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
        t6 = Task(3, id_=6, name="Task 6")

        pool.add(t1)
        pool.add(t2)
        pool.add(t3)
        pool.add(t4)
        pool.add(t5)
        pool.add(t6)

        e = DeterministicEnergoton(8, name="energoton")
        plans = e.build_plans(pool)
        self.assertEqual(
            plans,
            set(
                (
                    (t1, t2),
                    (t1, t4),
                    (t1, t6),
                    (t2, t5),
                    (t2, t3, t4),
                    (t2, t4, t6),
                    (t3, t6),
                    (t4, t5),
                ),
            ),
        )

    def test_build_plans_non_deterministic(self):
        pool = Pool(name="Pool")
        t1 = Task(5, id_="1", name="Task 1")
        t2 = Task(2, id_="2", name="Task 2")
        t3 = Task(4, id_="3", name="Task 3")
        t4 = Task(2, id_="4", name="Task 4")

        pool.add(t1)
        pool.add(t2)
        pool.add(t3)
        pool.add(t4)

        e = NonDeterministicEnergoton(8, name="energoton")
        plans = e.build_plans(pool)

        t3_part = t3.part(part_done=3)
        self.assertIn((t1, t3_part), plans)
        t3.drop_part(t3_part)

        t1_part = t1.part(part_done=2)
        self.assertIn((t1_part, t2, t3), plans)
        t1.drop_part(t1_part)

        t3_part = t3.part(part_done=1)
        self.assertIn((t1, t3_part, t4), plans)
        t3.drop_part(t3_part)

        t3_part = t3.part(part_done=1)
        self.assertIn((t1, t2, t3_part), plans)
        t3.drop_part(t3_part)

        t1_part = t1.part(part_done=2)
        self.assertIn((t1_part, t3, t4), plans)
        t1.drop_part(t1_part)

        t4_part = t4.part(part_done=1)
        self.assertIn((t1, t2, t4_part), plans)
        t4.drop_part(t4_part)

        t2_part = t2.part(part_done=1)
        self.assertIn((t1, t2_part, t4), plans)
        t2.drop_part(t2_part)

        t1_part = t1.part(part_done=4)
        self.assertIn((t1_part, t2, t4), plans)
        t1.drop_part(t1_part)

        t1_part = t1.part(part_done=4)
        self.assertIn((t1_part, t3), plans)

        self.assertIn((t2, t3, t4), plans)

    def test_build_plans_blocked(self):
        pool = Pool(name="Pool")
        t1 = Task(5, id_=1, name="Task 1")
        t2 = Task(2, id_=2, name="Task 2")
        t3 = Task(4, id_=3, name="Task 3")
        t4 = Task(2, id_=4, name="Task 4")
        t5 = Task(6, id_=5, name="Task 5")
        t6 = Task(3, id_=6, name="Task 6")

        pool.add(t1)
        pool.add(t2)
        pool.add(t3)
        pool.add(t4)
        pool.add(t5)
        pool.add(t6)

        Blocking(t5, t3)

        e = DeterministicEnergoton(8, name="energoton")
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
        pool = Pool(name="Pool")
        t1 = Task(5, id_=1, name="Task 1")
        t2 = Task(2, id_=2, name="Task 2")
        t3 = Task(4, id_=3, name="Task 3")
        t4 = Task(2, id_=4, name="Task 4")
        t5 = Task(6, id_=5, name="Task 5")
        t6 = Task(3, id_=6, name="Task 6")

        pool.add(t1)
        pool.add(t2)
        pool.add(t3)
        pool.add(t4)
        pool.add(t5)
        pool.add(t6)

        Alternative(t1, t2)

        e = DeterministicEnergoton(8, name="energoton")
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
                    (t3, t6),
                    (t2, t3, t4),
                ),
            ),
        )
