"""
Author: Patrick Sullivan

The main, runnable class for the Family Tree Project
"""


import sys
from FamilyTree import FamilyTree
from Person import Person
import Person


def main():
    tree = FamilyTree()
    query = sys.stdin.readline()

    while query:
        parts = query[:-1].split(' ')

        if parts[0] == 'E':
            if len(parts) == 3:  # New Marriage
                person1 = tree.get_person(parts[1])
                person2 = tree.get_person(parts[2])

                # Initialize person if they don't exist
                if person1 is None:
                    person1 = Person.Person(parts[1], None, None)
                    tree.add_person(person1)
                if person2 is None:
                    person2 = Person.Person(parts[2], None, None)
                    tree.add_person(person2)

                # Set the proper spouse for the entries
                person1.add_spouse(person2)
                person2.add_spouse(person1)

            elif len(parts) == 4:  # New Child
                person1 = tree.get_person(parts[1])
                person2 = tree.get_person(parts[2])

                # Initialize the parents if they don't exist
                if person1 is None:
                    person1 = Person.Person(parts[1], None, None)
                    tree.add_person(person1)
                if person2 is None:
                    person2 = Person.Person(parts[2], None, None)
                    tree.add_person(person2)

                # Create the child if they don't exist
                if tree.get_person(parts[3]) is not None:
                    print(parts[3], ' already exists! Child not created.')
                else:
                    person3 = Person.Person(parts[3], person1, person2)
                    tree.add_person(person3)
                    person1.add_child(person3)
                    person2.add_child(person3)

            else:
                print('Please enter a valid query.')
                break

        elif parts[0] == 'W':  # List all <relation> of <person>
            if len(parts) == 3:
                print(query[:-1])
                person = tree.get_person(parts[2])
                if person is None:
                    print(parts[2], ' does not exist!')
                else:
                    if parts[1] == 'child':
                        for child in person.get_children():
                            print(child)
                    elif parts[1] == 'spouse':
                        for spouse in person.get_spouses():
                            print(spouse)
                    elif parts[1] == 'sibling':
                        for sibling in person.get_siblings():
                            print(sibling)
                    elif parts[1] == 'ancestor':
                        for ancestor in person.get_ancestors():
                            print(ancestor)
                    elif parts[1] == 'cousin':
                        for cousin in tree.get_cousins(person):
                            print(cousin)
                    elif parts[1] == 'unrelated':
                        for unrelated in tree.get_unrelated(person):
                            print(unrelated)
                    else:
                        print('Please enter a valid query.')
            else:
                print('Please enter a valid query.')
            print()

        elif parts[0] == 'X':  # Is <person> the <relation> of <person>?
            if len(parts) == 4:
                print(query[:-1])

                person1 = tree.get_person(parts[1])
                if person1 is None:
                    print(parts[1], 'does not exist!')
                    break
                person2 = tree.get_person(parts[3])
                if person2 is None:
                    print(parts[3], ' does not exist!')
                    break

                if parts[2] == 'child':
                    if person1.is_child(person2):
                        print('Yes')
                    else:
                        print('No')
                elif parts[2] == 'spouse':
                    if person1.is_spouse(person2):
                        print('Yes')
                    else:
                        print('No')
                elif parts[2] == 'sibling':
                    if person1.is_sibling(person2):
                        print('Yes')
                    else:
                        print('No')
                elif parts[2] == 'ancestor':
                    if person1.is_ancestor(person2):
                        print('Yes')
                    else:
                        print('No')
                elif parts[2] == 'cousin':
                    if person1.is_cousin(person2):
                        print('Yes')
                    else:
                        print('No')
                elif parts[2] == 'unrelated':
                    if person1.is_unrelated(person2):
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

        query = sys.stdin.readline()


if __name__ == '__main__':
    main()
