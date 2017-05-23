#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Usage:
    amity_manager.py create_room (Office|Livingspace) <room_name>...
    amity_manager.py add_person (<person_name> <person_name>) (Fellow|Staff) [<wants_accommodation>]

arguments:
    create_room Creates a room type of <room_type> called <room_name>
    add_person Adds a person, and assigns the person to a randomly chosen existing room
'''

import cmd
from docopt import docopt, DocoptExit
from amity.amity import AmityManager
import os


def docopt_cmd(func):
    """
    This decorator function is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Amity Manager V.1: Invalid argument value(s)')
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
            '       The Amity Room Allocations Management\n' \
            '       _____________Version 0.0_____________\n' \
            '\n' \
            'Usage:\n'\
            '   create_room (Office|Livingspace) <room_name>...\n' \
            '   add_person (<person_name> <person_name>) (Fellow|Staff) [<wants_accommodation>]\n' \
            '   reallocate_person <person_identifier> <new_room_name>\n' \
            '   print_room <room_name>\n' \
            '   print_allocations [<-o=filename>]\n' \
            '   print_unallocated [<-o=filename>]\n' \
            '   load_people (<people_file>)\n' \
            '   save_state [--db=sqlite_database]​\n' \
            '   load_state [--db=sqlite_database]​\n' \
            '   help\n' \
            '   clear\n' \
            '   exit\n' \
            'arguments:\n' \
            '   create_room Creates a room type of <room_type> called <room_name>\n' \
            '   add_person Adds a person, and assigns the person to a randomly chosen existing room\n' \
            '   reallocate_person Move person <person_identifier> to room <new_room_name>\n' \
            '   print_room Prints the occupants fo the stated room\n' \
            '   print_allocations Prints how the people are allocated in the different rooms\n' \
            '   print_unallocated Prints people who are not located in any rooms\n' \
            '   laod_people Loads people into the sysytem from input text file\n' \
            '   save_state Saves the data in the program to specified database\n' \
            '   load_state Loads the data form specified database\n' \
            '   help Prints this help message\n' \
            '   clear Clears the screen\n' \
            '   exit Exits this interactive session\n' \
            '\n\n'

    prompt = 'Enter Command: '
    amity_manager = AmityManager()

    @docopt_cmd
    def do_create_room(self, user_input):
        '''
        Usage:
            create_room (Office|Livingspace) (<room_name>...)
        '''
        self.amity_manager.create_room(user_input)

    @docopt_cmd
    def do_add_person(self, user_input):
        '''
        Usage:
            add_person (<person_name> <person_name>) (Fellow|Staff) [<wants_accommodation>]
        '''
        self.amity_manager.add_person(user_input)

    def do_clear(self, user_input):
        '''To clear screen'''
        os.system('cls' if os.name == 'nt' else 'clear')

    def do_exit(self, user_input):
        '''To exit from Amity Manager Session'''
        print('\nAmity Manager V0. Exiting...')
        return True

    @docopt_cmd
    def do_print_room(self, user_input):
        '''
        Usage:
            print_room <room_name>
        '''
        self.amity_manager.print_room(user_input)

    @docopt_cmd
    def do_print_allocations(self, user_input):
        '''
        Usage:
            print_allocations [<-o=filename>]
        '''
        self.amity_manager.print_allocations(user_input)

    @docopt_cmd
    def do_print_unallocated(self, user_input):
        '''
        Usage:
            print_unallocated [<-o=filename>]
        '''
        self.amity_manager.print_unallocated(user_input)

    @docopt_cmd
    def do_reallocate_person(self, user_input):
        '''
        Usage:
            reallocate_person <person_identifier> <new_room_name>
        '''
        self.amity_manager.reallocate_person(user_input)

    @docopt_cmd
    def do_load_people(self, user_input):
        '''
        Usage:
            load_people (<people_file>)
        '''
        self.amity_manager.load_people(user_input)

    @docopt_cmd
    def do_save_state(self, user_input):
        '''
        Usage:
            save_state [<--db=sqlite_database>]
        '''
        db_name = user_input['<--db=sqlite_database>']
        self.amity.save_state(db_name)

    @docopt_cmd
    def do_load_state(self, user_input):
        '''
        Usage:
            load_state <sqlite_database>​
        '''
        print('Not yet implemented')

if __name__ == '__main__':
    try:
        DocoptManager().cmdloop()
    except (KeyboardInterrupt, SystemExit):
        print('Amity Manager V0. Exit.')
        print('____________________________')