"""This sample shows how to use task pools."""

from work import Pool, Task

t1 = Task(cost=4)
t2 = Task(cost=5)
t3 = Task(cost=1)

# Tasks can be added during pool init.
pool = Pool(
    children=[t1, t2, t3],
    name="Next Sprint",
    custom_fields={"week": 3, "year": 2025, "month": 5},
)

# Pools support custom fields, just like tasks.
print("Custom field: ", pool["week"])

# Tasks can be added into an existing pool.
t4 = Task(cost=3)
pool.add(t4)

# Tasks have a reference to the parent pool.
print("t4 parent pool: ", t4.parent)

# Pools have a reference to the parent pool,
# when embedded.
root_pool = Pool(
    children=[pool],
    name="Root Pool",
)

print("The pool's parent: ", pool.parent)

# A task can be got from the pool by its
# id, even if it's embedded into an embedded pool.
print("Task from the pool by id: ", root_pool.get(t4.id))

# A task can be removed from the pool by its id,
# even if it's embedded into an embedded pool.
pool.pop(t4.id)

# A pool is solved, if all of it tasks are solved.
print("Pool is solved: ", pool.is_solved)

# All the solved tasks can be got from the pool.
print("Solved tasks in the pool: ", list(pool.done))

# All the unsolved tasks can be got from the pool.
print("Unsolved tasks in the pool: ", list(pool.todo))

# A pool can be iterated over.
print("Iterate through the pool:")
for t in pool:
    print(t)

# When you iterate through a pool, which
# embeds another pool, the embedded pool
# will be returned as is.
print(
    "Iterating through a pool, doesn't iterate embedded pools: ",
    list(root_pool),
)

# All the tasks of the pool can be got
# as a dict with task ids as keys.
print("All tasks as a dict: ", pool.children)
