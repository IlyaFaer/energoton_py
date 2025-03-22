**energoton_py** is a Python package that automates task planning. Init workers with energy capacity, create tasks with energy cost, and the package will build possible work plans, considering priorities and relations between tasks.

## About
**What's energoton?**  
Energoton is a formal model similar to automatons. Imagine an abstract machine with a limited amount of energy and ability to solve abstract tasks, by spending that energy. This is energoton. It's goal is to walk through the given pool of tasks and find optimal resolution plans.

**Okay, how can I use it?**  
<u>Example 1</u>: You have a team of 5 developers, on average 15 standing tasks and you need to plan scrum sprints every week, considering priorities. Energotons can plan those sprints automatically.

<u>Example 2</u>: You're developing a game NPC, which is supposed to be able to plan their actions, considering alternatives. Create a bunch of tasks, linked to each other through "Alternative" relations, and energoton will find the best of variants.

<u>Example 3</u>: You have a microservice, which solves queued tasks (scraping, aggregation, etc.). As tasks are monotonous, you know their cost, so, with energoton, you can make the service work smarter by ordering tasks, instead of going through them blindly.

So, shortly, energotons are abstract enough for a wide range of tasks - if there is planning, they'll will give you a shoulder.

**Curious, is it an AI?**  
No. You don't need to train it, only load tasks and workers data. You're free to connect any AI to it as a secondary system though.

# Use Basics
**Task**  
Task is an atomic piece of work to do. Its only required attribute is `cost` - a simple `int`, which represents the amount of energy that must be spent to solve the task.

```python
t = Task(
    cost=4,  # e.g. the task takes 4 hours to solve
    custom_fields={"date_due": "2025-03-15"},
    name="Task name",
)

# your custom_fields are available by their keys
t["date_due"]
```

**Energoton**  
Energoton is a worker that can solve tasks by spending energy. Easy to guess, its required attribute is energy capacity.

```python
e1 = DeterministicEnergoton(
    capacity=8,  # e.g. 8 hours long work day
    name="Energoton 1",
)
e2 = NonDeterministicEnergoton(
    capacity=8,
    name="Energoton 2",
)
```
The package supports two types of energotons, designed for different cases:  
  
* _DeterministicEnergoton_ will work on a task only if it has enough energy to solve it, without any partial conditions.
* _NonDeterministicEnergoton_ can solve a given task partially, putting its energy into the task as a contribution.
  
**Pool**  
A pool represents a group of tasks. It can be a sprint, a project, or just a complex task, which consists of several subtasks. Pools can be embedded into each other for a more complex hierarchy.

```python
t1 = Task(cost=4)
t2 = Task(cost=6)
t3 = Task(cost=3)

pool = Pool(
    children=[t1, t2],
    name="Pool 1"
)

root_pool = Pool()
root_pool.add(pool)
root_pool.add(t3)

t1 = root_pool.get(t1.id)
root_pool.pop(pool.id)
```

**Planner**  
Now, when we are shortly introduced to the main elements, we can start planning our work:
```python
planner = Planner(
    # e.g. a team of 3 employees
    energotons=[
        DeterministicEnergoton(8),
        DeterministicEnergoton(8),
        DeterministicEnergoton(8),
    ],
    # tasks to be done
    pool=Pool(
        children=[
            Task(3),
            Task(5),
            Task(1),
            Task(4),
        ]
    )
)

# build all possible plans
planner.build_plans()

# filter through plans to find the best ones
plans = planner.filter_plans(
    # order the plans by descendance of the amount
    # of tasks solved in the plan
    sort_by="value",
    # return only plans with the most tasks solved
    only_best=True,
)
```
**Cycles**  
Work cycle represents an abstract time unit, during which energotons are working. It may be a work day, a sprint, an entire month - you're free to choose the scale. After a cycle is ended, the planner will recharge energotons, so they could continue working. You can control charges.
```python
e = DeterministicEnergoton(
    # 5 work days, 8 hours each,
    # Tue is a day-off
    capacity=[8, 0, 8, 8, 8]
)

planner = Planner(
    energotons=[e],
    pool=some_pool,
)

plans = planner.build_plans(cycles=5)
```

**WorkDone**  
A plan built by a planner consists of `WorkDone` objects, each of which represents a piece of planned work with the following fields:
* *task* - target task
* *energy_spent* - amount of energy that's going to be spent
* *assignee* - energoton that's going to spend this energy
* *cycle* - number of the work cycle, at which work is planned to be done

**Advanced Features**  
The package includes more interesting functionality e.g. **Relations**, which allow to run planning in more complex cases. To see how they work (with detailed comments), check out the [samples](https://github.com/IlyaFaer/energoton/tree/main/samples).

## Early Version Warning
This package is in early **beta** development stage. It may contain errors, performance issues, inconveniences and can introduce breaking changes. Use it cautiously and report any findings and ideas.

## Development Plan
As the package is quite raw, some time will be spent to sharpen it, fix mistakes, improve performance and documentation. Star the repository and stay tuned, as there is more to come.  

When the package is stable, a PyPl release is going to be made.  
  
Next, there is a plan to implement a REST API on a fast programming language (it'll be Go, most likely) with a database and put build a Docker image, to make it possible for users to easily unroll a language-independent microservice based on energotons.  

## What's Next
* Read the Energoton formal model [specification](https://docs.google.com/document/d/1qSr1LRrfzFkJYoJUsLwi7DLwz6v3poVYMY_cnEyMLn8/edit?usp=sharing) for comprehensive understanding
* Study [the License](https://github.com/IlyaFaer/energoton_py/blob/main/LICENSE.md) to check the appropriate use cases
