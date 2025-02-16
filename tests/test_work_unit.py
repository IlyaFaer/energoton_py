import unittest

from task.relation import Alternative, Blocking
from task.work_unit import WorkUnit


class TestWorkUnit(unittest.TestCase):
    def test_id_immutable(self):
        id_ = 1

        unit = WorkUnit(id_, "test-name")
        with self.assertRaises(ValueError):
            unit.id = 2

        self.assertEqual(unit.id, id_)

    def test_custom_fields(self):
        key1 = "key1"
        value1 = "value1"

        unit = WorkUnit(1, "test-name", custom_fields={key1: value1})

        self.assertEqual(unit[key1], value1)

        key2 = "key2"
        value2 = "value2"
        unit[key2] = value2

        self.assertEqual(unit[key2], value2)

        del unit[key2]

        with self.assertRaises(KeyError):
            unit[key2]

    def test_blocking_relationship(self):
        blocker = WorkUnit(1, "test-name1")
        blocked = WorkUnit(2, "test-name2")

        rel = Blocking(1, blocker, blocked)

        self.assertEqual(blocked.blocked_by, [rel])
        self.assertEqual(blocker.blocked_by, [])

        self.assertEqual(blocked.blocking, [])
        self.assertEqual(blocker.blocking, [rel])

    def test_is_blocked_by_parent(self):
        root = WorkUnit(4, "test-name4")
        parent = WorkUnit(3, "test-name3", parent=root)

        blocked = WorkUnit(2, "test-name2", parent=parent)
        blocker = WorkUnit(1, "test-name1")

        Blocking(1, blocker, parent)

        self.assertTrue(blocked.is_blocked)

        blocked.relations = {}
        parent.relations = {}
        self.assertFalse(blocked.is_blocked)

        Blocking(2, blocker, root)
        self.assertTrue(blocked.is_blocked)

    def test_drop_blocking(self):
        blocker = WorkUnit(1, "test-name1")
        blocked = WorkUnit(2, "test-name2")

        rel = Blocking(1, blocker, blocked)
        self.assertTrue(blocked.is_blocked)

        rel.drop()

        self.assertEqual(blocker.blocking, [])
        self.assertEqual(blocked.blocked_by, [])
        self.assertFalse(blocked.is_blocked)

    def test_alternative_relationship(self):
        alt1 = WorkUnit(1, "test-name1")
        alt2 = WorkUnit(2, "test-name2")
        alt3 = WorkUnit(3, "test-name3")

        rel = Alternative(1, alt1, alt2, alt3)

        self.assertEqual(alt1.relations[1], rel)
        self.assertEqual(alt2.relations[1], rel)
        self.assertEqual(alt3.relations[1], rel)
