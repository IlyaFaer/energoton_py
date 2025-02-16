import unittest

from task import Pool, Task


class TestPool(unittest.TestCase):
    def test_task_by_key(self):
        task_id = "there-is-some-id"

        task = Task(task_id, "Task 1", 10)
        pool = Pool(1, "Pool 1", children=[task])

        self.assertEqual(pool.get(task_id), task)

        task_id2 = "there-is-another-id"
        task = Task(task_id2, "Task 2", 20)
        pool.add(task)

        self.assertEqual(pool.get(task_id2), task)

    def test_task_already_exists(self):
        same_id = "same-id"

        task = Task(same_id, "Task 1", 10)
        pool = Pool(1, "Pool 1", children=[task])

        task2 = Task(same_id, "Task 2", 20)

        with self.assertRaises(ValueError):
            pool.add(task2)

    def test_parenting(self):
        task_id = "there-is-some-id"

        task = Task(task_id, "Task 1", 10)
        pool = Pool(1, "Pool 1", children=[task])

        self.assertEqual(task.parent, pool)

        pool.pop(task_id)

        self.assertIsNone(task.parent)

        new_pool = Pool(2, "Pool 2")

        pool.add(new_pool)
        self.assertEqual(new_pool.parent, pool)

        pool.pop(new_pool.id)
        self.assertIsNone(new_pool.parent)

    def test_iter(self):
        tasks = [Task(i, f"Task {i}", i) for i in range(5)]
        pool = Pool(1, "Pool 1", children=tasks)

        for task in pool:
            self.assertIn(task, tasks)

        self.assertEqual(len(pool), len(tasks))

    def test_is_solved(self):
        tasks = [Task(i, f"Task {i}", i) for i in range(5)]
        pool = Pool(1, "Pool 1", children=tasks)

        self.assertFalse(pool.is_solved)

        for task in tasks:
            task.spent = task.cost

        self.assertTrue(pool.is_solved)

    def test_done(self):
        task1 = Task(1, "Task 1", 10)
        task1.spent = 10

        task2 = Task(2, "Task 2", 20)

        pool = Pool(1, "Pool 1", children=[task1, task2])

        self.assertEqual(pool.done, [task1])
        self.assertEqual(pool.todo, [task2])

    def test_composite(self):
        task1 = Task(1, "Task 1", 10)
        task2 = Task(2, "Task 2", 20)
        task2.spent = 20
        pool1 = Pool(1, "Pool 1", children=[task1, task2])

        task3 = Task(3, "Task 3", 30)
        task4 = Task(4, "Task 4", 40)
        pool2 = Pool(2, "Pool 2", children=[task3, task4])

        task5 = Task(5, "Task 5", 50)
        task6 = Task(6, "Task 6", 60)
        task6.spent = 60

        root_pool = Pool(3, "Root Pool", children=[pool1, pool2, task5, task6])

        self.assertFalse(root_pool.is_solved)

        self.assertEqual(root_pool.todo, [pool1, pool2, task5])
        self.assertEqual(root_pool.done, [task6])

        # make the first pool solved
        task1.spent = 10
        self.assertEqual(root_pool.todo, [pool2, task5])

        # make the second pool solved
        task3.spent = 30
        task4.spent = 40
        self.assertEqual(root_pool.todo, [task5])

        # make the last task solved
        task5.spent = 50
        self.assertTrue(root_pool.is_solved)

        self.assertEqual(root_pool.done, [pool1, pool2, task5, task6])
        self.assertEqual(root_pool.todo, [])

    def test_composite_iter(self):
        task1 = Task(1, "Task 1", 10)
        task2 = Task(2, "Task 2", 20)

        pool1 = Pool(1, "Pool 1", children=[task1, task2])

        task3 = Task(3, "Task 3", 30)

        root_pool = Pool(3, "Root Pool", children=[pool1, task3])
        self.assertEqual(list(root_pool), [pool1, task3])
