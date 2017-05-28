#!/usr/bin/python3
# -*- coding: utf-8 -*-
import random
import os
import re
import sys
import itertools
from models.person import Staff, Fellow
from models.room import Office, LivingSpace
from models.database import Base, FellowDb, StaffDb, OfficeblockDb, LivingspaceDb, PersonelIdsDb, UnallocatedDb, MaxRoomOccupants
from blessings import Terminal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class AmityManager(object):
    '''
    Class Dojo to model the amity complex, and manage all the data models
    '''
    fellows = []
    staff_members = []
    office_block = []
    living_spaces = []
    un_allocated_persons = {'fellows_acc': [], 'fellows_office': [], 'staff': []}
    personnel_id = 0
    office_max_occupants = 6
    livingspace_max_occupants = 4
    data_saved = False  # Flag to indicate presence of data in the program at exit time, if not saved to database

    def print_message(self, message, message_state='success'):
        '''
        Function that prints out messages and program state to the terminal
        :param message: Message to be printed to the screen
        :param message_state: If message is success mesage, or error message. Default is 'success'
        :return: None
        '''
        terminal = Terminal()
        # margin from the left of terminal.
        width = terminal.width # Terminal width from blessings module. Doesnt work with virtual terminal like running tests

        if width is None: # Work-around to provide default terminal width size.
            width = 600
        margin = width - 20
        spacer = ' ' * int(margin / 4)

        if message_state == 'success':  # For an operation succeeded
            state = terminal.green

        elif message_state == 'info':  # For you program information.
            state = terminal.yellow

        elif message_state == 'error':  # On error in program operation
            state = terminal.red

        print('{spacer}{state}{message}{terminal_normal}\n'.format(state=state, spacer=spacer, message= message, terminal_normal=terminal.normal))

    def title_printer(self, title):
        '''Function to print titles of the various program screens'''
        print('\n')
        msg = '{:_^80}'.format(title)
        print('\n')
        self.print_message(msg)


    def create_room(self, room_names, room_type):
        '''
        Function to create a room in the amity model
        :param user_input: cli arguments from which room_name and room_type arguments are parsed.
        :return: specific errors incase of any errors or print statements to display status.
        '''

        self.title_printer('CREATE ROOM')

        for room_name in room_names:
            if self.names_check(room_name):
                pass
            else:
                self.print_message('{room_name} is not a valid room name. Room not created'.format(room_name=room_name), 'error')
                continue
            # Get list of already existing room names.
            existing_room_names = [x.room_name for x in self.office_block] + [x.room_name for x in self.living_spaces]
            if room_name in existing_room_names:
                self.print_message('A room called {} already exists'.format(room_name), 'error')
                continue
            self.add_room(room_name, room_type)
        print('\n')

    def add_room(self, room_name, room_type):
        '''
        Function to call create_room function for the case of multiple room arguments
        :param room_name: name for the new room
        :param room_type: tyoe of room, either 'Livingspace' or 'Office'.
        :return: Prints to the console on successful creation of the specified room or error message.
        '''
        if room_type == 'Office':
            office_instance = Office()
            room = office_instance.create_room(room_name, 'office')
            self.office_block.append(room)
            self.print_message('An Office called {0} has been successfully created!'.format(room_name))

        elif room_type == 'Livingspace':
            livingspace_instance = LivingSpace()
            room = livingspace_instance.create_room(room_name, 'livingspace')
            self.living_spaces.append(room)
            self.print_message('A Livingspace called {0} has been successfully created!'.format(room_name))

    def new_personnel_number(self, person_type):
        '''
        Funtion to return new personel ID based on the current number
        :return: personel_number
        '''
        self.personnel_id += 1   # increment current staff personnel_id
        new_number_string = format(self.personnel_id, '03d')
        if person_type == 'staff':
            new = 'AND/S/' + new_number_string

        elif person_type == 'fellow':
            new = 'AND/F/' + new_number_string

        return new

    def add_person(self, name, person_type, wants_accommodation):
        '''
        Function to add individuals to the amity
        :param name: List of new persons name [first_name, second_name]
        :param wants_accommodation: argument that specifies if person to be added wants accommodation or not. Should be either 'Y', 'N', 'y' or 'n' 
        :param person_type: New person type, either 'Staff' or 'Fellow'
        :return: prints to the console on successful creation, returns relevant error messages on errors
        '''

        self.title_printer('ADD PERSON')

        if not self.names_check(name[0]) or not self.names_check(name[1]):
            self.print_message('Invalid Person Name.', 'error')
            return
        if wants_accommodation:
            if person_type == 'Staff':
                self.print_message('Staff are not entitled to accommodation', 'error')
                return

            if wants_accommodation.lower() == 'y':
                accommodation = True

            elif wants_accommodation.lower() == 'n':
                accommodation = False

            else:
                self.print_message('Argument for Accommodation can only be either Y/y or N/n\n', 'error')
                return
        else:
            accommodation = False
        if person_type == 'Fellow':
            person_class = Fellow()
            person_number = self.new_personnel_number('fellow')
            new_fellow = person_class.add_person(name, accommodation, person_number)
            self.fellows.append(new_fellow)
            self.print_message('Fellow {0} {1} has been successfully added.'.format(new_fellow.person_name[0], new_fellow.person_name[1]))
            random_office = self.allocate_office()

            if random_office:
                random_office.occupants.append(new_fellow)
                self.print_message('{0} has been allocated the office {1}'.format(new_fellow.person_name[0], random_office.room_name))
            else:
                self.un_allocated_persons['fellows_office'].append(new_fellow)  # Add new_fellow to list of unallocated fellows

            if accommodation:
                random_livingspace = self.allocate_livingspace()
                if random_livingspace:
                    random_livingspace.occupants.append(new_fellow)
                    self.print_message('{0} has been allocated the livingspace {1}'.format(new_fellow.person_name[0], random_livingspace.room_name))
                else:
                    self.un_allocated_persons['fellows_acc'].append(new_fellow)  # Add new_fellow to list of unallocated fellows

            else:
                self.print_message('{0} does not wish to be accommodated'.format(new_fellow.person_name[0]))
        elif person_type == 'Staff':
            person_class = Staff()
            person_id = self.new_personnel_number('staff')
            new_staff = person_class.add_person(name, person_id)
            self.staff_members.append(new_staff)
            self.print_message('Staff {0} {1} has been successfully added.'.format(new_staff.person_name[0], new_staff.person_name[1]))

            random_office = self.allocate_office()
            if random_office:
                random_office.occupants.append(new_staff)
                self.print_message('{0} has been allocated the office {1}'.format(new_staff.person_name[0], random_office.room_name))
            else:
                self.un_allocated_persons['staff'].append(new_staff)  # Add new_staff to list of unallocated Staff

    def allocate_livingspace(self):
        '''Function to randomly allocate a livingroom to fellows'''

        if len(self.living_spaces) == 0:
            self.print_message('No Livingroom currently available for allocation', 'error')
            return None

        available_rooms = [x for x in self.living_spaces if len(x.occupants) < self.livingspace_max_occupants]

        if len(available_rooms) == 0:
            self.print_message('Sorry, No space currently available in any of the livingroms', 'error')
            return None

        return random.choice(available_rooms)

    def allocate_office(self):
        '''Function to randomly allocate an office to fellows and staff'''
        if len(self.office_block) == 0:
            self.print_message('No Offices currently available for allocation', 'error')
            return None

        available_rooms = [x for x in self.office_block if len(x.occupants) < self.office_max_occupants]

        if len(available_rooms) == 0:
            self.print_message('Sorry, No space currently available in any of the Offices', 'error')
            return None

        return random.choice(available_rooms)

    def print_room(self, room_name):
        '''Prints the names of all the people in ​specified room_name​.'''

        self.title_printer('ROOM OCCUPANTS')

        available_rooms = self.office_block + self.living_spaces
        available_room_names = [x.room_name for x in available_rooms]

        if room_name not in available_room_names:
            self.print_message('Room {} does not exist'.format(room_name), 'error')
            return

        room_object = [x for x in available_rooms if x.room_name == room_name][0]
        occupant_list = room_object.occupants

        if len(occupant_list) == 0: # When a room is empty
            print_output = 'Room is empty'
        else:
            print_names = []
            for occupant in occupant_list:
                name = ' '.join(occupant.person_name)
                print_names.append(name)

            print_output = ', '.join(print_names)

        self.print_message('Room Name: {}'.format(room_name.upper()))
        self.print_message('{space:->60}'.format(space='-'))
        self.print_message('Room Occupants: {}\n'.format(print_output))

    def print_allocations(self, output_file):
        '''
        Function to print room allocations, and optionally output same to file
        :param output_file: Optional text file to which the data is saved to.
        :return: Returns relevant error messages, or prints out information on success
        '''

        self.title_printer('AMITY ALLOCATIONS')

        rooms = self.office_block + self.living_spaces
        if len(rooms) == 0:
            self.print_message('No rooms currently available.\n', 'error')
            return
        allocations_data = {}
        for room in rooms:
            occupant_list = room.occupants
            occupant_details = {}
            if len(occupant_list) > 0:
                for occupant in occupant_list:
                    name = ' '.join(occupant.person_name)
                    occupant_details[occupant.person_id] = name
                allocations_data[room.room_name] = [occupant_details, room.room_type.upper()]
            else:
                allocations_data[room.room_name] = ['Room is empty', room.room_type.upper()]

        self.print_message('Total Rooms available: {offices} Offices and {livingspaces} Living spaces'.format(offices=len(self.office_block), livingspaces=len(self.living_spaces)))
        self.print_message('{staff} Staff Members and {fellows} Fellows are currently accommodated'.format(staff=len(self.staff_members), fellows=len(self.fellows)))

        for room_name, room_details in allocations_data.items():
            print('\n')
            self.print_message('Room name: {name}{space: >20}Room Type: {type}'.format(name=room_name.upper(), space=' ', type=room_details[1]), 'info')  # Additional feature, specify room type
            self.print_message('{line:->60}'.format(line='-'))
            self.print_message('Room Occupants:\n', 'info')

            if isinstance(room_details[0], str):
                msg = '{:^60}'.format('ROOM IS EMPTY', 'error')
                self.print_message(msg, 'error')
                print('\n')
            else:
                for person_id, name in room_details[0].items():
                    self.print_message('{space: >15}{name: <20} - {id: <10}'.format(space='*', name=name, id=person_id))
            self.print_message('{:_^80}'.format('_'), 'error')

        if output_file:
            if not output_file.endswith('.txt'):
                self.print_message('The output file specified is not a valid text file. Data will not be saved\n', 'error')
                return

            with open(output_file, 'w+') as f:
                f.writelines('Room Name: {name}        Room Type: {type}\n{space:_>60}\n\nRoom Occupants: {occupants}\n\n'.format(space='_', name=k, type=v[1], occupants=v[0]) for k,
                                                                                                                                                                       v in allocations_data.items())
                f.write('\n')
            self.print_message('Room allocations saved to file {}'.format(output_file))

    def print_unallocated(self, unallocated_file_name):
        '''
        Function to print list of the unallocated people
        :param unallocated_file_name: an optional  text (.txt) file to which unallocated people names shall be saved.
        :return: prints list of unallocated people if available, or error messages.
        '''

        self.title_printer('UN-ALLOCATED PERSONS')

        unallocated_people = set(self.un_allocated_persons['fellows_office'] + self.un_allocated_persons['staff'] + self.un_allocated_persons['fellows_acc'])

        if len(unallocated_people) == 0:
            self.print_message('There are currently no unallocated people', 'info')
            return
        else:
            unallocated_data = {}
            for person in unallocated_people:
                name = ' '.join(person.person_name)
                person_id = person.person_id

                if person in set(self.un_allocated_persons['fellows_office']) & set(self.un_allocated_persons['fellows_acc']):
                    needs = 'Livingspace and Office'

                elif person in self.un_allocated_persons['fellows_office'] or person in self.un_allocated_persons['staff']:
                    needs = 'Office'

                elif person in self.un_allocated_persons['fellows_acc'] and person not in self.un_allocated_persons['fellows_office']:
                    needs = 'Livingspace'

                unallocated_data[person_id] = name, needs

            self.print_message('{pn: <20}  {name: <35}{ua: <15}'.format(name='NAME', ua='UNALLOCATED', pn='PERSONNEL NUMBER'))

            for person_id, person_details in unallocated_data.items():
                self.print_message('  {number: <20}{name: <35}{needs: <15}'.format(needs=person_details[1], name=person_details[0], number=person_id), 'info')
            print('\n')

            if unallocated_file_name:
                if not unallocated_file_name.endswith('.txt'):
                    self.print_message('Invalid output file format', 'error')
                    return

                with open(unallocated_file_name, 'w') as f:
                    f.write('Unallocated  Persons')
                    f.write('\n({pn: <10}{name: <30}{wants: <15}\n'.format(pn='P.NUMBER', name='NAME', wants='WANTS'))
                    f.writelines('{person_id: <10}{name: <30}{needs: <15}\n'.format(name=v[0], needs=v[1], person_id=k) for k, v in unallocated_data.items())

                self.print_message('List of the unallocated saved to {}'.format(unallocated_file_name))
                print('\n')

    def print_free_rooms(self):
        '''Function to print a list of the rooms with free space'''

        self.title_printer('AVAILABLE ROOMS')

        if self.office_block:
            free_offices = [x for x in self.office_block if len(x.occupants) < self.office_max_occupants]
            offices_data = {}
            for office in free_offices:
                offices_data[office.room_name] = self.office_max_occupants - len(office.occupants)

            if bool(offices_data):
                self.print_message('{name: <30}{avail_space: <15}'.format(name='OFFICE NAME', avail_space='AVAILABLE SPACE'))
                for office, space_available in offices_data.items():
                    self.print_message('  {name: <30} -{space: <3}'.format(name=office, space=space_available))
            else:
                self.print_message('No Office space available')

        else:
            self.print_message('No offices available')

        if self.living_spaces:
            free_livingspaces = [x for x in self.living_spaces if len(x.occupants) < self.livingspace_max_occupants]
            livingspaces_data = {}
            for room in free_livingspaces:
                livingspaces_data[room.room_name] = self.livingspace_max_occupants - len(room.occupants)

            if bool(livingspaces_data):
                self.print_message('{name: <30}{avail_space: <10}'.format(name='LIVINGSPACE NAME', avail_space='AVAILABLE SPACE'))
                for name, spaces_available in livingspaces_data.items():
                    self.print_message('  {name: <30} -{space: <3}'.format(name=name, space=spaces_available))
            else:
                self.print_message('No space available in livingspaces.')

        else:
            self.print_message('No livingspaces available.')


    def load_people(self, text_file):
        '''
        Function to load people into rooms from a specified text file
        :param text_file: Input text file that contains list of people
        :return: Print status messages or returns error messages.
        '''

        if not text_file.endswith('.txt'):
            self.print_message('Invalid input file name', 'error')
            return

        if not os.path.isfile(text_file): # To check if file exists
            self.print_message('The specified file does not exist', 'error')
            return

        with open(text_file) as f:
            content = f.readlines()

            stripped_content = [x.strip() for x in content]

        for person in stripped_content:
            details = person.split(' ')
            name = [details[0], details[1]]
            person_type = details[2].title()        # Convert the person type to Title case
            try:
                wants_accommodation = details[3]
            except IndexError:
                wants_accommodation = None

            self.add_person(name, person_type, wants_accommodation)

    def names_check(self, name):
        '''
        Function to validate name variables
        :param name: String to be validated
        :return: True if validated, else False
        '''

        if len(name) <= 1 or name.isnumeric():
            return False

        chars = ['#', '$', '%', '^', '*', '?', '!', '<', '>', ':', ';', '(', ')', '{', '}']  # Set of characters not allowed to be in name strings

        for char in chars:
            if char in name:
                return False
        return True

    def reallocate_person(self, relocate_id, new_room):
        ''' Function to reallocate a person from one room to another one.
        :argument relocate_id:This is the id of the person to me moved.
        :argument new_room: THe room a person specified by the relocate_id is to be moved to.
        :return: None.
        '''

        self.title_printer('REALLOCATE PERSON')

        available_people = list(itertools.chain(self.fellows, self.staff_members))  # List of all people objects present
        available_people_ids = [x.person_id for x in available_people]  # List of available people ids

        if relocate_id not in available_people_ids:
            self.print_message('Employee {} does not exist'.format(relocate_id), 'error')
            return

        person_object = [x for x in available_people if x.person_id == relocate_id][0]  # Get person object belonging to the specified ID

        available_rooms = list(itertools.chain(self.office_block, self.living_spaces)) # Get list of all room object available.
        current_rooms_occupied = [x for x in available_rooms if person_object in x.occupants]  # Find current room(s) occupied by person

        current_occupied_room_names = [x.room_name for x in current_rooms_occupied]

        if new_room in current_occupied_room_names:
            self.print_message('You cannot relocate a person to a room they are currently occupying.', 'error')
            return

        available_rooms = list(itertools.chain(self.office_block, self.living_spaces))
        available_room_names = [x.room_name for x in available_rooms]

        if new_room in available_room_names:
            room_object = [x for x in available_rooms if x.room_name == new_room][0]
        else:
            self.print_message('Room {} does not exist.'.format(new_room), 'error')
            return

        if room_object.room_type == 'office':
            if len(room_object.occupants) == 6:
                self.print_message('Office {} is fully occupied'.format(new_room), 'error')
                return
            else:
                try:
                    current_office_occupied = [x for x in current_rooms_occupied if x.room_type == 'office'][0] # Get current office occupied and remove person
                    current_office_occupied.occupants.remove(person_object)
                except IndexError: # person was unallocated.
                    pass
                room_object.occupants.append(person_object)  # Add person to new room
                self.print_message('{} has been re-allocated to room {}'.format(person_object.person_name[0], new_room))

        elif room_object.room_type == 'livingspace':

            if person_object in self.staff_members: # If person is staff, return as they are not eligible for accommodation.
                self.print_message('Staff are not eligible for accommodation', 'error')
                return

            if len(room_object.occupants) == 4:
                self.print_message('Livingspace {} is fully occupied'.format(new_room), 'error')
                return
            else:
                try:
                    current_livingspace_occupied = [x for x in current_rooms_occupied if x.room_type == 'livingspace'][0] # Get current livingspace occupied, and remove perso
                    current_livingspace_occupied.occupants.remove(person_object)
                except IndexError: # person was unallocated
                    pass
                room_object.occupants.append(person_object)  # Add person to new room
                self.print_message('{} has been re-allocated to room {}'.format(person_object.person_name[0], new_room))

    def remove_person(self, personnel_id):
        '''
        To remove a person from the record
        :param personnel_id: The person_id who is to be removed.
        :return: None. Prints to the screen status messages.
        '''

        self.title_printer('REMOVE PERSON')

        regex = re.compile(r'^AND\/(S|F)\/(\d{3})')

        if not regex.search(personnel_id):
            self.print_message('Incorrect Personnel ID format')
            return

        available_people = list(itertools.chain(self.fellows, self.staff_members))  # List of all people objects present
        available_people_ids = [x.person_id for x in available_people]  # List of available people ids

        if personnel_id not in available_people_ids:
            self.print_message('Employee {} does not exist'.format(personnel_id), 'error')
            return

        person_object = [x for x in available_people if x.person_id == personnel_id][0]  # Get person object belonging to the specified ID

        if personnel_id.split('/')[1] == 'S':  # If the person is staff
            self.staff_members.remove(person_object)
            self.print_message('Staff member {} has been removed from Staff Members list.'.format(' '.join(person_object.person_name)), 'info')

        elif personnel_id.split('/')[1] == 'F':
            self.fellows.remove(person_object)
            self.print_message('Fellow {} has been removed from Fellows list.'.format(' '.join(person_object.person_name)), 'info')

        available_rooms = list(itertools.chain(self.office_block, self.living_spaces))

        occupied_rooms = [x for x in available_rooms if person_object in x.occupants]

        if len(occupied_rooms) == 0:  # If the person was unallocated.
            self.print_message('The specified person did not occupy any room.', 'info')
            for list_of_unallocated in (self.un_allocated_persons['fellows_acc'], self.un_allocated_persons['staff'], self.un_allocated_persons['fellows_office']):
                if person_object in list_of_unallocated:
                    list_of_unallocated.remove(person_object)
                    self.print_message('Employee No: {} Has been removed from the records'.format(personnel_id))

        else: # Employee occupied at least one room
            for room in occupied_rooms:
                room.occupants.remove(person_object)
                self.print_message('Employee has been removed from {type} {name}'.format(type=room.room_type, name=room.room_name))



    def load_state(self, database_name):
        '''
        Function to load data from the specified database
        :param database_name: The sqlite database that contains the data
        :return: prints confirmation message that the data has been loaded or error message in case of failure.
        '''

        self.title_printer('LOAD FROM DATABASE')

        if not os.path.isfile(database_name):
            self.print_message('The specified database does not exist.')
            return

        if not str(database_name).endswith('.db') or not str(database_name).endswith('.sqlite'):
            self.print_message('The specified file is not a valid database file.')
            return

    def save_state(self, database_name):
        '''
        Fuction to save the program data to a specified database, or to a default one if none is specified
        :param database_name: The database, if specified to which data will be saved in.
        :return: Print statement on success or errors.
        '''

        self.title_printer('SAVE TO DATABASE')

        changes = False # Flag to track if theres data to be saved

        if database_name is None:
            db_name = 'data/amity_data.db'
        else:
            if not str(database_name).endswith('.db'): # Enforce database name to end in '.db'
                self.print_message('Invalid database name. Make sure the name ends with ".db".', 'error')
                return
            db_name = 'data/' + database_name

        # If database exists, back it up first, then delete after successful saving to fresh database.
        if os.path.exists(db_name):
            os.rename(db_name, db_name + '-backup')

        engine = create_engine("sqlite:///{}".format(db_name))

        Base.metadata.bind = engine
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()

        if self.fellows:
            changes = True
            self.print_message('Saving Fellows data...')
            for fellow in self.fellows:
                name = ' '.join(fellow.person_name)
                new_fellow = FellowDb(person_name=name, person_id=fellow.person_id)
                session.add(new_fellow)
            session.commit()
        else:
            self.print_message('No fellows around...', 'info')

        if self.staff_members:
            changes = True
            self.print_message('Saving Staff data...')
            for staff in self.staff_members:
                name = ' '.join(staff.person_name)
                new_staff = StaffDb(person_name=name, person_id=staff.person_id)
                session.add(new_staff)
            session.commit()

        else:
            self.print_message('No staff to save at this moment', 'info')

        if self.office_block:
            changes = True
            self.print_message('Saving offices data...')
            for room in self.office_block:
                people_ids = [x.person_id for x in room.occupants]
                id_string = ', '.join(str(x) for x in people_ids)
                new_room = OfficeblockDb(room_name=room.room_name, room_occupants=id_string)
                session.add(new_room)
            session.commit()
        else:
            self.print_message('No offices available', 'info')

        if self.living_spaces:
            changes = True
            self.print_message('Saving livingspace data...')
            for room in self.living_spaces:
                people_ids = [x.person_id for x in room.occupants]
                id_string = ', '.join(str(x) for x in people_ids)
                livingspace = LivingspaceDb(room_name=room.room_name, room_occupants=id_string)
                session.add(livingspace)
            session.commit()

        else:
            self.print_message('No living paces available...', 'info')

        fellows_office = self.un_allocated_persons['fellows_office']
        fellows_accommodation = self.un_allocated_persons['fellows_acc']
        staff = self.un_allocated_persons['staff']

        fellows = fellows_office + fellows_accommodation

        if fellows:
            for person in fellows_office:
                name = ' '.join(person.person_name)
                person_id = person.person_id

                if person in fellows_accommodation and person in fellows_office:
                    need = 'accommodation and office'

                elif person in fellows_office and person not in fellows_accommodation:
                    need = 'office'

                elif person in fellows_accommodation:
                    need = 'accommodation'

                unallocated_person = UnallocatedDb(person_name=name, person_id=person_id, person_type='fellow', need=need)
                session.add(unallocated_person)
                session.commit()
        else:
            self.print_message('No fellows currently unallocated', 'info')

        if staff:
            changes = True
            self.print_message('Saving unallocated staff data...')
            for person in staff:
                name = ' '.join(person.person_name)
                unallocated_person = UnallocatedDb(person_name=name, person_id=person.person_id, person_type='staff', need='office')
                session.add(unallocated_person)
            session.commit()
        else:
            self.print_message('No staff currently unallocated', 'info')

        rooms_max_occupants = MaxRoomOccupants(office_max_occupants=self.office_max_occupants, livingspace_max_occupants=self.livingspace_max_occupants)
        session.add(rooms_max_occupants)

        current_employment_id = PersonelIdsDb(self.personnel_id)
        session.add(current_employment_id)
        session.commit()

        if changes:
            self.print_message('Program data successfully saved to {}!'.format(db_name))
            try:
                os.unlink(db_name + '-backup')  # Delete backed-up data, if present
            except:
                pass

            self.data_saved = True

        else:
            self.print_message('No data to save.', 'info')

    def exit_gracefully(self):
        '''Function to ensure the programs prompts the user to save data if theres any data in the program when exit command is entered'''

        changes = False # Flag to indicate presence of data in the program at exit time

        for data_field in (self.fellows, self.staff_members, self.un_allocated_persons['fellows_office'], self.un_allocated_persons['staff'], self.un_allocated_persons['fellows_acc'],self.office_block,
                           self.living_spaces):
            if data_field:
                changes = True
            else:
                pass

        while True:
            if changes and not self.data_saved:  # When there is data in the system
                self.print_message('There is unsaved data. Do you want to SAVE?')
                response = input('{qn: >100}'.format(qn='Type YES to save now, NO to exit without saving. Response:  '))
            else:
                print('\n\n')
                self.print_message('{spacer:*^80}'.format(spacer='Amity Manager: Session Ended'))
                print('\n')
                sys.exit()

            if response == 'YES' or response == 'Yes':
                self.save_state(None)
                self.print_message('{msg: <80}'.format(msg='Data Saved. Session shall be Ended.'))
                self.print_message('{msg:*^80}'.format(msg='Amity Manager: Session Ended'))
                sys.exit()

            elif response == 'No' or response == 'NO':
                self.print_message('{msg: ^80}'.format(msg='Data Not Saved'), 'error')
                self.print_message('{msg:*^80}'.format(msg='Amity Manager: Session Ended'))
                print('\n')
                sys.exit()

            else:
                print('\n')
                self.print_message('      Incorrect response.', 'error')



