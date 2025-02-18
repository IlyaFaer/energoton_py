import unittest

from work import Alternative, Task


class TestTask(unittest.TestCase):
    def test_status(self):
        task = Task(10, name="Task 1")
        self.assertFalse(task.is_solved)
        self.assertEqual(task.todo, 10)

        task.spent = 10
        self.assertTrue(task.is_solved)
        self.assertEqual(task.todo, 0)

        task.spent = 5
        self.assertFalse(task.is_solved)
        self.assertEqual(task.todo, 5)

    def test_alternative_is_solved(self):
        t1 = Task(2, name="test-name1")
        t2 = Task(2, name="test-name2")
        t3 = Task(2, name="test-name3")

        rel = Alternative(t1, t2, t3)

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

    def test_part_done(self):
        task = Task(8, name="Task 1")

        task.spent = 5
        part = task.part(5)

        self.assertEqual(part.part_done, 5)
        self.assertEqual(part.spent, 5)
        self.assertEqual(part.todo, 3)
        self.assertEqual(part.name, "Task 1")


class TestPartTask(unittest.TestCase):
    def test_part(self):
        task = Task(10, name="Task 1")

        task.spent = 5
        part = task.part(5)

        self.assertEqual(part.part_done, 5)
        self.assertEqual(part.spent, 5)
        self.assertEqual(part.todo, 5)
        self.assertEqual(part.name, "Task 1")
