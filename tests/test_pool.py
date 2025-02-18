import unittest

from work import Pool, Task


class TestPool(unittest.TestCase):
    def test_task_by_key(self):
        task_id = "there-is-some-id"

        task = Task(10, id_=task_id, name="Task 1")
        pool = Pool(children=[task], name="Pool 1")

        self.assertEqual(pool.get(task_id), task)

        task_id2 = "there-is-another-id"
        task = Task(20, id_=task_id2, name="Task 2")
        pool.add(task)

        self.assertEqual(pool.get(task_id2), task)

    def test_task_already_exists(self):
        same_id = "same-id"

        task = Task(10, id_=same_id, name="Task 1")
        pool = Pool(children=[task], name="Pool 1")

        task2 = Task(20, id_=same_id, name="Task 2")

        with self.assertRaises(ValueError):
            pool.add(task2)

    def test_parenting(self):
        task_id = "there-is-some-id"

        task = Task(10, id_=task_id, name="Task 1")
        pool = Pool(children=[task], name="Pool 1")

        self.assertEqual(task.parent, pool)

        pool.pop(task_id)

        self.assertIsNone(task.parent)

        new_pool = Pool(name="Pool 2")

        pool.add(new_pool)
        self.assertEqual(new_pool.parent, pool)

        pool.pop(new_pool.id)
        self.assertIsNone(new_pool.parent)

    def test_iter(self):
        tasks = [Task(f"Task {i}", i, id_=i) for i in range(5)]
        pool = Pool(children=tasks, name="Pool 1")

        for task in pool:
            self.assertIn(task, tasks)

        self.assertEqual(len(pool), len(tasks))

    def test_is_solved(self):
        tasks = [Task(f"Task {i}", i, id_=i) for i in range(5)]
        pool = Pool(children=tasks, name="Pool 1")

        self.assertFalse(pool.is_solved)

        for task in tasks:
            task.spent = task.cost

        self.assertTrue(pool.is_solved)

    def test_done(self):
        task1 = Task(10, name="Task 1")
        task1.spent = 10

        task2 = Task(20, name="Task 2")

        pool = Pool(children=[task1, task2], name="Pool 1")

        self.assertEqual(list(pool.done), [task1])
        self.assertEqual(list(pool.todo), [task2])

    def test_composite(self):
        task1 = Task(10, name="Task 1")
        task2 = Task(20, name="Task 2")
        task2.spent = 20
        pool1 = Pool(children=[task1, task2], name="Pool 1")

        task3 = Task(30, name="Task 3")
        task4 = Task(40, name="Task 4")
        pool2 = Pool(children=[task3, task4], name="Pool 2")

        task5 = Task(50, name="Task 5")
        task6 = Task(60, name="Task 6")
        task6.spent = 60

        root_pool = Pool(
            children=[pool1, pool2, task5, task6], name="Root Pool"
        )

        self.assertFalse(root_pool.is_solved)

        self.assertEqual(list(root_pool.todo), [pool1, pool2, task5])
        self.assertEqual(list(root_pool.done), [task6])

        # make the first pool solved
        task1.spent = 10
        self.assertEqual(list(root_pool.todo), [pool2, task5])

        # make the second pool solved
        task3.spent = 30
        task4.spent = 40
        self.assertEqual(list(root_pool.todo), [task5])

        # make the last task solved
        task5.spent = 50
        self.assertTrue(root_pool.is_solved)

        self.assertEqual(list(root_pool.done), [pool1, pool2, task5, task6])
        self.assertEqual(list(root_pool.todo), [])

    def test_composite_iter(self):
        task1 = Task(10, name="Task 1")
        task2 = Task(20, name="Task 2")

        pool1 = Pool(children=[task1, task2], name="Pool 1")

        task3 = Task(30, name="Task 3")

        root_pool = Pool(children=[pool1, task3], name="Root Pool")
        self.assertEqual(list(root_pool), [pool1, task3])
