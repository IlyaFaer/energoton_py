from .priority import NoPriority
from .relation import Alternative, Blocking


class WorkUnit:
    def __init__(
        self,
        id_,
        name,
        custom_fields={},
        parent=None,
        priority=NoPriority(),
    ):
        self._id = id_
        self.custom_fields = custom_fields
        self.name = name
        self.relations = {}
        self.priority = priority
        self.parent = parent

    @property
    def blocked_by(self):
        rels = []
        for rel in self.relations.values():
            if isinstance(rel, Blocking) and rel.blocked == self:
                rels.append(rel)

        return rels

    @property
    def blocking(self):
        rels = []
        for rel in self.relations.values():
            if isinstance(rel, Blocking) and rel.blocker == self:
                rels.append(rel)

        return rels

    @property
    def is_blocked(self):
        if self.blocked_by:
            return True

        return self.parent.is_blocked if self.parent else False

    @property
    def is_actual(self):
        for rel in self.relations.values():
            if isinstance(rel, Alternative) and rel.is_solved:
                return False

        return True

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, _):
        raise ValueError(f"Object '{self.name}' id is immutable")

    def __getitem__(self, key):
        return self.custom_fields[key]

    def __setitem__(self, key, value):
        self.custom_fields[key] = value

    def __delitem__(self, key):
        del self.custom_fields[key]
