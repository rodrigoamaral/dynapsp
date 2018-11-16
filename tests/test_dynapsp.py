"""Tests for `dynapsp` package."""

import pytest
from dynapsp.project import Project, Task, Employee, InvalidDependencyError, ProjectEvent


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


@pytest.fixture
def minimum_project():
    p = Project()
    p.add_task(Task(1))
    p.add_task(Task(2))
    p.add_employee(Employee(1))
    p.add_employee(Employee(2))
    return p


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


def test_add_dependency_to_tpg(minimum_project):
    p = minimum_project
    p.add_dependency(1, 2)
    assert (
        (p.tpg.number_of_nodes() == 2)
        and (p.tpg.number_of_edges() == 1)
        and ((1, 2) in p.tpg.edges)
    )


def test_add_dependency_with_missing_task(minimum_project):
    p = minimum_project
    with pytest.raises(InvalidDependencyError):
        p.add_dependency(1, 3)


def test_task_add_finished_effort():
    t = Task(1, initial_effort=10)
    t.add_finished_effort(2)
    assert t.remaining_effort == 8


def test_task_add_finished_effort_greater_than_remaining():
    t = Task(1, initial_effort=10)
    t.add_finished_effort(13)
    assert t.remaining_effort == 0


def test_calculate_employee_payment():
    e = Employee(1, max_dedication=1.1, normal_salary=1000, overtime_salary=2000)
    assert e.payment(2, 1.1) == pytest.approx(2400)


def test_employee_no_dedication_payment():
    e = Employee(1, max_dedication=1.1, normal_salary=1000, overtime_salary=2000)
    assert e.payment(2, 0) == pytest.approx(0)


def test_employee_no_work_payment():
    e = Employee(1, max_dedication=1.1, normal_salary=1000, overtime_salary=2000)
    assert e.payment(0, 1.1) == pytest.approx(0)


def test_employee_overdedication_payment():
    e = Employee(1, max_dedication=1.1, normal_salary=1000, overtime_salary=2000)
    assert e.payment(2, 1.5) == pytest.approx(2400)


def test_employee_underdedication_payment():
    e = Employee(1, max_dedication=1.1, normal_salary=1000, overtime_salary=2000)
    assert e.payment(2, 0.5) == pytest.approx(1000)


def test_empty_timeline(minimum_project):
    p = minimum_project
    assert len(p.timeline) == 0


def test_add_event_to_timeline(minimum_project):
    p = minimum_project
    p.add_event(ProjectEvent(0.75))
    assert len(p.timeline) > 0 and isinstance(p.timeline[0], ProjectEvent)


def test_events_within_interval(minimum_project):
    p = minimum_project
    p.add_event(ProjectEvent(0.75))
    p.add_event(ProjectEvent(1.2))
    p.add_event(ProjectEvent(2.1))
    p.add_event(ProjectEvent(3.3))
    events = p.events_within_interval(1, 3)
    assert len(events) == 2 and all(n in [ev.instant for ev in events] for n in [1.2, 2.1])
