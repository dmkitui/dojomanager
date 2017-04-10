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

    def __init__(self, name='', room_type=''):
        self.room_name = name
        self.all_rooms = []
        self.room_type = room_type
        print(room_type)
        if self.room_type.lower() == 'office':
            self.max_occupants = 6
        elif self.room_type.lower() == 'livingspace':
            self.max_occupants = 4

    def create_room(self, name, room_type):

        print('Making Room Now')
        self.all_rooms.append(self)

        return self


class Person:
    def __init__(self):
        pass


class Fellow(Person):

    def __init__(self):
        pass


class Staff(Person):

    def __init__(self):
        pass


class Office(Room):
    def __init__(self):
        pass

    def create_room(self, name, room_type):
        super(Office, self).__init__(name, room_type)
        # self.room_name = name
        # self.room_type = room_type
        # print('Making Room Now')
        self.all_rooms.append(self)
        print(self.max_occupants, self.room_name, len(self.all_rooms))
        return self


class LivingSpace(Room):
    def __init__(self):
        pass

    def create_room(self, name, room_type):
        super(LivingSpace, self).__init__(name, room_type)
        # self.room_name = name
        # self.room_type = room_type
        print('Making Room Now')
        self.all_rooms.append(self)
        print(self.max_occupants, self.room_name, len(self.all_rooms))
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
        print(options)

        name = [options['<person_name1>'], options['<person_name2>']]
        print(name)

        wants_accommodation = options['<wants_accommodation>']
        room_names = options['<room_name>']
        room_type = options['<room_type>']
        # add_person = options['<add_person>']
        if options['add_person']:
            print('Yes', name, wants_accommodation)
            self.fellows.append(Fellow.add_person(self, name,
                                                  wants_accommodation))

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
            self.offices.append(Office.create_room(room_name, room_type))
            print('An Office called {0} has been successfully '
                  'created!'.format(room_name))
            # self.fellows.append()

        elif room_type.lower() == 'livingspace':

            self.livingspaces.append(LivingSpace.create_room(room_name,
                                                             room_type))
            print('A Living Room called {0} has been successfully '
                  'created!'.format(room_name))



if __name__ == "__main__":

    options = docopt.docopt(__doc__, version='0.0.0.0')
    a = Dojo()
    a.main(options)