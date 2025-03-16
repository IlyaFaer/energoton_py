"""This sample shows how use task pools."""

from work import Alternative, Blocking, ExponentialPriority, Pool, Task

t1 = Task(
    cost=4,
    name="Do something 1",
)

t2 = Task(
    cost=5,
    name="Do something 2",
)

t3 = Task(
    cost=1,
    name="Do something 3",
)

# Tasks can be added during pool init.
pool = Pool(
    children=[t1, t2, t3],
    name="Next Sprint",
    custom_fields={"week": 3, "year": 2025, "month": 5},
)

# Pools support custom fields, just like tasks.
assert pool.custom_fields["week"] == 3

# Tasks can be added into an existing pool.
t4 = Task(
    cost=3,
    name="Do something 4",
)

pool.add(t4)

# Tasks have a reference to the parent pool.
assert t4.parent == pool

# Pools have a reference to the parent pool,
# when embedded.
root_pool = Pool(
    children=[pool],
    name="Root Pool",
)

assert pool.parent == root_pool

# A task can be got from the pool by its
# id, even if it's embedded into a child pool.
assert root_pool.get(t4.id) == t4

# A task can be removed from the pool by its id,
# even if it's embedded into a child pool.
pool.pop(t4.id)

# A pool is solved, if all of it tasks are solved.
assert not pool.is_solved

# All the solved tasks can be got from the pool.
assert list(pool.done) == []

# All the unsolved tasks can be got from the pool.
assert list(pool.todo) == [t1, t2, t3]

# All the tasks of the pool can be got in a flat list,
# unrolling the embedded pools.
assert root_pool.flat_tasks() == [t1, t2, t3]

# A pool can be iterated over.
for t in pool:
    print(t)

# When you iterate through a pool, which
# embeds another pool, the embedded pool
# will be returned as is.
assert list(root_pool) == [pool]

# All the tasks of the pool can be got
# as a dict with task ids as keys.
assert pool.children == {
    t1.id: t1,
    t2.id: t2,
    t3.id: t3,
}
