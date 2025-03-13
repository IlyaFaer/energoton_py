from base.mixins import IdMixin

from .priority import NoPriority
from .work_unit import WorkUnit


class WorkDone(IdMixin):
    def __init__(self, id_, task, energy_spent, assignee, cycle=1):
        self.task = task
        self.amount = energy_spent
        self.assignee = assignee
        self.cycle = cycle

        super().__init__(id_)

    def __repr__(self):
        return f"WorkDone(task={self.task}, amount={self.amount}, cycle={self.cycle})"

    def __eq__(self, other):
        return (
            self.task == other.task
            and self.amount == other.amount
            and self.assignee == other.assignee
        )

    def drop(self):
        self.task.drop_work_done(self)


class Task(WorkUnit):
    def __init__(
        self,
        cost,
        custom_fields={},
        parent=None,
        priority=NoPriority(),
        id_=None,
        name=None,
    ):
        self._work_done = []
        self.cost = cost

        super().__init__(custom_fields, parent, priority, id_, name)

    def __repr__(self):
        return f"Task(name='{self.name}', cost={self.cost})"

    @property
    def spent(self):
        return sum(w.amount for w in self._work_done)

    @property
    def is_solved(self):
        return self.spent == self.cost

    @property
    def todo(self):
        return self.cost - self.spent

    def drop_work_done(self, energy_spent):
        self._work_done.remove(energy_spent)

    def work_done(self, energy_spent, energoton, cycle=1):
        work_done = WorkDone(
            str(self.id) + "-work_done-" + str(len(self._work_done) + 1),
            self,
            energy_spent,
            energoton,
            cycle,
        )
        self._work_done.append(work_done)
        return work_done
