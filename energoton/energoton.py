import copy

from base.mixins import IdMixin
from work import WorkDone
from .planner import Plan


class Energoton(IdMixin):
    def __init__(self, capacity, id_=None, name=None):
        self.name = name
        self.capacity = capacity
        self.energy_left = capacity

        super().__init__(id_)

    def _build_plans(self, task, plan, tasks, plans):
        if task is not None:
            work_done = self.work(task)
            plan.append(work_done)
            if task.is_solved:
                tasks.remove(task)

        can_continue = False
        for t in copy.copy(tasks):
            if self.can_solve(t):
                self._build_plans(t, plan, tasks, plans)
                can_continue = True

        if not can_continue:
            plans.append(copy.copy(plan))

        if task is not None:
            if task.is_solved:
                tasks.append(task)

            plan.remove(work_done)
            self.energy_left += work_done.amount

            work_done.drop()

    def build_plans(self, pool):
        plans = []
        self._build_plans(
            task=None, plan=Plan(), tasks=pool.flat_tasks(), plans=plans
        )
        return plans

    def work(self, task):
        energy_spent = min(self.energy_left, task.todo)
        self.energy_left -= energy_spent
        work_done = task.work_done(energy_spent, self)

        return work_done


class DeterministicEnergoton(Energoton):
    def can_solve(self, task):
        if (
            self.energy_left > 0
            and self.energy_left >= task.todo
            and not task.is_blocked
            and task.is_actual
        ):
            return True
        return False


class NonDeterministicEnergoton(Energoton):
    def can_solve(self, task):
        if self.energy_left > 0 and not task.is_blocked and task.is_actual:
            return True
        return False
