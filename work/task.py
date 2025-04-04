"""Task represents a single unit of work to be done."""

from .work_unit import Priority, WorkUnit


class Task(WorkUnit):
    """A piece of work to do.

    Args:
        cost (int):
            Energy cost of the task.
        custom_fields (Optional[Dict[str: Any]]):
            Custom fields for additional task info.
            Can be accessed by keys:
            >>> task['field_name']
        parent (Optional[work.pool.Pool]):
            Parent pool.
        priority (Optional[Priority]):
            Priority of the task. Defaults to "medium" priority.
        id_ (Optional[str | uuid.UUID]):
            Id of the task. Generated, if not provided explicitly.
        name (Optional[str]):
            Name of the task.
    """

    def __init__(
        self,
        cost,
        custom_fields={},
        parent=None,
        priority=Priority("normal"),
        id_=None,
        name=None,
    ):
        self.work_done = []
        self.cost = cost

        super().__init__(custom_fields, parent, priority, id_, name)

    def __repr__(self):
        """Textual representation of the task.

        Returns:
            str: Textual representation of the task.
        """
        return f"Task(id_='{self.id}', name='{self.name}', cost={self.cost})"

    @property
    def dry(self):
        """Short form of the task, used during plan building.

        Returns:
            dict: Short form of the task.
        """
        return {
            "id": self.id,
            "cost": self.cost,
            "spent": self.spent,
            "priority": self.priority,
        }

    @property
    def spent(self):
        """Amount of energy spent on the task.

        Returns:
            int: Energy spent on the task.
        """
        return sum(w.amount for w in self.work_done)

    @property
    def is_solved(self):
        """Check if the task is solved.

        Returns:
            bool: True if the task is solved, False otherwise.
        """
        return self.spent == self.cost

    @property
    def todo(self):
        """Amount of energy left to be spent on the task.

        Returns:
            int: Energy left to be spent on the task.
        """
        return self.cost - self.spent
