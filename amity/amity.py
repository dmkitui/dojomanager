#!/usr/bin/python3
# -*- coding: utf-8 -*-
import random
import shutil
from models.person import Staff, Fellow
from models.room import Office, LivingSpace
from models.database import Base, FellowDb, StaffDb, OfficeblockDb, LivingspaceDb, PersonelIdsDb, UnallocatedDb
import os
from blessings import Terminal
<<<<<<< HEAD
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

=======
>>>>>>> develop


class AmityManager(object):
    '''
    Class Dojo to model the amity complex, and manage all the data models
    '''
    fellows = []
    staff_members = []
    office_block = []
    living_spaces = []
    un_allocated_persons = {'fellows': [], 'staff': []}
    personnel_id = 1

    def print_message(self, message, message_state='success'):
        '''
        Function that prints out messages and program state to the terminal
        :param message: Message to be printed to the screen
        :param message_state: If message is success mesage, or error message. Default is 'success'
        :return: None
        '''
        terminal = Terminal()
        # margin from the left of terminal.
        width = shutil.get_terminal_size().columns
        margin = int(width) - 20
        spacer = ' ' * int(margin / 4)

        if message_state == 'success':
            state = terminal.green
        elif message_state == 'error':
            state = terminal.red

        print('{spacer}{state}{message}{terminal_normal}'.format(state=state, spacer=spacer, message= message, terminal_normal=terminal.normal))

    def create_room(self, room_names, room_type):
        '''
        Function to create a room in the amity model
        :param user_input: cli arguments from which room_name and room_type arguments are parsed.
        :return: specific errors incase of any errors or print statements to display status.
        '''
        print('\n')
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

    def add_person(self, name, person_type, wants_accommodation):
        '''
        Function to add individuals to the amity
        :param name: List of new persons name [first_name, second_name]
        :param wants_accommodation: argument that specifies if person to be added wants accommodation or not. Should be either 'Y', 'N', 'y' or 'n' 
        :param person_type: New person type, either 'Staff' or 'Fellow'
        :return: prints to the console on successful creation, returns relevant error messages on errors
        '''
        print('\n')
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
            new_fellow = person_class.add_person(name, accommodation, self.personnel_id)
            self.personnel_id += 1  # increment personel_id variable for the next employee
            self.fellows.append(new_fellow)
            self.print_message('Fellow {0} {1} has been successfully added.'.format(new_fellow.person_name[0], new_fellow.person_name[1]))
            # self.allocate_office(person)
            random_office = self.allocate_office()

            if random_office:
                random_office.occupants.append(new_fellow)
                self.print_message('{0} has been allocated the office {1}'.format(new_fellow.person_name[0], random_office.room_name))
            else:
                un_allocated_fellows = self.un_allocated_persons['fellows']
                if new_fellow not in un_allocated_fellows:
                    un_allocated_fellows.append(new_fellow)
                    self.un_allocated_persons['fellows'] = un_allocated_fellows

            if accommodation:
                random_livingspace = self.allocate_livingspace()
                if random_livingspace:
                    random_livingspace.occupants.append(new_fellow)
                    self.print_message('{0} has been allocated the livingspace {1}'.format(new_fellow.person_name[0], random_livingspace.room_name))
                else:
                    un_allocated_fellows = self.un_allocated_persons['fellows']
                    if new_fellow not in un_allocated_fellows:
                        un_allocated_fellows.append(new_fellow)
                        self.un_allocated_persons['fellows'] = un_allocated_fellows
            else:
                self.print_message('{0} does not wish to be accommodated'.format(new_fellow.person_name[0]))

        elif person_type == 'Staff':
            person_class = Staff()
            new_staff = person_class.add_person(name, self.personnel_id)
            self.staff_members.append(new_staff)
            self.personnel_id += 1
            self.print_message('Staff {0} {1} has been successfully added.'.format(new_staff.person_name[0], new_staff.person_name[1]))
