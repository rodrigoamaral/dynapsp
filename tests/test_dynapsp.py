
"""Tests for `dynapsp` package."""

import pytest
from dynapsp.project import Project, Task, Employee


@pytest.fixture
def task():
    t = Task(1)
    t.add_skill(1)
    t.add_skill(2)
    t.add_skill(3)
    t.add_skill(4)
    t.add_skill(5)
    return t


@pytest.fixture
def employee():
    e = Employee(1)
    e.add_skill(1)
    e.add_skill(2)
    e.add_skill(3)
    return e


def test_create_project():
    assert Project()


def test_create_task():
    t = Task(1)
    assert t.oid == 1


def test_add_task():
    p = Project()
    p.add_task(Task(1))
    assert p.tasks[1].oid == 1


def test_add_employee():
    p = Project()
    p.add_employee(Employee(1))
    assert p.employees[1].oid == 1


def test_add_skill_to_task(task):
    assert 1 in task.skills


def test_add_skill_to_employee(employee):
    assert 1 in employee.skills


def test_task_missing_skills(task):
    assert task.missing_skills({1, 3}) == {2, 4, 5}


def test_task_missing_skills_multiple(task):
    assert task.missing_skills({1}, {2, 3}) == {4, 5}


def test_task_employee_missing_skills_(task, employee):
    assert task.missing_skills(employee.skills) == {4, 5}

