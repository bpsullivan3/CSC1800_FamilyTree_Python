"""
Author: Patrick Sullivan

A class to keep track of and manage a family tree of Person objects
"""


import Person


class FamilyTree:
    def __init__(self):
        self.tree = {}

    def add_person(self, person):
        self.tree[person.get_name()] = person

    def get_person(self, name):
        if name not in self.tree:
            return None
        else:
            return self.tree[name]

    def get_cousins(self, person):
        cousins = list()
        for entry in self.tree:
            if person.is_cousin(self.tree[entry]):
                cousins.append(entry)
        cousins.sort()
        return cousins

    def get_unrelated(self, person):
        unrelated = list()
        for entry in self.tree:
            if person.is_unrelated(self.tree[entry]):
                unrelated.append(entry)
        unrelated.sort()
        return unrelated
