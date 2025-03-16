"""
This sample shows how to use a single task.

Task is an atomic piece of work to be done.
"""

import datetime

from work import Task


t1 = Task(
    cost=4,
    custom_fields={
        "description": "Implement a loading bar for the photo loading screen",
        "due_date": datetime.date(2025, 6, 3),
        "reporter": "Catlin Whiskas",
    },
    name="Photo Loading Screen",
)

print("Task:", t1)

# Task cost indicates how much energy
# is required to complete the task.
# It's up to you to decide what a single
# unit of cost represents: seconds - if
# it's a microservice, hours - if it's
# about alive employees, scrum story points
# - if it's about some development
# methodology, turns - if it's a turn-based
# video game, etc.
print("Cost: ", t1.cost)

# Indicates if the task is solved.
print("Task is solved: ", t1.is_solved)

# The amount of energy to be spent to
# solve the task. Useful with non-deterministic
# energotons, which can solve a task partially.
print("Work to do: ", t1.todo)

# The amount of energy already spent on the task.
# Useful with non-deterministic energotons,
# which can solve a task partially.
print("Work done: ", t1.spent)

# Custom fields that you add to the task, are
# available by their keys to help you to
# incorporate the task into your workflow.
print("Description: ", t1.custom_fields["description"])
print("Due date: ", t1.custom_fields["due_date"])
