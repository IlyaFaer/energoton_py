from base.mixins import IdMixin

from .priority import NoPriority
from .work_unit import WorkUnit


class PartTask(IdMixin):
    def __init__(self, id_, task, part_done):
        self.task = task
        self.part_done = part_done

        super().__init__(id_)

    def __getattr__(self, name):
        if name == "part_done":
            return self.part_done
        return getattr(self.task, name)

    def __repr__(self):
        return f"PartTask(task={self.task}, part_done={self.part_done})"

    def drop(self):
        self.task.spent -= self.part_done
        self.task.drop_part(self)


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
        self._parts = []
        self.spent = 0

        self.cost = cost

        super().__init__(custom_fields, parent, priority, id_, name)

    def __repr__(self):
        return f"Task(name={self.name}, cost={self.cost}, spent={self.spent})"

    @property
    def is_solved(self):
        return self.spent == self.cost

    @property
    def todo(self):
        return self.cost - self.spent

    def drop_part(self, part):
        self._parts.remove(part)

    def part(self, part_done):
        part = PartTask(
            str(self.id) + "-part-" + str(len(self._parts) + 1),
            self,
            part_done,
        )
        self._parts.append(part)
        return part
