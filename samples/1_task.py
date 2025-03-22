"""
This sample shows how to use a single task.

Task is an atomic piece of work to be done.
"""

import datetime

from work import ExponentialPriority, Pool, Task

# Init a task.
t = Task(
    cost=4,
    custom_fields={
        "description": "Implement a loading bar for the photo uploading screen",
        "due_date": datetime.date(2025, 6, 3),
        "reporter": "Catlin Whiskas",
    },
    name="Photo Loading Screen",
)

print("Task:", t)

# Task cost indicates how much energy
# is required to complete the task.
# It's up to you to decide what the cost
# represents: seconds of microservice
# work, human/hours of alive employees,
# scrum story points, turns in
# turn-based game, etc.
print("Cost: ", t.cost)

print("Task is solved: ", t.is_solved)

# The amount of energy to be spent to
# solve the task. Useful with non-deterministic
# energotons, which can solve a task partially.
print("Work to do: ", t.todo)

# The amount of energy already spent on the task.
# Useful with non-deterministic energotons,
# which can solve a task partially.
print("Work done: ", t.spent)

# Custom fields that you add to the task are
# available by their keys to help you to
# incorporate the task into your workflow
# without too much efforts.
print("Description: ", t["description"])
print("Due date: ", t["due_date"])

t["flagged"] = True
print("Flagged: ", t["flagged"])

# Shows blocking relationships of the
# task, if any.
print("Blocked by: ", list(t.blocked_by))
print("Blocking: ", list(t.blocking))
print("Is blocked: ", t.is_blocked)

# Shows if the task alternative was already
# solved (this, this task is no longer actual).
print("Is actual: ", t.is_actual)

# Additional attributes of a task init.
pool = Pool()
t = Task(
    cost=4,
    # Id is optional. If not provided, it'll
    # be generated as a UUID.
    id_="task-1",
    # A task can be parented to a pool on init.
    parent=pool,
    priority=ExponentialPriority("high"),
)
