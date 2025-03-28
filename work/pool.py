from .work_unit import Priority, WorkUnit


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
        for c in children:
            c.parent = self
            if c.id in self.children:
                raise ValueError(
                    f"Child '{c.name}' with id '{c.id}' already exists in the pool {self.name}."
                )

            self.children[c.id] = c

        super().__init__(custom_fields, parent, priority, id_, name)

    def __iter__(self):
        return iter(self.children.values())

    def __len__(self):
        return len(self.children)

    def __repr__(self):
        return f"Pool(id={self.id}, name={self.name})"

    @property
    def dry(self):
        return {t.id: t.dry for t in self.flat_tasks()}

    @property
    def done(self):
        for t in filter(lambda c: c.is_solved, self.children.values()):
            yield t

    @property
    def is_solved(self):
        for c in self.children.values():
            if not c.is_solved:
                return False

        return True

    @property
    def todo(self):
        for t in filter(lambda c: not c.is_solved, self.children.values()):
            yield t

    def add(self, child):
        if child.id in self.children:
            raise ValueError(
                f"Child with id '{child.id}' already exists in the pool {self.id}."
            )

        child.parent = self
        self.children[child.id] = child

    def flat_tasks(self):
        tasks = []
        for c in self.children.values():
            if isinstance(c, Pool):
                tasks.extend(c.flat_tasks())
            else:
                if not c.is_solved:
                    tasks.append(c)

        return tasks

    def get(self, child_id):
        if child_id in self.children:
            return self.children[child_id]

        for task in self.flat_tasks():
            if task.id == child_id:
                return task

    def pop(self, child_id):
        if child_id in self.children:
            child = self.children[child_id]
            self.children[child_id].parent = None
            del self.children[child_id]

        for task in self.flat_tasks():
            if task.id == child_id:
                child = task.parent.pop(task.id)

        return child

    @property
    def as_dict(self):
        dict_ = {}
        for t in self.flat_tasks():
            dict_[t.id] = t

        return dict_
