import unittest

from energoton import DeterministicEnergoton, NonDeterministicEnergoton
from work import Alternative, Blocking, Pool, Task, WorkDone
from energoton.planner import Plan


class TestEnergoton(unittest.TestCase):
    def test_can_solve(self):
        e = DeterministicEnergoton(10)
        t = Task(5)
        self.assertTrue(e.can_solve(t))

        e.energy_left = 0
        self.assertFalse(e.can_solve(t))

    def test_work(self):
        e = DeterministicEnergoton(10)
        t = Task(5)
        e.work(t)

        self.assertEqual(t.spent, 5)
        self.assertEqual(e.energy_left, 5)

    def test_build_plans_deterministic(self):
        pool = Pool()
        t1 = Task(5, id_=1)
        t2 = Task(2, id_=2)
        t3 = Task(4, id_=3)
        t4 = Task(2, id_=4)
        t5 = Task(6, id_=5)

        pool.add(t1)
        pool.add(t2)
        pool.add(t3)
        pool.add(t4)
        pool.add(t5)

        e = DeterministicEnergoton(8)
        plans = e.build_plans(pool)

        self.assertEqual(
            plans,
            [
                Plan(
                    [
                        WorkDone(None, t1, 5, e),
                        WorkDone(None, t2, 2, e),
                    ]
                ),
                Plan(
                    [
                        WorkDone(None, t1, 5, e),
                        WorkDone(None, t4, 2, e),
                    ]
                ),
                Plan(
                    [
                        WorkDone(None, t2, 2, e),
                        WorkDone(None, t3, 4, e),
                        WorkDone(None, t4, 2, e),
                    ]
                ),
                Plan(
                    [
                        WorkDone(None, t2, 2, e),
                        WorkDone(None, t5, 6, e),
                    ]
                ),
                Plan(
                    [
                        WorkDone(None, t2, 2, e),
                        WorkDone(None, t4, 2, e),
                        WorkDone(None, t3, 4, e),
                    ]
                ),
                Plan(
                    [
                        WorkDone(None, t2, 2, e),
                        WorkDone(None, t1, 5, e),
                    ]
                ),
                Plan(
                    [
                        WorkDone(None, t3, 4, e),
                        WorkDone(None, t4, 2, e),
                        WorkDone(None, t2, 2, e),
                    ]
                ),
                Plan(
                    [
                        WorkDone(None, t3, 4, e),
                        WorkDone(None, t2, 2, e),
                        WorkDone(None, t4, 2, e),
                    ]
                ),
                Plan(
                    [
                        WorkDone(None, t4, 2, e),
                        WorkDone(None, t5, 6, e),
                    ]
                ),
                Plan(
                    [
                        WorkDone(None, t4, 2, e),
                        WorkDone(None, t1, 5, e),
                    ]
                ),
                Plan(
                    [
                        WorkDone(None, t4, 2, e),
                        WorkDone(None, t2, 2, e),
                        WorkDone(None, t3, 4, e),
                    ]
                ),
                Plan(
                    [
                        WorkDone(None, t4, 2, e),
                        WorkDone(None, t3, 4, e),
                        WorkDone(None, t2, 2, e),
                    ]
                ),
                Plan(
                    [
                        WorkDone(None, t5, 6, e),
                        WorkDone(None, t2, 2, e),
                    ]
                ),
                Plan(
                    [
                        WorkDone(None, t5, 6, e),
                        WorkDone(None, t4, 2, e),
                    ]
                ),
            ],
        )

    def test_build_plans_non_deterministic(self):
        pool = Pool()
        t1 = Task(5, id_="1")
        t2 = Task(2, id_="2")
        t3 = Task(4, id_="3")

        pool.add(t1)
        pool.add(t2)
        pool.add(t3)

        e = NonDeterministicEnergoton(8)
        plans = e.build_plans(pool)

        plan = Plan(
            [
                WorkDone(None, t1, 5, e),
                WorkDone(None, t3, 3, e),
            ]
        )

        self.assertEqual(
            plans,
            [
                Plan(
                    [
                        WorkDone(None, t1, 5, e),
                        WorkDone(None, t2, 2, e),
                        WorkDone(None, t3, 1, e),
                    ]
                ),
                Plan(
                    [
                        WorkDone(None, t1, 5, e),
                        WorkDone(None, t3, 3, e),
                    ]
                ),
                Plan(
                    [
                        WorkDone(None, t1, 2, e),
                        WorkDone(None, t2, 2, e),
                        WorkDone(None, t3, 4, e),
                    ]
                ),
                Plan(
                    [
                        WorkDone(None, t1, 5, e),
                        WorkDone(None, t2, 2, e),
                        WorkDone(None, t3, 1, e),
                    ]
                ),
                Plan(
                    [
                        WorkDone(None, t1, 4, e),
                        WorkDone(None, t3, 4, e),
                    ]
                ),
                Plan(
                    [
                        WorkDone(None, t1, 2, e),
                        WorkDone(None, t2, 2, e),
                        WorkDone(None, t3, 4, e),
                    ]
                ),
            ],
        )

    def test_build_plans_blocked(self):
        pool = Pool()
        t1 = Task(5)
        t2 = Task(2)
        t3 = Task(4)
        t4 = Task(2)
        t5 = Task(6)

        pool.add(t1)
        pool.add(t2)
        pool.add(t3)
        pool.add(t4)
        pool.add(t5)

        Blocking(t5, t3)

        e = DeterministicEnergoton(8)
        plans = e.build_plans(pool)

        self.assertEqual(
            plans,
            [
                Plan([WorkDone(None, t1, 5, e), WorkDone(None, t2, 2, e)]),
                Plan([WorkDone(None, t1, 5, e), WorkDone(None, t4, 2, e)]),
                Plan([WorkDone(None, t2, 2, e), WorkDone(None, t5, 6, e)]),
                Plan([WorkDone(None, t2, 2, e), WorkDone(None, t4, 2, e)]),
                Plan([WorkDone(None, t2, 2, e), WorkDone(None, t1, 5, e)]),
                Plan([WorkDone(None, t4, 2, e), WorkDone(None, t5, 6, e)]),
                Plan([WorkDone(None, t4, 2, e), WorkDone(None, t1, 5, e)]),
                Plan([WorkDone(None, t4, 2, e), WorkDone(None, t2, 2, e)]),
                Plan([WorkDone(None, t5, 6, e), WorkDone(None, t2, 2, e)]),
                Plan([WorkDone(None, t5, 6, e), WorkDone(None, t4, 2, e)]),
            ],
        )

    def test_build_plans_alternative(self):
        pool = Pool(name="Pool")
        t1 = Task(5)
        t2 = Task(2)
        t3 = Task(4)
        t4 = Task(2)
        t5 = Task(6)

        pool.add(t1)
        pool.add(t2)
        pool.add(t3)
        pool.add(t4)
        pool.add(t5)

        Alternative(t1, t2)

        e = DeterministicEnergoton(8)
        plans = list(e.build_plans(pool))

        self.assertEqual(
            plans,
            [
                Plan([WorkDone(None, t1, 5, e), WorkDone(None, t4, 2, e)]),
                Plan(
                    [
                        WorkDone(None, t2, 2, e),
                        WorkDone(None, t3, 4, e),
                        WorkDone(None, t4, 2, e),
                    ]
                ),
                Plan([WorkDone(None, t2, 2, e), WorkDone(None, t5, 6, e)]),
                Plan(
                    [
                        WorkDone(None, t2, 2, e),
                        WorkDone(None, t4, 2, e),
                        WorkDone(None, t3, 4, e),
                    ]
                ),
                Plan(
                    [
                        WorkDone(None, t3, 4, e),
                        WorkDone(None, t4, 2, e),
                        WorkDone(None, t2, 2, e),
                    ]
                ),
                Plan(
                    [
                        WorkDone(None, t3, 4, e),
                        WorkDone(None, t2, 2, e),
                        WorkDone(None, t4, 2, e),
                    ]
                ),
                Plan([WorkDone(None, t4, 2, e), WorkDone(None, t1, 5, e)]),
                Plan([WorkDone(None, t4, 2, e), WorkDone(None, t5, 6, e)]),
                Plan(
                    [
                        WorkDone(None, t4, 2, e),
                        WorkDone(None, t2, 2, e),
                        WorkDone(None, t3, 4, e),
                    ]
                ),
                Plan(
                    [
                        WorkDone(None, t4, 2, e),
                        WorkDone(None, t3, 4, e),
                        WorkDone(None, t2, 2, e),
                    ]
                ),
                Plan([WorkDone(None, t5, 6, e), WorkDone(None, t2, 2, e)]),
                Plan([WorkDone(None, t5, 6, e), WorkDone(None, t4, 2, e)]),
            ],
        )

    def test_charges(self):
        charge = 5
        e = DeterministicEnergoton(charge)
        self.assertEqual(e.energy_left, charge)
        self.assertEqual(e.next_charge, charge)

        e = DeterministicEnergoton([5, 3, 2])
        self.assertEqual(e.energy_left, 5)
        e.recharge()

        self.assertEqual(e.energy_left, 3)
        e.recharge()

        self.assertEqual(e.energy_left, 2)
        e.recharge()

        self.assertEqual(e.energy_left, 0)
