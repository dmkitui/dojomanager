#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''

Usage:
    dojo_manager.py create_room (<room_type>) <room_name>...
    dojo_manager.py add_person (<person_name> <person_name>) (Fellow|Staff) [<wants_accommodation>]

arguments:
    create_room Creates a room type of <room_type> called <room_name>
    add_person Adds a person, and assigns the person to a randomly chosen existing room
'''

# options:
#     -h, --help Show this screen and exit
#     -v, --version show program's version number and exit



import docopt


class Room(object):

    '''
    Class Room.
    '''
    max_occupants = 0
    all_rooms = []
    room_name = ''

    def __init__(self, room_name='', room_type=''):
        self.room_name = room_name
        self.room_type = room_type
        print('Room Name: ', self.room_name)

        if room_type.lower() == 'office':
            Room.max_occupants = 6
        elif room_type.lower() == 'livingspace':
            Room.max_occupants = 4
        self.max_occupants = Room.max_occupants
        print('Type: ', room_type, self.max_occupants)

    def create_room(self, name, room_type):

        print('Making Room Now')
        self.all_rooms.append(self)

        return self


class Person(object):
    person_name = ''
    accommodation = False

    def __init__(self, name='', accommodation=False):

        self.person_name = name
        self.accommodation = accommodation

    def add_person(self, name, job_group):
        return self


class Fellow(Person):

    def add_person(self, name='', accomodation=False):
        Person().__init__(name, accomodation)
        print('Fellow {0} {1} has been successfully added.'.format(name[0],
                                                                  name[1]))
        if not accomodation:
            print('{0} does not wish to be accomodated'.format(name[0]))
        print('NAME: ', self.person_name)
        return self


class Staff(Person):

    def add_person(self, name='', wants_accommodation=False):
        Person().__init__(name, wants_accommodation=False)
        print('Staff {0} has been successfully added.'.format(name))
        return self


class Office(Room):

    def create_room(self, room_name, room_type):
        Room().__init__(room_name, room_type)
        print('An Office called {0} has been successfully '
              'created!'.format(room_name))
        return self


class LivingSpace(Room):

    def create_room(self, room_name, room_type):
        Room().__init__(room_name, room_type)
        print('A Livingspace called {0} has been successfully '
              'created!'.format(room_name))

        return self


class Dojo(object):

    def __init__(self):
        self.fellows = []
        self.staff = []
        self.offices = []
        self.livingspaces = []

    def error_handler(self):
        pass

    def main(self, options):
        # print(options)

        name = options['<person_name>']

        wants_accommodation = options['<wants_accommodation>']
        room_names = options['<room_name>']
        room_type = options['<room_type>']

        if wants_accommodation and wants_accommodation.lower() == 'y':
            accommodation = True
        else:
            accommodation = False

        if options['add_person']:
            if options['Fellow']:
                person_class = Fellow()
                person = person_class.add_person(name, accommodation)
                self.fellows.append(person)
            elif options['Staff']:
                person_class = Staff()
                person = person_class.add_person(name, accommodation)
                self.staff.append(person)

        elif options['create_room']:
            for room in room_names:
                self.add_room(room, room_type)

        print(len(self.livingspaces))
        print(len(self.offices))
        print(len(self.fellows))
        print(len(self.staff))

    def add_room(self, room_name, room_type):

        if room_type.lower() == 'office':
            a = Office()
            room = a.create_room(room_name, room_type)
            self.offices.append(room)

        elif room_type.lower() == 'livingspace':
            b = LivingSpace()
            room = b.create_room(room_name, room_type)
            self.livingspaces.append(room)


if __name__ == "__main__":

    options = docopt.docopt(__doc__, version='0')
    a = Dojo()
    a.main(options)