import copy

from base.mixins import IdMixin
from work import PartTask
from .planner import Plan


class Energoton(IdMixin):
    def __init__(self, capacity, id_=None, name=None):
        self.name = name
        self.capacity = capacity
        self.energy_left = capacity

        super().__init__(id_)

    def _build_plans(self, task, plan, tasks, plans):
        if task is not None:
            energy_spent = self.work(task)
            task = self._task_done(task, plan, tasks, energy_spent)

        can_continue = False
        for t in copy.copy(tasks):
            if self.can_solve(t):
                self._build_plans(t, plan, tasks, plans)
                can_continue = True

        if not can_continue:
            # TODO: it should be done in the planner
            # the user may want to see all plans
            # including different order of tasks
            plans.add(tuple(sorted(plan, key=lambda t: t.id)))

        if task is not None:
            if isinstance(task, PartTask):
                if task.is_solved:
                    tasks.append(task.task)
            else:
                tasks.append(task)

            plan.remove(task)
            self.energy_left += energy_spent

            if isinstance(task, PartTask):
                task.drop()
            else:
                task.spent -= energy_spent

    def build_plans(self, pool):
        plans = set()
        self._build_plans(
            task=None, plan=Plan(), tasks=pool.flat_tasks(), plans=plans
        )
        return plans

    def work(self, task):
        energy_spent = min(self.energy_left, task.todo)
        task.spent += energy_spent
        self.energy_left -= energy_spent
        return energy_spent


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

    def _task_done(self, task, plan, tasks, _):
        plan.append(task)
        tasks.remove(task)
        return task


class NonDeterministicEnergoton(Energoton):
    def can_solve(self, task):
        if self.energy_left > 0 and not task.is_blocked and task.is_actual:
            return True
        return False

    def _task_done(self, task, plan, tasks, energy_spent):
        if task.is_solved:
            tasks.remove(task)
        else:
            task = task.part(energy_spent)

        plan.append(task)
        return task
