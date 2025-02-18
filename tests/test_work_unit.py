import unittest

from work.relation import Alternative, Blocking
from work.work_unit import WorkUnit


class TestWorkUnit(unittest.TestCase):
    def test_custom_fields(self):
        key1 = "key1"
        value1 = "value1"

        unit = WorkUnit(name="test-name", custom_fields={key1: value1})

        self.assertEqual(unit[key1], value1)

        key2 = "key2"
        value2 = "value2"
        unit[key2] = value2

        self.assertEqual(unit[key2], value2)

        del unit[key2]

        with self.assertRaises(KeyError):
            unit[key2]

    def test_blocking_relationship(self):
        blocker = WorkUnit(name="test-name1")
        blocked = WorkUnit(name="test-name2")

        rel = Blocking(blocker, blocked)

        self.assertEqual(list(blocked.blocked_by), [rel])
        self.assertEqual(list(blocker.blocked_by), [])

        self.assertEqual(list(blocked.blocking), [])
        self.assertEqual(list(blocker.blocking), [rel])

    def test_is_blocked_by_parent(self):
        root = WorkUnit(name="test-name4")
        parent = WorkUnit(name="test-name3", parent=root)

        blocked = WorkUnit(name="test-name2", parent=parent)
        blocker = WorkUnit(name="test-name1")

        Blocking(blocker, parent)

        self.assertTrue(blocked.is_blocked)

        blocked.relations = {}
        parent.relations = {}
        self.assertFalse(blocked.is_blocked)

        Blocking(blocker, root)
        self.assertTrue(blocked.is_blocked)

    def test_drop_blocking(self):
        blocker = WorkUnit(name="test-name1")
        blocked = WorkUnit(name="test-name2")

        rel = Blocking(blocker, blocked)
        self.assertTrue(blocked.is_blocked)

        rel.drop()

        self.assertEqual(list(blocker.blocking), [])
        self.assertEqual(list(blocked.blocked_by), [])
        self.assertFalse(blocked.is_blocked)

    def test_alternative_relationship(self):
        alt1 = WorkUnit(name="test-name1")
        alt2 = WorkUnit(name="test-name2")
        alt3 = WorkUnit(name="test-name3")

        rel = Alternative(alt1, alt2, alt3)

        self.assertEqual(list(alt1.relations.values())[0], rel)
        self.assertEqual(list(alt2.relations.values())[0], rel)
        self.assertEqual(list(alt3.relations.values())[0], rel)
