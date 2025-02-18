import unittest

from base.mixins import IdMixin


class TestIdMixin(unittest.TestCase):
    def test_id_immutable(self):
        id_ = 1

        unit = IdMixin(id_)
        with self.assertRaises(ValueError):
            unit.id = 2

        self.assertEqual(unit.id, id_)

    def test_id_generated(self):
        unit1 = IdMixin()
        unit2 = IdMixin()

        self.assertNotEqual(unit1.id, unit2.id)

    def test_id_equality(self):
        unit1 = IdMixin()
        unit2 = IdMixin()

        self.assertNotEqual(unit1, unit2)

        unit2 = IdMixin(unit1.id)
        self.assertEqual(unit1, unit2)
