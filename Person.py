"""
Author: Patrick Sullivan

A class to support the members of a family tree
"""


class Person:
    def __init__(self, name, parent1, parent2):
        """
        A constructor for the Person class. If the person has no parents,
        the parent arguments should be None.

        :param name: String
        :param parent1: Person
        :param parent2: Person
        """
        self.name = name  # String
        self.spouses = list()  # List of Strings
        self.parent1 = parent1  # Person
        self.parent2 = parent2  # Person
        self.children = list()  # List of Strings

    def get_name(self):
        return self.name

    def get_spouses(self):
        return self.spouses

    def get_parent1(self):
        return self.parent1

    def get_parent2(self):
        return self.parent2

    def get_children(self):
        return self.children

    def set_name(self, name):
        self.name = name

    def add_spouse(self, spouse):
        self.spouses.append(spouse.get_name())
        self.spouses.sort()

    def set_parent1(self, parent):
        self.parent1 = parent

    def set_parent2(self, parent):
        self.parent2 = parent

    def add_child(self, child):
        self.children.append(child.get_name())
        self.children.sort()

    def get_ancestors(self):
        """
        Recurse through the parents of the person, and gather the list
        of direct ancestors.

        :return: A list of strings of ancestors' names.
        """
        ancestors = list()
        if self.parent1 is None or self.parent2 is None:
            return ancestors
        else:
            ancestors.append(self.parent1.get_name())
            ancestors.append(self.parent2.get_name())
            for person in self.parent1.get_ancestors():
                ancestors.append(person)
            for person in self.parent2.get_ancestors():
                ancestors.append(person)
        ancestors.sort()
        return ancestors

    def get_siblings(self):
        """
        Gather the list of children for each parent, and add them to a list of
        siblings for the current person. Removes the person themselves from the list.

        :return: A list of strings of siblings' names.
        """
        siblings = list()
        if self.parent1 is not None:
            for child in self.parent1.get_children():
                siblings.append(child)
        if self.parent2 is not None:
            for child in self.parent2.get_children():
                if child not in siblings:
                    siblings.append(child)
        siblings.remove(self.name)
        siblings.sort()
        return siblings

    def is_child(self, person2):
        """
        Check if this person is a direct child of the given person

        :param person2: Person
        :return: Boolean
        """
        if self.parent1 is None or self.parent2 is None:
            return False
        return self.parent1.equals(person2) or self.parent2.equals(person2)

    def is_spouse(self, person2):
        """
        Check if this person is the spouse of the given person,
        including ex-spouses

        :param person2: Person
        :return: Boolean
        """
        return person2.get_name() in self.spouses

    def is_sibling(self, person2):
        """
        Check if this person is a sibling of the given person,
        including half-siblings

        :param person2: Person
        :return: Boolean
        """
        if self.equals(person2):
            return False
        elif person2.get_parent1() is None or person2.get_parent2() is None:
            return False
        elif self.parent1 is not None \
                and (self.parent1.equals(person2.get_parent1())
                     or self.parent1.equals(person2.get_parent2())):
            return True
        elif self.parent2 is not None \
                and (self.parent2.equals(person2.get_parent1())
                     or self.parent2.equals(person2.get_parent2())):
            return True
        else:
            return False

    def is_ancestor(self, person2):
        """
        Check if this person is the ancestor of the given person

        :param person2: Person
        :return: Boolean
        """
        return self.name in person2.get_ancestors()

    def is_cousin(self, person2):
        """
        Check if this person and the given person share a common ancestor
        but are not direct ancestors

        :param person2: Person
        :return: Boolean
        """
        if self.equals(person2):
            return False
        elif self.is_child(person2) or person2.is_child(self):
            return False
        else:
            ancestors1 = self.get_ancestors()
            ancestors2 = person2.get_ancestors()

            if person2.get_name() in ancestors1 or self.name in ancestors2:
                return False

            for anc in ancestors1:
                if anc in ancestors2:
                    return True

        return False

    def is_unrelated(self, person2):
        """
        Check if this person and the given person are not related at all.

        :param person2: Person
        :return: Boolean
        """
        if self.equals(person2):
            return True
        elif self.is_child(person2) or person2.is_child(self):
            return False
        elif self.is_sibling(person2):
            return False
        elif self.is_cousin(person2):
            return False
        elif self.is_ancestor(person2) or person2.is_ancestor(self):
            return False
        else:
            return True

    def equals(self, person2):
        """
        If this person and the given person share a name, they are considered equal.

        :param person2: Person
        :return: Boolean
        """
        return self.name == person2.get_name()
