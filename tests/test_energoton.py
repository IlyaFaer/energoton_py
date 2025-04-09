import unittest

from energoton import DeterministicEnergoton, NonDeterministicEnergoton
from work import Alternative, Blocking, Pool, Task, WorkDone
from energoton.planner import Plan


class TestEnergoton(unittest.TestCase):
    def test_can_solve(self):
        e = DeterministicEnergoton(10)
        t = Task(5)

        e.pool = Pool(children=[t])

        dry = t.dry
        self.assertTrue(e.can_solve(dry))

        e.energy_left = 0
        self.assertFalse(e.can_solve(dry))

    def test_work(self):
        e = DeterministicEnergoton(10)
        t = Task(5)
        e.pool = Pool(children=[t])

        dry = t.dry
        e.work(dry)

        self.assertEqual(dry["spent"], 5)
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
        e.pool = pool
        plans = e.build_plans(pool.dry)

        p = Plan(
            [
                WorkDone(t2, 2, e),
                WorkDone(t3, 4, e),
                WorkDone(t4, 2, e),
            ]
        )
        p.commit()

        self.assertEqual(plans, [p])

    def test_build_plans_non_deterministic(self):
        pool = Pool()
        t1 = Task(5, id_="1")
        t2 = Task(2, id_="2")
        t3 = Task(4, id_="3")

        pool.add(t1)
        pool.add(t2)
        pool.add(t3)

        e = NonDeterministicEnergoton(8)
        e.pool = pool
        plans = e.build_plans(pool.dry)

        p1 = Plan(
            [
                WorkDone(t1, 2, e),
                WorkDone(t2, 2, e),
                WorkDone(t3, 4, e),
            ]
        )
        p1.commit()

        p2 = Plan(
            [
                WorkDone(t1, 5, e),
                WorkDone(t2, 2, e),
                WorkDone(t3, 1, e),
            ]
        )
        p2.commit()

        self.assertEqual(plans, [p1, p2])

    def test_build_plans_blocked(self):
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

        Blocking(t5, t3)

        e = DeterministicEnergoton(8)
        e.pool = pool
        plans = e.build_plans(pool.dry)

        p1 = Plan([WorkDone(t2, 2, e), WorkDone(t4, 2, e)])
        p2 = Plan([WorkDone(t1, 5, e), WorkDone(t2, 2, e)])
        p3 = Plan([WorkDone(t2, 2, e), WorkDone(t5, 6, e)])
        p4 = Plan([WorkDone(t1, 5, e), WorkDone(t4, 2, e)])
        p5 = Plan([WorkDone(t4, 2, e), WorkDone(t5, 6, e)])
        p1.commit()
        p2.commit()
        p3.commit()
        p4.commit()
        p5.commit()

        self.assertEqual(
            plans,
            [p1, p2, p3, p4, p5],
        )

    def test_build_plans_alternative(self):
        pool = Pool(name="Pool")
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

        Alternative(t1, t2)

        e = DeterministicEnergoton(8)
        e.pool = pool
        plans = list(e.build_plans(pool.dry))

        p = Plan(
            [
                WorkDone(t2, 2, e),
                WorkDone(t3, 4, e),
                WorkDone(t4, 2, e),
            ]
        )
        p.commit()

        self.assertEqual(plans, [p])

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
