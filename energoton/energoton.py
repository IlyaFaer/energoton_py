class Energoton:
    def __init__(self, id_, name, capacity):
        self.id = id_
        self.name = name
        self.capacity = capacity
        self.energy_left = capacity

    def can_solve(self, task):
        if (
            self.energy_left > 0
            and self.energy_left >= task.todo
            and not task.is_blocked
            and task.is_actual
        ):
            return True
        return False

    def work(self, task):
        energy_spent = min(self.energy_left, task.todo)
        task.spent += energy_spent
        self.energy_left -= energy_spent
        return energy_spent

    def _build_plans(self, task, plan, tasks, plans):
        if task is not None:
            energy_spent = self.work(task)
            plan.append(task)
            tasks.remove(task)

        can_continue = False
        for t in tasks:
            if self.can_solve(t):
                self._build_plans(t, plan, tasks, plans)
                can_continue = True

        if not can_continue:
            plans.add(tuple(sorted(plan, key=lambda t: t.id)))

        if task is not None:
            tasks.append(task)
            plan.remove(task)
            self.energy_left += energy_spent
            task.spent -= energy_spent

    def build_plans(self, pool):
        plans = set()

        self._build_plans(task=None, plan=[], tasks=pool.flat_tasks(), plans=plans)
        return plans
