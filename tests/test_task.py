import unittest
from unittest import mock

from work import Alternative, Task


class TestTask(unittest.TestCase):
    def test_status(self):
        task = Task(10, name="Task 1")
        self.assertFalse(task.is_solved)
        self.assertEqual(task.todo, 10)

        task.work_done(10, mock.Mock())
        self.assertTrue(task.is_solved)
        self.assertEqual(task.todo, 0)

        task._work_done = []
        task.work_done(5, mock.Mock())
        self.assertFalse(task.is_solved)
        self.assertEqual(task.todo, 5)

    def test_alternative_is_solved(self):
        t1 = Task(2, name="test-name1")
        t2 = Task(2, name="test-name2")
        t3 = Task(2, name="test-name3")

        rel = Alternative(t1, t2, t3)

        self.assertFalse(rel.is_solved)
        self.assertTrue(t1.is_actual)

        t1.work_done(2, mock.Mock())
        self.assertTrue(rel.is_solved)
        self.assertFalse(t2.is_actual)
        self.assertFalse(t3.is_actual)

        t1._work_done = []
        t2.work_done(2, mock.Mock())
        self.assertTrue(rel.is_solved)
        self.assertFalse(t1.is_actual)
        self.assertFalse(t3.is_actual)

    def test_part_done(self):
        task = Task(8, name="Task 1")

        work_done = task.work_done(5, mock.Mock())

        self.assertEqual(work_done.amount, 5)
        self.assertEqual(work_done.task.spent, 5)
        self.assertEqual(work_done.task.todo, 3)
        self.assertEqual(work_done.task.name, "Task 1")


class TestPartTask(unittest.TestCase):
    def test_part(self):
        task = Task(10, name="Task 1")

        done = task.work_done(5, mock.Mock())

        self.assertEqual(done.amount, 5)
        self.assertEqual(done.task.spent, 5)
        self.assertEqual(done.task.todo, 5)
        self.assertEqual(done.task.name, "Task 1")
