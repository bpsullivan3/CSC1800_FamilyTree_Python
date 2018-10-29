#! /usr/bin/python3.6

"""
Authors:

Meghan Carlock
Justin Graham
Patrick Sullivan
"""


import sys


def create_person(name, parent1, parent2):
    """
    Create a dictionary for a 'Person'. If the person has no parents, the
    parent arguments should be None.

    :param name: String
    :param parent1: Dict
    :param parent2: Dict
    :return: Dict
    """
    person = dict()
    person['name'] = name  # String
    person['spouses'] = list()
    person['parent1'] = parent1  # Dict
    person['parent2'] = parent2  # Dict
    person['children'] = list()
    return person


def add_spouse(person, spouse):
    """
    Access the list of spouses for the given person, and append the new spouse.

    :param person: Dict
    :param spouse: Dict
    :return: None
    """
    person['spouses'].append(spouse['name'])
    person['spouses'].sort()


def add_child(person, child):
    """
    Access the list of children for the given person, and append the new child.

    :param person: Dict
    :param child: Dict
    :return: None
    """
    person['children'].append(child['name'])
    person['children'].sort()


def get_children(person):
    """
    :param person: Dict
    :return: list of strings
    """
    return person['children']


def get_spouses(person):
    """
    :param person: Dict
    :return: list of strings
    """
    return person['spouses']


def get_siblings(person):
    """
    Gather the list of children for each parent, and add them to a list of
    siblings for the current person. Removes the person themselves from the list.

    :param person: Dict
    :return: list of strings
    """
    siblings = list()
    if person['parent1'] is not None:
        for child in get_children(person['parent1']):
            siblings.append(child)
    if person['parent2'] is not None:
        for child in get_children(person['parent2']):
            if child not in siblings:
                siblings.append(child)
    siblings.remove(person['name'])
    siblings.sort()
    return siblings


def get_ancestors(person):
    """
    Recurse through the parents of the person, and gather the list
    of direct ancestors.

    :param person: Dict
    :return: list of strings
    """
    ancestors = list()
    if person['parent1'] is None or person['parent2'] is None:
        return ancestors
    else:
        ancestors.append(person['parent1']['name'])
        ancestors.append(person['parent2']['name'])
        for anc in get_ancestors(person['parent1']):
            ancestors.append(anc)
        for anc in get_ancestors(person['parent2']):
            ancestors.append(anc)
    ancestors.sort()
    return ancestors


def is_child(person1, person2):
    """
    Check person1 is a direct child of person2
    :param person1: Dict
    :param person2: Dict
    :return: Boolean
    """
    if person1['parent1'] is None or person1['parent2'] is None:
        return False
    else:
        return person1['parent1'] == person2 or person1['parent2'] == person2


def is_spouse(person1, person2):
    """
    Check if person1 and person2 were spouses at some point in time.

    :param person1: Dict
    :param person2: Dict
    :return: Boolean
    """
    return person2['name'] in person1['spouses']


def is_sibling(person1, person2):
    """
    Check if person1 and person2 are siblings. One cannot be their own sibling.

    :param person1: Dict
    :param person2: Dict
    :return: Boolean
    """
    if person1 == person2:
        return False
    elif person1['parent1'] is not None and \
            (person1['parent1'] == person2['parent1']
             or person1['parent1'] == person2['parent2']):
        return True
    elif person1['parent2'] is not None and \
            (person1['parent2'] == person2['parent1']
             or person1['parent2'] == person2['parent2']):
        return True
    else:
        return False


def is_ancestor(person1, person2):
    """
    Check if person1 is an ancestor of person2

    :param person1: Dict
    :param person2: Dict
    :return: Boolean
    """
    return person1['name'] in get_ancestors(person2)


def is_cousin(person1, person2):
    """
    Check if person1 and person2 share a direct ancestor that is not each other.

    :param person1: Dict
    :param person2: Dict
    :return: Boolean
    """
    if person1 == person2:
        return False
    elif is_child(person1, person2) or is_child(person2, person1):
        return False
    else:
        ancestors1 = get_ancestors(person1)
        ancestors2 = get_ancestors(person2)

        if person2['name'] in ancestors1 or person1['name'] in ancestors2:
            return False

        for anc in ancestors1:
            if anc in ancestors2:
                return True

    return False


def is_unrelated(person1, person2):
    """
    Check if person1 and person2 are unrelated. For the purposes of this project,
    a person is unrelated to themselves.

    :param person1: Dict
    :param person2: Dict
    :return: Boolean
    """
    if person1 == person2:
        return True
    elif is_child(person1, person2) or is_child(person2, person1):
        return False
    elif is_sibling(person1, person2):
        return False
    elif is_cousin(person1, person2):
        return False
    elif is_ancestor(person1, person2) or is_ancestor(person2, person1):
        return False
    else:
        return True


