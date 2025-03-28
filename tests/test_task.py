import unittest
from unittest import mock

from work import Alternative, Task, WorkDone
from work.relation import Alternative, Blocking


class TestTask(unittest.TestCase):
    def test_status(self):
        task = Task(10, name="Task 1")
        self.assertFalse(task.is_solved)
        self.assertEqual(task.todo, 10)

        task.work_done.append(WorkDone(None, task, 10, mock.Mock()))
        self.assertTrue(task.is_solved)
        self.assertEqual(task.todo, 0)

        task.work_done = []
        task.work_done.append(WorkDone(None, task, 5, mock.Mock()))
        self.assertFalse(task.is_solved)
        self.assertEqual(task.todo, 5)

    def test_alternative_is_solved(self):
        t1 = Task(2, name="test-name1")
        t2 = Task(2, name="test-name2")
        t3 = Task(2, name="test-name3")

        rel = Alternative(t1, t2, t3)

        self.assertFalse(rel.is_solved)
        self.assertTrue(t1.is_actual)

        t1.work_done.append(WorkDone(None, t1, 2, mock.Mock()))
        self.assertTrue(rel.is_solved)
        self.assertFalse(t2.is_actual)
        self.assertFalse(t3.is_actual)

        t1.work_done = []
        t1.work_done.append(WorkDone(None, t2, 2, mock.Mock()))
        self.assertTrue(rel.is_solved)
        self.assertFalse(t1.is_actual)
        self.assertFalse(t3.is_actual)

    def test_part_done(self):
        task = Task(8, name="Task 1")

        work_done = WorkDone(None, task, 5, mock.Mock())
        task.work_done.append(work_done)

        self.assertEqual(work_done.amount, 5)
        self.assertEqual(work_done.task.spent, 5)
        self.assertEqual(work_done.task.todo, 3)
        self.assertEqual(work_done.task.name, "Task 1")

    def test_custom_fields(self):
        key1 = "key1"
        value1 = "value1"

        unit = Task(cost=3, name="test-name", custom_fields={key1: value1})

        self.assertEqual(unit[key1], value1)

        key2 = "key2"
        value2 = "value2"
        unit[key2] = value2

        self.assertEqual(unit[key2], value2)

        del unit[key2]

        with self.assertRaises(KeyError):
            unit[key2]

    def test_blocking_relationship(self):
        blocker = Task(cost=3, name="test-name1")
        blocked = Task(cost=3, name="test-name2")

        rel = Blocking(blocker, blocked)

        self.assertEqual(list(blocked.blocked_by), [rel])
        self.assertEqual(list(blocker.blocked_by), [])

        self.assertEqual(list(blocked.blocking), [])
        self.assertEqual(list(blocker.blocking), [rel])

    def test_is_blocked_by_parent(self):
        root = Task(cost=3, name="test-name4")
        parent = Task(cost=3, name="test-name3", parent=root)

        blocked = Task(cost=3, name="test-name2", parent=parent)
        blocker = Task(cost=3, name="test-name1")

        Blocking(blocker, parent)

        self.assertTrue(blocked.is_blocked)

        blocked.relations = {}
        parent.relations = {}
        self.assertFalse(blocked.is_blocked)

        Blocking(blocker, root)
        self.assertTrue(blocked.is_blocked)

    def test_drop_blocking(self):
        blocker = Task(cost=3, name="test-name1")
        blocked = Task(cost=3, name="test-name2")

        rel = Blocking(blocker, blocked)
        self.assertTrue(blocked.is_blocked)

        rel.drop()

        self.assertEqual(list(blocker.blocking), [])
        self.assertEqual(list(blocked.blocked_by), [])
        self.assertFalse(blocked.is_blocked)

    def test_alternative_relationship(self):
        alt1 = Task(cost=3, name="test-name1")
        alt2 = Task(cost=3, name="test-name2")
        alt3 = Task(cost=3, name="test-name3")

        rel = Alternative(alt1, alt2, alt3)

        self.assertEqual(list(alt1.relations.values())[0], rel)
        self.assertEqual(list(alt2.relations.values())[0], rel)
        self.assertEqual(list(alt3.relations.values())[0], rel)


class TestPartTask(unittest.TestCase):
    def test_part(self):
        task = Task(10, name="Task 1")

        done = WorkDone(None, task, 5, mock.Mock())
        task.work_done.append(done)

        self.assertEqual(done.amount, 5)
        self.assertEqual(done.task.spent, 5)
        self.assertEqual(done.task.todo, 5)
        self.assertEqual(done.task.name, "Task 1")
