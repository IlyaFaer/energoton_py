from .work_unit import Priority, WorkUnit
from .task import Task


class Pool(WorkUnit):
    def __init__(
        self,
        custom_fields={},
        parent=None,
        priority=Priority("normal"),
        children=[],
        id_=None,
        name=None,
    ):
        self.children = {}
        self._indexate_pool(children)

        super().__init__(custom_fields, parent, priority, id_, name)

    def _indexate_pool(self, pool):
        for c in pool:
            if c.id in self.children:
                raise ValueError(
                    f"Child '{c.name}' with id '{c.id}' already exists in the pool {self.name}."
                )

            if isinstance(c, Pool):
                self._indexate_pool(c)

            if not c.parent:
                c.parent = self

            self.children[c.id] = c

    def __iter__(self):
        return iter(filter(lambda c: c.parent == self, self.children.values()))

    def __len__(self):
        return len(self.children)

    def __repr__(self):
        return f"Pool(id={self.id}, name={self.name})"

    @property
    def dry(self):
        return {t.id: t.dry for t in self.flat_tasks()}

    @property
    def done(self):
        for t in filter(
            lambda c: c.is_solved and c.parent == self, self.children.values()
        ):
            yield t

    @property
    def is_solved(self):
        for c in self.children.values():
            if not c.is_solved:
                return False

        return True

    @property
    def todo(self):
        for t in filter(
            lambda c: not c.is_solved and c.parent == self,
            self.children.values(),
        ):
            yield t

    def add(self, child):
        if child.id in self.children:
            raise ValueError(
                f"Child with id '{child.id}' already exists in the pool {self.id}."
            )

        child.parent = self
        self.children[child.id] = child

        if isinstance(child, Pool):
            self._indexate_pool(child)

    def flat_tasks(self):
        return filter(
            lambda c: isinstance(c, Task) and not c.is_solved,
            self.children.values(),
        )

    def get(self, child_id):
        return self.children.get(child_id)

    def pop(self, child_id):
        child = self.children[child_id]
        if child.parent != self:
            child.parent.pop(child_id)

        self.children[child_id].parent = None
        del self.children[child_id]

        return child