<<<<<<< HEAD

            random_office = self.allocate_office()
            if random_office:
                random_office.occupants.append(new_staff)
                self.print_message('{0} has been allocated the office {1}'.format(new_staff.person_name[0], random_office.room_name))
            else:
                un_allocated_staff = self.un_allocated_persons['staff']
                if new_staff not in un_allocated_staff:
                    un_allocated_staff.append(new_staff)
                    self.un_allocated_persons['staff'] = un_allocated_staff
        print('\n')

=======

            random_office = self.allocate_office()
            if random_office:
                random_office.occupants.append(new_staff)
                self.print_message('{0} has been allocated the office {1}'.format(new_staff.person_name[0], random_office.room_name))
            else:
                un_allocated_staff = self.un_allocated_persons['staff']
                if new_staff not in un_allocated_staff:
                    un_allocated_staff.append(new_staff)
                    self.un_allocated_persons['staff'] = un_allocated_staff
        print('\n')

>>>>>>> develop
    def allocate_livingspace(self):
        '''Function to randomly allocate a livingroom to fellows'''

        if len(self.living_spaces) == 0:
            self.print_message('No Livingroom currently available for allocation', 'error')
            return None

        available_rooms = [x for x in self.living_spaces if len(x.occupants) < 4]

        if len(available_rooms) == 0:
            self.print_message('Sorry, No livingspace currently available in any of the rooms', 'error')
            return None

        return random.choice(available_rooms)

    def allocate_office(self):
        '''Function to randomly allocate an office to fellows and staff'''
        if len(self.office_block) == 0:
            self.print_message('No Offices currently available for allocation', 'error')
            return None

        available_rooms = [x for x in self.office_block if len(x.occupants) < 6]

        if len(available_rooms) == 0:
            self.print_message('Sorry, No space currently available in any of the Offices', 'error')
            return None

        return random.choice(available_rooms)

    def print_room(self, room_name):
        '''Prints the names of all the people in ​specified room_name​.'''
        print('\n')
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

        title = '{:_^60}'.format('PRINT ROOM')
        self.print_message(title)
<<<<<<< HEAD

        self.print_message('Room Name: {}'.format(room_name.upper()))
        self.print_message('{space:->60}'.format(space='-'))
        self.print_message('Room Occupants: {}\n'.format(print_output))

=======

        self.print_message('Room Name: {}'.format(room_name.upper()))
        self.print_message('{space:->60}'.format(space='-'))
        self.print_message('Room Occupants: {}\n'.format(print_output))

