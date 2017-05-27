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
from blessings import Terminal


# The left margin print margin
terminal = Terminal()  # Instance of Terminal from blessings package
width = terminal.width # Current width of the terminal
margin = width - 50
spacer1 = ' ' * int(margin / 2)  # Indentation for the heading
spacer2 = ' ' * int(margin / 4)  # Indentation for the subsequent prints


def docopt_cmd(func):
    """
    This decorator function is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        # terminal = Terminal()
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('\n{term}Amity Manager V.1: Invalid argument value(s){term_normal}\n'.format(term=terminal.red, term_normal=terminal.normal))
            print('{term}{error_message}{term_normal}'.format(error_message=e, term=terminal.white, term_normal=terminal.normal))
            print('\n')
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

    # width = os.get_terminal_size().columns
    # margin = int(width) - 50
    # spacer1 = ' ' * int(margin / 2)
    # spacer2 = ' ' * int(margin / 4)
    # term = Terminal()

    intro = '\n' \
            '\n' \
            '{space}       {term1}________________ANDELA_______________{term_normal}\n' \
            '{space}       {term1}The Amity Room Allocations Management{term_normal}\n' \
            '{space}       {term1}_____________Version 0.0_____________{term_normal}\n' \
            '{term_normal}\n' \
            '{space2}{term2}Usage:{term_normal}\n'\
            '{space2}   create_room (Office|Livingspace) <room_name>...\n' \
            '{space2}   add_person (<person_name> <person_name>) (Fellow|Staff) [<wants_accommodation>]\n' \
            '{space2}   reallocate_person <person_identifier> <new_room_name>\n' \
            '{space2}   print_room <room_name>\n' \
            '{space2}   print_allocations [<-o=filename>]\n' \
            '{space2}   print_unallocated [<-o=filename>]\n' \
            '{space2}   load_people (<people_file>)\n' \
            '{space2}   save_state [--db=sqlite_database]​\n' \
            '{space2}   load_state [--db=sqlite_database]​\n' \
            '{space2}   help\n' \
            '{space2}   clear\n' \
            '{space2}   exit\n' \
            '\n' \
            '{space2}{term2}arguments:{term_normal}\n' \
            '{space2}   create_room         - Creates room(s) of type <room_type> with the specified name(s)\n' \
            '{space2}   add_person          - Adds a person, and assigns the person to a randomly chosen existing room\n' \
            '{space2}   reallocate_person   - Move person with the <person_identifier> to room <new_room_name>\n' \
            '{space2}   print_room          - Prints the occupants of the specified room\n' \
            '{space2}   print_allocations   - Prints the current occupants of all existing rooms\n' \
            '{space2}   print_unallocated   - Prints people who are not located in any rooms\n' \
            '{space2}   laod_people         - Loads people into the system from the specified input text file\n' \
            '{space2}   save_state          - Saves the data in the program to the specified database\n' \
            '{space2}   load_state          - Loads the data form specified database\n' \
            '{space2}   help                - Prints this help message\n' \
            '{space2}   clear               - Clears the screen\n' \
            '{space2}   exit                - Exits this interactive session\n' \
            '\n\n'.format(term1=terminal.bold_white, term2=terminal.white, term_normal=terminal.normal, space=spacer1, space2=spacer2)

    prompt = '{space2}{term1}Enter Command:  {term_normal}'.format(term1=terminal.bold_white, term_normal=terminal.normal, space2=spacer2)

    amity = AmityManager()

    @docopt_cmd
    def do_create_room(self, user_input):
        '''
        Usage:
            create_room (Office|Livingspace) (<room_name>...)
        '''

        if user_input['Livingspace']:
            room_type = 'Livingspace'
        else:
            room_type = 'Office'

        room_names = user_input['<room_name>']

        self.amity.create_room(room_names, room_type)

    @docopt_cmd
    def do_add_person(self, user_input):
        '''
        Usage:
            add_person (<person_name> <person_name>) (Fellow|Staff) [<wants_accommodation>]
        '''
        name = user_input['<person_name>']
        wants_accommodation = user_input['<wants_accommodation>']

        if user_input['Fellow']:
            person_type = 'Fellow'
        elif user_input['Staff']:
            person_type = 'Staff'
        self.amity.add_person(name, person_type, wants_accommodation)

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
        room_name = user_input['<room_name>']
        self.amity.print_room(room_name)

    @docopt_cmd
    def do_print_allocations(self, user_input):
        '''
        Usage:
            print_allocations [<-o=filename>]
        '''
        output_file = user_input['<-o=filename>']
        self.amity.print_allocations(output_file)

    @docopt_cmd
    def do_print_unallocated(self, user_input):
        '''
        Usage:
            print_unallocated [<-o=filename>]
        '''

        unallocated_file_name = user_input['<-o=filename>']

        self.amity.print_unallocated(unallocated_file_name)

    @docopt_cmd
    def do_reallocate_person(self, user_input):
        '''
        Usage:
            reallocate_person <person_identifier> <new_room_name>
        '''
        relocate_id = user_input['<person_identifier>']
        new_room = user_input['<new_room_name>']
        self.amity.reallocate_person(relocate_id, new_room)

    @docopt_cmd
    def do_load_people(self, user_input):
        '''
        Usage:
            load_people (<people_file>)
        '''
        text_input_file = user_input['<people_file>']
        self.amity.load_people(text_input_file)

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
        db_name = user_input['<sqlite_database>​']
        self.amity.load_state(db_name)

    @docopt_cmd
    def do_print_free_rooms(self, user_input):
        '''
        Usage:
            print_free_rooms
        '''
        self.amity.print_free_rooms()

if __name__ == '__main__':
    try:
        DocoptManager().cmdloop()
    except (KeyboardInterrupt, SystemExit):
        print('Amity Manager V0. Exit.')
        print('____________________________')