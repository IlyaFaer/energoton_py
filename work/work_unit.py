import abc

from base.mixins import IdMixin

from .priority import NoPriority
from .relation import Alternative, Blocking


class WorkUnit(IdMixin, metaclass=abc.ABCMeta):
    def __init__(
        self,
        custom_fields={},
        parent=None,
        priority=NoPriority(),
        id_=None,
        name=None,
    ):
        super().__init__(id_)

        self.custom_fields = custom_fields
        self.name = name
        self.relations = {}
        self.priority = priority
        self.parent = parent

    @abc.abstractmethod
    def is_solved(self):
        raise NotImplementedError(
            "is_solved method must be implemented for any work unit!"
        )

    def __delitem__(self, key):
        del self.custom_fields[key]

    def __getitem__(self, key):
        return self.custom_fields[key]

    def __setitem__(self, key, value):
        self.custom_fields[key] = value

    @property
    def blocked_by(self):
        for rel in self.relations.values():
            if (
                isinstance(rel, Blocking)
                and rel.blocked == self
                and not rel.blocker.is_solved
            ):
                yield rel

    @property
    def blocking(self):
        for rel in self.relations.values():
            if (
                isinstance(rel, Blocking)
                and rel.blocker == self
                and not self.is_solved
            ):
                yield rel

    @property
    def is_actual(self):
        for rel in self.relations.values():
            if isinstance(rel, Alternative) and rel.is_solved:
                return False

        return True

    @property
    def is_blocked(self):
        try:
            next(self.blocked_by)
            return True
        except StopIteration:
            return self.parent.is_blocked if self.parent else False
