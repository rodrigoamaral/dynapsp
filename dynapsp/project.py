from dynapsp.core import Entity, Repository

class Task(Entity):
    def __init__(self, oid):
        Entity.__init__(self, oid)
        self._skills = set()

    
    @property
    def skills(self):
        return self._skills
    
    
    def add_skill(self, skill):
        self.skills.add(skill)


    def missing_skills(self, *skillset):
        return self.skills.difference(*skillset)



class Employee(Entity):
    def __init__(self, oid):
        Entity.__init__(self, oid)
        self._skills = set()

    def add_skill(self, skill):
        self.skills.add(skill)

    @property
    def skills(self):
        return self._skills


class Project():
    def __init__(self):
        self._tasks = Repository()
        self._employees = Repository()

    @property
    def tasks(self):
        return self._tasks

    @property
    def employees(self):
        return self._employees

    def add_task(self, task):
        self.tasks.add(task)
    
    def add_employee(self, employee):
        self.employees.add(employee)

