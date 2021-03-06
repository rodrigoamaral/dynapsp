import numpy as np
import networkx as nx

from dynapsp.core import Entity, Repository


class Task(Entity):
    def __init__(self, oid, initial_effort=0):
        Entity.__init__(self, oid)
        self._skills = set()
        self._effort = initial_effort
        self._finished_effort = 0

    @property
    def skills(self):
        return self._skills

    @property
    def effort(self):
        return self._effort

    @property
    def remaining_effort(self):
        remaining = self._effort - self._finished_effort
        if remaining < 0:
            return 0
        return remaining

    def add_skill(self, skill):
        self.skills.add(skill)

    def missing_skills(self, *skillset):
        return self.skills.difference(*skillset)

    def add_finished_effort(self, finished_effort):
        self._finished_effort += finished_effort


class Employee(Entity):
    def __init__(self, oid, max_dedication=0, normal_salary=0, overtime_salary=0):
        Entity.__init__(self, oid)
        self._skills = set()
        self._max_dedication = max_dedication
        self._normal_salary = normal_salary
        self._overtime_salary = overtime_salary

    @property
    def skills(self):
        return self._skills

    def add_skill(self, skill):
        self.skills.add(skill)

    def payment(self, duration, dedication):
        ded = min(dedication, self._max_dedication)
        normal_dedication = min(1, ded)
        over_dedication = max(0, ded - 1)
        regular_payment = self._normal_salary * normal_dedication * duration
        overtime_payment = self._overtime_salary * over_dedication * duration
        return regular_payment + overtime_payment


class ProjectEvent:
    def __init__(self, instant):
        self._instant = instant

    @property
    def instant(self):
        return self._instant


class DedicationMatrix:
    def __init__(self, e, t):
        self._m = np.zeros((e, t))

    def __getitem__(self, k):
        return self._m[k[0], k[1]]

    @property
    def shape(self):
        return self._m.shape


class Project:
    def __init__(self):
        self._tasks = Repository()
        self._employees = Repository()
        self._tpg = nx.DiGraph()
        self._timeline = []

    @property
    def tasks(self):
        return self._tasks

    @property
    def employees(self):
        return self._employees

    @property
    def tpg(self):
        return self._tpg

    @property
    def timeline(self):
        return self._timeline

    def add_task(self, task):
        self.tasks.add(task)

    def add_employee(self, employee):
        self.employees.add(employee)

    def add_dependency(self, t1, t2):
        for t in [t1, t2]:
            if not self.tasks.get(t):
                raise InvalidDependencyError("Task {} does not exist".format(t))
        self.tpg.add_edge(t1, t2)

    def add_event(self, event):
        self.timeline.append(event)

    def events_within_interval(self, start, finish):
        return [ev for ev in self.timeline if ev.instant >= start and ev.instant <= finish]

    def create_dm(self):
        return DedicationMatrix(len(self.employees), len(self.tasks))


class Error(Exception):
    pass


class InvalidDependencyError(Error):
    pass
