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

# options:
#     -h, --help Show this screen and exit
#     -v, --version show program's version number and exit



import docopt
import random
from personel.person import Person, Staff
from rooms.room import Office, LivingSpace

class Dojo(object):
    '''
    Class Dojo to model the dojo complex, and manage all the other classes
    from the main()
    '''

    def __init__(self):
        self.fellows = []
        self.staff = []
        self.offices = []
        self.livingspaces = []

    def error_handler(self):
        pass

    def main(self, options):
        '''
        Main function that instantiates and manages the other classes.
        :param options: input from docopt
        :return: None
        '''
        # print(options)

        name = options['<person_name>']

        wants_accommodation = options['<wants_accommodation>']
        room_names = options['<room_name>']

        if wants_accommodation:
            if options['Staff']:
                print('Staff are not entitled to accommodation')
                return 'Staff are not entitled to accommodation'

            if wants_accommodation.lower() == 'y' or \
                            wants_accommodation.lower() == 'n':
                accommodation = True
            else:
                print('Argument for Accomodation can only be either Y or N')
                return 'Argument for Accomodation can only be either Y or N'

        else:
            accommodation = False

        if options['add_person']:
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
                self.staff.append(person)

        elif options['create_room']:
            if options['Office']:
                for room_name in room_names:
                    self.add_office(room_name)
                    print('An Office called {0} has been successfully '
                          'created!'.format(room_name))
            if options['Livingspace']:
                for room_name in room_names:
                    self.add_living_space(room_name)
                    print('A Livingspace called {0} has been successfully '
                      'created!'.format(room_name))


#Print for testing purposes.
        # print(len(self.livingspaces))
        # print(len(self.offices))
        # print(len(self.fellows))
        # print(len(self.staff))


    def add_office(self, room_name):
        '''Function to call create_room function for the case of multiple
        room arguments'''
        a = Office()
        room = a.create_room(room_name, 'office')
        self.offices.append(room)

    def add_living_space(self, room_name):
        '''Function to repeatedly call create_room method for multiple rooms entered.'''
        b = LivingSpace()
        room = b.create_room(room_name, 'livingspace')
        self.livingspaces.append(room)

    def allocate_livingroom(self, name):

        '''
        Function to allocate a random livin space to the person object that
        is passed as input
        :argument: name- person name to be allocated
        :return: None
        '''

        livingroom = LivingSpace()
        livingroom_names = ['Comfort', 'Kenya', 'Uganda', 'Kampala']

        living_places = []

        for pad in livingroom_names:
            living_place = livingroom.create_room(pad, 'livingspace')
            living_places.append(living_place)

        x = random.randint(0, len(living_places)-1)
        # allocated_livingroom = living_places[x]

        print('{0} has been allocated the livingspace {1}'.format(name[0],
                                                             livingroom_names[x]))

    def allocate_office(self, name):
        '''
        Function to allocate a random office to the person passed as argument
        :param name: Person object to be allocated
        :return: None
        '''
        office_instance = Office()
        office_block = []

        # Create dummy rooms for use to demo task0 as persistance is yet to
        # be implemented
        office_names = ['Green', 'Yellow', 'Blue', 'Brown']

        for officename in office_names:
            new_office = office_instance.create_room(officename, 'office')
            office_block.append(new_office)

        y = random.randint(0, len(office_block) - 1)
        print(y)

        allocated_office = office_block[y]
        print('{0} has been allocated the office {1}'.format(name[0],
                                                             office_names[y]))



if __name__ == "__main__":
    # To give a more detailed error in case of commandline arguemnt
    # mismatch
    try:
        options = docopt.docopt(__doc__, version='0')
        a = Dojo()
        a.main(options)

    except docopt.DocoptExit as e:
        print('\n')
        print('Dojo Manager V. 1: Invalid command(s) or argument '
                                        'values')
        print('\n')
        print(e)
        print('\n')