>>>>>>> develop
    def print_allocations(self, output_file):
        '''
        Function to print room allocations, and optionally output same to file
        :param output_file: Optional text file to which the data is saved to.
        :return: Returns relevant error messages, or prints out information on success
        '''
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
                    occupant_details[name] = occupant.person_id
                allocations_data[room.room_name] = [occupant_details, room.room_type.upper()]
            else:
                allocations_data[room.room_name] = ['Room is empty', room.room_type.upper()]

        title = '{:_^60}'.format('ROOM ALLOCATIONS')
        print('\n')
        self.print_message(title)

        for room_name, room_details in allocations_data.items():
            print('\n')
            self.print_message('Room name: {name}{space: >20}Room Type: {type}'.format(name=room_name.upper(), space=' ', type=room_details[1]))  # Additional feature, specify room type
            self.print_message('{line:->60}'.format(line='-'))

            self.print_message('Room Occupants:\n')

            if isinstance(room_details[0], str):
                msg = '{:^60}'.format('ROOM IS EMPTY')
                self.print_message(msg)
                print('\n')
            else:
                for name, person_id in room_details[0].items():
                    self.print_message('{space: >15}{name: <20} - {id: <3}'.format(space='*', name=name, id=person_id))
                print('\n')

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
        ''''''

        if len(self.un_allocated_persons['fellows']) == 0 and len(self.un_allocated_persons['staff']) == 0:
            self.print_message('There are currently no unallocated people', 'error')
            return
        else:
            un_allocated_list = self.un_allocated_persons['fellows'] + self.un_allocated_persons['staff']
            unallocated_data = {}
            for person in un_allocated_list:
                name = ' '.join(person.person_name)
                person_id = person.person_id
                unallocated_data[name] = person_id

            title = '{:_^60}'.format('UNALLOCATED PERSONS')
            print('\n')
            self.print_message(title)
            self.print_message('NAME{0: >40}PERSONNEL NUMBER'.format(' '))
            # print('\n')
            for key, value in unallocated_data.items():
                self.print_message('{name: <25}{space: >29}{number}'.format(name=key, space=' ', number=value))
            print('\n')

            if unallocated_file_name:
                if not unallocated_file_name.endswith('.txt'):
                    self.print_message('Invalid output file format', 'error')
                    return

                with open(unallocated_file_name, 'w') as f:
                    f.write(title)
                    f.write('\nNAME{0: >40}PERSONNEL NUMBER\n'.format(' '))
                    f.writelines('{name: <25}{space: >29}{number}\n'.format(name=k, space=' ', number=v) for k, v in unallocated_data.items())

                self.print_message('List of the unallocated saved to {}'.format(unallocated_file_name))
                print('\n')

    def load_people(self, text_file):
        '''
        Function to load people into rooms from a specified text file
        :param text_file: Input text file that contains list of people
        :return: Print status messages or returns error messages.
        '''
        if not text_file.endswith('.txt'):
            print('Invalid input file name')
            return

        if not os.path.isfile(text_file): # To check if file exists
            print('The specified file does not exist')
            return

        with open(text_file) as f:
            content = f.readlines()

        content = [x.strip() for x in content]

        for person in content:

            details = person.split(' ')
            name = [details[0], details[1]]
            job_type = details[2]

            if job_type == 'FELLOW':
                fellow = True
                staff = False
            elif job_type == 'STAFF':
                staff = True
                fellow = False
                wants_accomodation = False

            if len(details) == 4:
                wants_accomodation = details[3]

            user_details = {
                '<person_name>': name,
                '<wants_accommodation>' : wants_accomodation,
                'Fellow': fellow,
                'Staff': staff
            }
            self.add_person(user_details)

    def names_check(self, name):
<<<<<<< HEAD
        '''
        Function to validate name variables
        :param name: String to be validated
        :return: True if validated, else False
        '''
=======
        '''
        Function to validate name variables
        :param name: String to be validated
        :return: True if validated, else False
        '''
>>>>>>> develop
        if len(name) <= 1 or name.isnumeric():
            return False

        chars = ['#', '$', '%', '^', '*', '?', '!', '<', '>', ':', ';']  # Set of characters not allowed to be in name strings

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
        available_people = self.fellows + self.staff_members  # List of all people objects present
        available_people_ids = [x.person_id for x in available_people]  # List of available people ids

        if int(relocate_id) not in available_people_ids:
            self.print_message('Employee {} does not exist'.format(relocate_id), 'error')
            return

        person_object = [x for x in available_people if x.person_id == int(relocate_id)][0]  # Get person object belonging to the specified ID
        available_rooms = self.office_block + self.living_spaces # Get list of all room object available.
        current_room_occupied = [x for x in available_rooms if person_object in x.occupants][0] # Find current room occupied by person

        if current_room_occupied.room_name == new_room:
            self.print_message('You cannot relocate a person to a room he/she is currently occupying.', 'error')
            return

        available_rooms = self.office_block + self.living_spaces
        available_room_names = [x.room_name for x in available_rooms]

        if new_room not in available_room_names:
            self.print_message('Room {} does not exist.'.format(new_room), 'error')
            return

        room_object = [x for x in available_rooms if x.room_name == new_room][0]

        if room_object.room_type == 'office':
            if len(room_object.occupants) == 6:
                self.print_message('Office {} is fully occupied'.format(new_room), 'error')
                return
            else:
                room_object.occupants.append(person_object)
                self.print_message('{} has been re-allocated to room {}'.format(person_object.person_name[0], new_room))
                current_room_occupied.occupants.remove(person_object)

        elif room_object.room_type == 'livingspace':
            if len(room_object.occupants) == 4:
                self.print_message('Livingspace {} is fully occupied'.format(new_room), 'error')
                return
            else:
                room_object.occupants.append(person_object)
                self.print_message('{} has been re-allocated to room {}'.format(person_object.person_name[0], new_room))
                current_room_occupied.occupants.remove(person_object)

    def load_state(self, database_name):
        '''
        Function to load data from the specified database
        :param database_name: The sqlite database that contains the data
        :return: prints confirmation message that the data has been loaded or error message in case of failure.
        '''
        if not os.path.isfile(database_name):
            self.print_message('The specified database does not exist.')
            return

        if not str(database_name).endswith('.db') or not str(database_name).endswith('.sqlite'):
            self.print_message('The specified file is not a valid database file.')
            return
