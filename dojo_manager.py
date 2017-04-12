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

from docopt import docopt, DocoptExit
import random
from cmd import Cmd
from personel.person import Staff, Fellow
from rooms.room import Office, LivingSpace
import os

def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Dojo Manager V.1: Invalid argument value(s)')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.
            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


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

    @docopt_cmd
    def do_create_room(self, user_input):
        """
        Usage:
            create_room (Office|Livingspace) (<room_name>...)
        """
        room_names = user_input['<room_name>']

        if user_input['Office']:
            existing_offices = [x.room_name for x in self.office_block]
            for room_name in room_names:
                if room_name in existing_offices:
                    print('An Office called {} already exists'.format(room_name))
                    continue
                self.add_office(room_name)
                print('An Office called {0} has been successfully '
                      'created!'.format(room_name))

        if user_input['Livingspace']:
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

    @docopt_cmd
    def do_add_person(self, user_input):
        '''
        Usage:
            add_person (<person_name> <person_name>) (Fellow|Staff) [<wants_accommodation>]
        '''

        name = user_input['<person_name>']

        wants_accommodation = user_input['<wants_accommodation>']

        if wants_accommodation:
            if user_input['Staff']:
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

        if user_input['Fellow']:
            person_class = Fellow()
            person = person_class.add_person(name, accommodation)
            self.fellows.append(person)
            self.allocate_office(name)
            if accommodation:
                self.allocate_livingroom(name)
        elif user_input['Staff']:
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

    # To implement docopt function wrapper fully
    # @docopt_cmd
    # def do_exit(self, user_input):
    #     '''To exit from Dojo Manager Session'''
    #     print('Dojo Manager V0. Exiting...')
    #     return True

    def do_exit(self, user_input):
        '''To exit from Dojo Manager Session'''
        print('Dojo Manager V0. Exiting...')
        return True

    # To implement docopt wrapper exit method
    # @docopt_cmd
    # def do_clear(self, user_input):
    #     '''To clear screen'''
    #     '''
    #     Usage:
    #         clear
    #     '''
    #     os.system('cls' if os.name == 'nt' else 'clear')

    def do_clear(self, user_input):
        '''To clear screen'''
        os.system('cls' if os.name == 'nt' else 'clear')

    @docopt_cmd
    def do_print_room(self, user_input):
        '''
        Usage:
            print_room <room_name>
        '''
        '''Prints the names of all the people in ​room_name​ on the screen.'''

        room_name = user_input['<room_name>']
        available_rooms = self.office_block + self.livingspaces
        available_room_names = [x.room_name for x in available_rooms]

        if room_name not in available_room_names:
            print('Room {} Seems not to exist. Kindly Confirm room '
                  'name'.format(room_name))
            return

        room_object = [x for x in available_rooms if x.room_name ==
                      room_name][0]
        occupant_list = room_object.occupants

        if len(occupant_list) == 0: # When a room is empty
            print_output = 'Room {} is empty'.format(room_name)
        else:
            print_names = []
            for occupant in occupant_list:
                name = ' '.join(occupant)
                print_names.append(name)

            print_output = ', '.join(print_names)

        print('Occupants of room {} : {}'.format(room_name, print_output))

    @docopt_cmd
    def do_print_allocations(self, user_input):
        '''
        Usage:
            print_allocations [<-o=filename>]
        '''
        print(user_input)
        if user_input['<-o=filename>']:
            output_file = user_input['<-o=filename>']

        rooms = self.office_block + self.livingspaces
        if len(len(rooms)) == 0:
            print('No rooms currently occupied')
            return

        for room in rooms:
            occupant_list = room.occupants
            room_occupant_names = []
            if len(occupant_list) > 0:
                for occupant in occupant_list:
                    name = ' '.join(occupant)
                    room_occupant_names.append(name)
            print(room.name)
            print('-----------------------')
            print(', '.join(room_occupant_names))





if __name__ == '__main__':

    try:
        DojoManager().cmdloop()
    except (KeyboardInterrupt, SystemExit):
        print('Dojo Manager V0. Exit.')
        print('____________________________')