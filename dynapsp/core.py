class Entity():
    def __init__(self, oid):
        self._oid = oid

    @property
    def oid(self):
        return self._oid


class Repository(dict):
    def add(self, entity):
        self[entity.oid] = entity
