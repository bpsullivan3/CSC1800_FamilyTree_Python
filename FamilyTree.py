"""
Author: Patrick Sullivan

A class to keep track of and manage a family tree of Person objects
"""


class FamilyTree:
    def __init__(self):
        """
        A Family tree is simply a dictionary with strings as keys and Persons as values
        """
        self.tree = {}

    def add_person(self, person):
        """
        Add a new person to the tree with their name as the key

        :param person:
        :return:
        """
        self.tree[person.get_name()] = person

    def get_person(self, name):
        """
        Return the person from the tree with the given name.
        If that name is not in the tree, return None

        :param name:
        :return:
        """
        if name not in self.tree:
            return None
        else:
            return self.tree[name]

    def get_cousins(self, person):
        """
        Iterate through every member of the tree and check if they are a cousin of the given person.

        :param person:
        :return: list of strings
        """
        cousins = list()
        for entry in self.tree:
            if person.is_cousin(self.tree[entry]):
                cousins.append(entry)
        cousins.sort()
        return cousins

    def get_unrelated(self, person):
        """
        Iterate through every member of the tree and check if they are unrelated to the given person.

        :param person:
        :return: list of strings
        """
        unrelated = list()
        for entry in self.tree:
            if person.is_unrelated(self.tree[entry]):
                unrelated.append(entry)
        unrelated.sort()
        return unrelated
