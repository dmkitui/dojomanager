#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''

Usage:
    dojo_manager.py create_room (Office|Livingspace) <room_name>...
    dojo_manager.py add_person (<person_name> <person_name>) (Fellow|Staff) [<wants_accommodation>]

arguments:
    create_room Creates a room type of <room_type> called <room_name>
    add_person Adds a person, and assigns the person to a randomly chosen existing room
'''



import docopt
import random
from cmd import Cmd
from personel.person import Staff, Fellow
from rooms.room import Office, LivingSpace


class DojoManager(Cmd):
    '''
    Class Dojo to model the dojo complex, and manage all the data models
    '''

    intro = '\n       ___________ANDELA KENYA______________\n' \
            '       The Dojo Room Allocatons Management\n' \
            '       _____________Version 0.0_____________\n'
    prompt = 'Enter Command: '

    fellows = []
    staff_members = []
    office_block = []
    livingspaces = []

    def do_create_room(self, user_input):

        """
        Usage:
            create_room (Office|Livingspace) (<room_name>...)
        """

        try:
            options = docopt.docopt(self.do_create_room.__doc__, user_input)

        except docopt.DocoptExit as e:
            print('_________________________________________')
            print('Dojo Manager V.1: Invalid argument value(s)')
            print(e)
            return

        room_names = options['<room_name>']

        if options['Office']:
            existing_offices = [x.room_name for x in self.office_block]
            for room_name in room_names:
                if room_name in existing_offices:
                    print('An Office called {} already exists'.format(room_name))
                    continue
                self.add_office(room_name)
                print('An Office called {0} has been successfully '
                      'created!'.format(room_name))

        if options['Livingspace']:
            existing_livingspaces = [x.room_name for x in self.livingspaces]
            for room_name in room_names:
                if room_name in existing_livingspaces:
                    print('A Livingspace called {} already exists'.format(
                        room_name))
                    continue
                self.add_living_space(room_name)
                print('A Livingspace called {0} has been successfully '
                  'created!'.format(room_name))

    def add_office(self, room_name):
        '''Function to call create_room function for the case of multiple
        room arguments'''

        a = Office()
        room = a.create_room(room_name, 'office')
        self.office_block.append(room)

    def add_living_space(self, room_name):
        '''Function to repeatedly call create_room method for multiple rooms entered.'''
        b = LivingSpace()
        room = b.create_room(room_name, 'livingspace')
        self.livingspaces.append(room)

    def do_add_person(self, user_input):

        '''
        Usage:
            add_person (<person_name> <person_name>) (Fellow|Staff) [<wants_accommodation>]
        '''

        try:
            options = docopt.docopt(self.do_add_person.__doc__, user_input)

        except docopt.DocoptExit as e:
            print('_________________________________________')
            print('Dojo Manager V.1: Invalid argument values')
            print(e)
            return

        name = options['<person_name>']

        wants_accommodation = options['<wants_accommodation>']

        if wants_accommodation:
            if options['Staff']:
                print('Staff are not entitled to accommodation')
                return 'Staff are not entitled to accommodation'

            if wants_accommodation.lower() == 'y':
                accommodation = True

            elif wants_accommodation.lower() == 'n':
                accommodation = False

            else:
                print('Argument for Accomodation can only be either Y or N')
                return
        else:
            accommodation = False

        if options['Fellow']:
            person_class = Fellow()
            person = person_class.add_person(name, accommodation)
            self.fellows.append(person)
            self.allocate_office(name)
            if accommodation:
                self.allocate_livingroom(name)
        elif options['Staff']:
            person_class = Staff()
            person = person_class.add_person(name)
            self.allocate_office(name)
            self.staff_members.append(person)

    def allocate_livingroom(self, name):

        '''
        Function to allocate a random livin space to the person object that
        is passed as input
        :argument: name- person name to be allocated
        :return: None
        '''
        if len(self.livingspaces) == 0:
            print('No Livingroom currently available for allocation')
            return

        available_rooms = [x for x in self.livingspaces if len(x.occupants) < 4]

        if len(available_rooms) == 0:
            print('Sorry, No livingspace currently available in any of the '
                  'rooms')
            return

        random_room = random.choice(available_rooms)
        random_room.occupants.append(name)

        print('{0} has been allocated the livingspace {1}'.format(name[0], random_room.room_name))

    def allocate_office(self, name):
        '''
        Function to allocate a random office to the person passed as argument
        :param name: Person object to be allocated
        :return: None
        '''
        if len(self.office_block) == 0:
            print('No Offices currently available for allocation')
            return

        available_rooms = [x for x in self.office_block if len(x.occupants) < 6]

        if len(available_rooms) == 0:
            print('Sorry, No space currently available in any of the Offices')
            return

        random_office = random.choice(available_rooms)
        random_office.occupants.append(name)

        print('{0} has been allocated the office {1}'.format(name[0], random_office.room_name))

if __name__ == '__main__':

    try:
        DojoManager().cmdloop()
    except (KeyboardInterrupt, SystemExit):
        print('____________________________')