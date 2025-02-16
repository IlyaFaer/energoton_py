import unittest

from task import Alternative, Task


class TestTask(unittest.TestCase):
    def test_status(self):
        task = Task(1, "Task 1", 10)
        self.assertFalse(task.is_solved)
        self.assertEqual(task.todo, 10)

        task.spent = 10
        self.assertTrue(task.is_solved)
        self.assertEqual(task.todo, 0)

        task.spent = 5
        self.assertFalse(task.is_solved)
        self.assertEqual(task.todo, 5)

    def test_alternative_is_solved(self):
        t1 = Task(1, "test-name1", 2)
        t2 = Task(2, "test-name2", 2)
        t3 = Task(3, "test-name3", 2)

        rel = Alternative(1, t1, t2, t3)

        self.assertFalse(rel.is_solved)
        self.assertTrue(t1.is_actual)

        t1.spent = 2
        self.assertTrue(rel.is_solved)
        self.assertFalse(t2.is_actual)
        self.assertFalse(t3.is_actual)

        t1.spent = 0
        t2.spent = 2
        self.assertTrue(rel.is_solved)
        self.assertFalse(t1.is_actual)
        self.assertFalse(t3.is_actual)