def get_cousins(tree, person):
    """
    Get all cousins of person by checking each member of the tree.

    :param tree: Dict
    :param person: Dict
    :return: List of strings
    """
    result = list()
    for cousin in tree:
        if is_cousin(person, tree[cousin]):
            result.append(cousin)
    result.sort()
    return result


def get_unrelated(tree, person):
    """
    Get all people in the tree unrelated to person.

    :param tree: Dict
    :param person: Dict
    :return: List of strings
    """
    result = list()
    for unrelated in tree:
        if is_unrelated(person, tree[unrelated]):
            result.append(unrelated)
    result.sort()
    return result


def main():
    tree = dict()
    query = sys.stdin.readline()

    while query:
        parts = query[:-1].split(' ')

        if parts[0] == 'E':
            if len(parts) == 3:  # New Marriage

                # Initialize person
                if parts[1] not in tree:
                    person1 = create_person(parts[1], None, None)
                    tree[parts[1]] = person1
                else:
                    person1 = tree[parts[1]]
                if parts[2] not in tree:
                    person2 = create_person(parts[2], None, None)
                    tree[parts[2]] = person2
                else:
                    person2 = tree[parts[2]]

                # Set the proper spouse for the entries
                add_spouse(person1, person2)
                add_spouse(person2, person1)

            elif len(parts) == 4:  # New Child

                # Initialize Parents
                if parts[1] not in tree:
                    person1 = create_person(parts[1], None, None)
                    tree[parts[1]] = person1
                else:
                    person1 = tree[parts[1]]
                if parts[2] not in tree:
                    person2 = create_person(parts[2], None, None)
                    tree[parts[2]] = person2
                else:
                    person2 = tree[parts[2]]

                # Create the child if they don't exist
                if parts[3] in tree:
                    print(parts[3], ' already exists! Child not created.')
                else:
                    person3 = create_person(parts[3], person1, person2)
                    tree[parts[3]] = person3
                    add_child(person1, person3)
                    add_child(person2, person3)

            else:
                print('Please enter a valid query.')
                break

        elif parts[0] == 'W':  # List all <relation> of <person>
            if len(parts) == 3:
                print(query[:-1])
                if parts[2] not in tree:
                    print(parts[2], ' does not exist!')
                else:
                    person = tree[parts[2]]
                    if parts[1] == 'child':
                        for child in get_children(person):
                            print(child)
                    elif parts[1] == 'spouse':
                        for spouse in get_spouses(person):
                            print(spouse)
                    elif parts[1] == 'sibling':
                        for sibling in get_siblings(person):
                            print(sibling)
                    elif parts[1] == 'ancestor':
                        for ancestor in get_ancestors(person):
                            print(ancestor)
                    elif parts[1] == 'cousin':
                        for cousin in get_cousins(tree, person):
                            print(cousin)
                    elif parts[1] == 'unrelated':
                        for unrelated in get_unrelated(tree, person):
                            print(unrelated)
                    else:
                        print('Please enter a valid query.')
            else:
                print('Please enter a valid query.')
            print()

        elif parts[0] == 'X':  # Is <person> the <relation> of <person>?
            if len(parts) == 4:
                print(query[:-1])

                person1 = tree[parts[1]]
                if person1 is None:
                    print(parts[1], 'does not exist!')
                    break
                person2 = tree[parts[3]]
                if person2 is None:
                    print(parts[3], ' does not exist!')
                    break

                if parts[2] == 'child':
                    if is_child(person1, person2):
                        print('Yes')
                    else:
                        print('No')
                elif parts[2] == 'spouse':
                    if is_spouse(person1, person2):
                        print('Yes')
                    else:
                        print('No')
                elif parts[2] == 'sibling':
                    if is_sibling(person1, person2):
                        print('Yes')
                    else:
                        print('No')
                elif parts[2] == 'ancestor':
                    if is_ancestor(person1, person2):
                        print('Yes')
                    else:
                        print('No')
                elif parts[2] == 'cousin':
                    if is_cousin(person1, person2):
                        print('Yes')
                    else:
                        print('No')
                elif parts[2] == 'unrelated':
                    if is_unrelated(person1, person2):
                        print('Yes')
                    else:
                        print('No')
                else:
                    print('Please enter a valid query.')
            else:
                print('Please enter a valid query.')
            print()
        else:
            print('Please enter a valid query.')
            print()

        query = sys.stdin.readline()


if __name__ == '__main__':
    """
    This part is not exactly necessary, but it helps the computer to process all of the program
    before running any actual commands. Syntax errors and other compiler issues will be found
    quicker this way. __name__ == '__main__' is simply best practice for running python programs.
    """
    main()
