#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''

Usage:
    dojo_manager.py create_room (<room_type>) <room_name>...
    dojo_manager.py add_person (<person_name1> <person_name2>) (Fellow|Staff) [<wants_accommodation>]

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

    def __init__(self, name='', room_type=''):
        self.room_name = name
        self.room_type = room_type

        if room_type.lower() == 'office':
            print('yes')
            Room.max_occupants = 6
        elif room_type.lower() == 'livingspace':
            print('No')
            Room.max_occupants = 4
        self.max_occupants = Room.max_occupants
        print('Type: ', room_type, self.max_occupants)

    def create_room(self, name, room_type):

        print('Making Room Now')
        self.all_rooms.append(self)

        return self


class Person:
    def __init__(self, name='', wants_accommodation=False):

        self.person_name = name
        self.wants_accommodation = wants_accommodation

    def add_person(self, name, job_group):
        return self


class Fellow(Person):

    def add_person(self, name='', wants_accomodation=False):
        Person().__init__(name, wants_accomodation)
        print('Fellow {0} {1} has been successfully added.'.format(name[0],
                                                                  name[1]))
        if not wants_accomodation:
            print('{0} does not wish to be accomodated'.format(name[0]))
        return self


class Staff(Person):

    def add_person(self, name='', wants_accommodation=False):
        Person().__init__(name, wants_accommodation=False)
        print('Staff {0} has been successfully added.'.format(name))
        return self


class Office(Room):

    def create_room(self, name, room_type):
        Room().__init__(name, room_type)

        print('Instance: ', self.max_occupants)
        print('An Office called {0} has been successfully '
              'created!'.format(name))
        return self


class LivingSpace(Room):

    def create_room(self, name, room_type):
        Room().__init__(name, room_type)
        print('A Livingspace called {0} has been successfully '
              'created!'.format(name))
        # self.all_rooms.append(self)
        print('Instance: ', self.max_occupants)
        # print(self.room_name, len(self.all_rooms))
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

        name = [options['<person_name1>'], options['<person_name2>']]
        print(name)

        wants_accommodation = options['<wants_accommodation>']
        room_names = options['<room_name>']
        room_type = options['<room_type>']
        # add_person = options['<add_person>']
        if options['add_person']:
            print('Yes', name, wants_accommodation)
            if options['Fellow']:
                self.fellows.append(Fellow.add_person(Dojo, name,
                                                  wants_accommodation))
            elif options['Staff']:
                self.staff.append(Staff.add_person(Dojo, name,
                                                   wants_accommodation=False))

        elif options['create_room']:
            for room in room_names:
                self.add_room(room, room_type)

        print(len(self.livingspaces))
        print(len(self.offices))
        print(len(self.fellows))
        print(len(self.staff))

    def add_room(self, room_name, room_type):
        # print('Freee', roomtype.lower())

        if room_type.lower() == 'office':
            self.offices.append(Office.create_room(Office, room_name,
                                                   room_type))
            # print('An Office called {0} has been successfully '
            #       'created!'.format(room_name))
            # self.fellows.append()

        elif room_type.lower() == 'livingspace':
            self.livingspaces.append(LivingSpace.create_room(LivingSpace, room_name,
                                                             room_type))
            # print('A Living Room called {0} has been successfully '
            #       'created!'.format(room_name))



if __name__ == "__main__":

    options = docopt.docopt(__doc__, version='0.0.0.0')
    a = Dojo()
    a.main(options)