<<<<<<< HEAD

    def save_state(self, database):
        '''
        Fuction to save the program data to a specified database, or to a default one if none is specified
        :param database: The database, if specified to which data will be saved in.
        :return: Print statement on success or errors.
        '''

        if database is None:
            db_name = 'amity_data.db'
        else:
            db_name = database

        # If database exists, back it up first, then delete after successful saving to fresh database.
        if os.path.exists(db_name):
            os.rename(db_name, db_name + '-backup')

        engine = create_engine("sqlite:///{}".format(db_name))

        Base.metadata.bind = engine
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()

        self.print_message('Saving program state')

        if self.fellows:
            self.print_message('Saving Fellows data...')
            for fellow in self.fellows:
                name = ' '.join(fellow.person_name)
                new_fellow = FellowDb(person_name=name, person_id=fellow.person_id)
                session.add(new_fellow)
            session.commit()
        else:
            self.print_message('No fellows around...')

        if self.staff_members:
            self.print_message('Saving Staff data...')
            for staff in self.staff_members:
                name = ' '.join(staff.person_name)
                new_staff = StaffDb(person_name=name, person_id=staff.person_id)
                session.add(new_staff)
            session.commit()

        else:
            self.print_message('No staff to save at this moment')

        if self.office_block:
            self.print_message('Saving offices data...')
            for room in self.office_block:
                people_ids = [x.person_id for x in room.occupants]
                id_string = ', '.join(str(x) for x in people_ids)
                new_room = OfficeblockDb(room_name=room.room_name, room_occupants=id_string)
                session.add(new_room)
            session.commit()
        else:
            self.print_message('No offices to speak of...')

        if self.living_spaces:
            self.print_message('Saving livingspace data...')
            for room in self.living_spaces:
                people_ids = [x.person_id for x in room.occupants]
                id_string = ', '.join(str(x) for x in people_ids)
                livingspace = LivingspaceDb(room_name=room.room_name, room_occupants=id_string)
                session.add(livingspace)
            session.commit()

        else:
            self.print_message('No livingspaces available...')

        fellows = self.un_allocated_persons['fellows']
        staff = self.un_allocated_persons['staff']

        if fellows:
            self.print_message('Saving unallocated fellow data...')
            for person in fellows:
                name = ' '.join(person.person_name)
                unallocated_person = UnallocatedDb(person_name=name, person_id=person.person_id, person_type='fellow')
                session.add(unallocated_person)
            session.commit()
        else:
            self.print_message('No fellows currently unallocated')

        if staff:
            self.print_message('Saving unallocated staff data...')
            for person in staff:
                name = ' '.join(person.person_name)
                unallocated_person = UnallocatedDb(person_name=name, person_id=person.person_id, person_type='staff')
                session.add(unallocated_person)
            session.commit()
        else:
            self.print_message('No staff currently unallocated')














=======
>>>>>>> develop

    def save_state(self, database='amity_data.db'):
        '''
        Fuction to save the program data to a specified database, or to a default one if none is specified
        :param database: The database to which data will be saved in.
        :return: Print statement on success or errors.
        '''
        pass

