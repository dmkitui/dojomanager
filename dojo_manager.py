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

import cmd
from docopt import docopt, DocoptExit
from dojo.dojo import DojoManager
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


class DocoptManager(cmd.Cmd):
    '''
    Class to handle docopt: parsing of cmd input and call relevant
    functionality from other module
    '''

    intro = '\n       ___________ANDELA KENYA______________\n' \
            '       The Dojo Room Allocations Management\n' \
            '       _____________Version 0.0_____________\n' \
            '\n' \
            'Usage:\n'\
            '   dojo_manager.py create_room (Office|Livingspace) <room_name>...\n' \
            '   dojo_manager.py add_person (<person_name> <person_name>) (Fellow|Staff) [' \
            '<wants_accommodation>]\n' \
            '\n' \
            'arguments:\n' \
            '    create_room Creates a room type of <room_type> called <room_name>\n' \
            '    add_person Adds a person, and assigns the person to a randomly chosen existing room\n' \
            '\n\n'

    prompt = 'Enter Command: '
    dojo_manager = DojoManager()

    @docopt_cmd
    def do_create_room(self, user_input):
        '''
        Usage:
            create_room (Office|Livingspace) (<room_name>...)
        '''
        self.dojo_manager.create_room(user_input)

    @docopt_cmd
    def do_add_person(self, user_input):
        '''
        Usage:
            add_person (<person_name> <person_name>) (Fellow|Staff) [<wants_accommodation>]
        '''
        self.dojo_manager.add_person(user_input)

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

    # To implement docopt function wrapper fully
    # @docopt_cmd
    # def do_exit(self, user_input):
    #     '''To exit from Dojo Manager Session'''
    #     print('Dojo Manager V0. Exiting...')
    #     return True
    def do_exit(self, user_input):
        '''To exit from Dojo Manager Session'''
        print('\nDojo Manager V0. Exiting...')
        return True

    @docopt_cmd
    def do_print_room(self, user_input):
        '''
        Usage:
            print_room <room_name>
        '''
        self.dojo_manager.print_room(user_input)

    @docopt_cmd
    def do_print_allocations(self, user_input):
        '''
        Usage:
            print_allocations [<-o=filename>]
        '''
        self.dojo_manager.print_allocations(user_input)

if __name__ == '__main__':
    try:
        DocoptManager().cmdloop()
    except (KeyboardInterrupt, SystemExit):
        print('Dojo Manager V0. Exit.')
        print('____________________________')
