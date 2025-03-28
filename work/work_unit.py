"""Base functionality for work units.

The difference between WorkUnit and WorkDone:
- WorkUnit represents a task/pool of tasks.
- WorkDone represents a piece of work done on a task.
"""

import abc

from base import Id

from .relation import Alternative, Blocking


class Priority:
    exp_values = {
        "lowest": 1,
        "low": 2,
        "normal": 4,
        "high": 8,
        "highest": 16,
    }

    def __init__(self, label):
        self.label = label
        self.value = self.exp_values[label]

    def __repr__(self):
        return f"Priority('{self.label}')"


class WorkUnit(Id, metaclass=abc.ABCMeta):
    """Represents a single work unit to do. Can be a task or a pool.

    Args:
        custom_fields (Optional[Dict[str: Any]]):
            Custom fields for the work unit. Can be accessed by keys:
            >>> work_unit['field_name']
        parent (Optional[work.pool.Pool]):
            Parent pool.
        priority (Optional[Union[
            Priority,
            CustomPriority,
        ]]):
            Priority of the work unit. Defaults to "medium" priority.
        id_ (Optional[str | uuid.UUID]):
            Id of the work unit. Generated, if not provided explicitly.
        name (Optional[str]):
            Name of the work unit.
    """

    def __init__(
        self,
        custom_fields=None,
        parent=None,
        priority=Priority("normal"),
        id_=None,
        name=None,
    ):
        super().__init__(id_)

        self.custom_fields = custom_fields or {}
        self.name = name
        self.relations = {}
        self.priority = priority
        self.parent = parent

    @abc.abstractmethod
    def is_solved(self):
        """Check if the work unit is solved.

        Raises:
            NotImplementedError:
                Must be implemented for any work unit.
        """
        raise NotImplementedError(
            "is_solved method must be implemented for any work unit!"
        )

    def __delitem__(self, key):
        """Magic method for a custom field deletion.

        Args:
            key (str): Field name.
        """
        del self.custom_fields[key]

    def __getitem__(self, key):
        """Magic method for a custom field access.

        Args:
            key (str): Field name.

        Returns:
            Any: Custom field value.
        """
        return self.custom_fields[key]

    def __setitem__(self, key, value):
        """Magic method for a custom field setting."

        Args:
            key (str): Field name.
            value (Any): Field value.
        """
        self.custom_fields[key] = value

    @property
    def blocked_by(self):
        """
        Return all relations that prevent this work
        unit from being done.

        Yields:
            work.relation.Blocking: Blocking relations.
        """
        for rel in self.relations.values():
            if (
                isinstance(rel, Blocking)
                and rel.blocked == self
                and not rel.blocker.is_solved
            ):
                yield rel

    @property
    def blocking(self):
        """
        Return all relations where this work unit
        prevents other units from being solved.

        Yields:
            work.relation.Blocking: Blocking relations.
        """
        for rel in self.relations.values():
            if (
                isinstance(rel, Blocking)
                and rel.blocker == self
                and not self.is_solved
            ):
                yield rel

    @property
    def is_actual(self):
        """Check if this unit still needs to be solved.

        Returns:
            bool:
                True if the unit is not solved and its
                alternatives are not solved as well.
        """
        for rel in self.relations.values():
            if isinstance(rel, Alternative) and rel.is_solved:
                return False

        return True

    @property
    def is_blocked(self):
        """Check if this unit is blocked by another unit.

        Returns:
           bool: True if the unit is blocked, False otherwise.
        """
        try:
            next(self.blocked_by)
            return True
        except StopIteration:
            return self.parent.is_blocked if self.parent else False


class WorkDone(Id):
    """Represents a log of some work being done in some plan.

    NOTE: It can represent a part of task being done -
        not necessarily an entire task being solved.

    Args:
        id_ (Optional[str | uuid.UUID]):
            Log id. Generated, if not provided explicitly.
        task (work.task.Task):
            Task that was worked on.
        energy_spent (int):
            Amount of energy spent on the task during this
            piece of work.
        assignee (work.energoton.Energoton):
            Energoton that did the work.
        cycle (int):
            Cycle number of the work cycle. Defaults to 1.
    """

    def __init__(self, id_, task, energy_spent, assignee, cycle=1):
        self.task = task
        self.amount = energy_spent
        self.assignee = assignee
        self.cycle = cycle

        super().__init__(id_)

    def __eq__(self, other):
        """Magic method for the equality operator.

        Returns:
            bool: True if the objects are equal, False otherwise.
        """
        return (
            self.task.id == other.task.id
            and self.amount == other.amount
            and self.assignee == other.assignee
            and self.cycle == other.cycle
        )

    def __hash__(self):
        """Magic method for the hash function.

        Returns:
            int: Object hash.
        """
        return hash(self.id)

    def __repr__(self):
        """Textual representation of the work piece.

        Returns:
            str: Textual representation.
        """
        return (
            f"WorkDone(task={self.task}, amount={self.amount},"
            f" cycle={self.cycle}, assignee='{self.assignee.id}')"
        )

    @property
    def dry(self):
        return (self.task.id, self.amount)
