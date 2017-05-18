#!/usr/bin/python3
# -*- coding: utf-8 -*-
import random
from models.person import Staff, Fellow
from models.room import Office, LivingSpace
import os


class AmityManager(object):
    '''
    Class Dojo to model the amity complex, and manage all the data models
    '''
    fellows = []
    staff_members = []
    office_block = []
    living_spaces = []
    un_allocated_persons = []
    personnel_id = 1

    def create_room(self, room_names, room_type):
        '''
        Function to create a room in the amity model
        :param user_input: cli arguments from which room_name and room_type arguments are parsed.
        :return: specific errors incase of any errors or print statements to display status.
        '''

        for room_name in room_names:
            if self.names_check(room_name):
                pass
            else:
                print('{} is not a valid room name. Room not created'.format(room_name))
                continue
            # Get list of already existing room names.
            existing_room_names = [x.room_name for x in self.office_block] + [x.room_name for x in self.living_spaces]
            if room_name in existing_room_names:
                print('A room called {} already exists\n'.format(room_name))
                continue
            self.add_room(room_name, room_type)

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
            print('An Office called {0} has been successfully created!\n'.format(room_name))

        elif room_type == 'Livingspace':
            livingspace_instance = LivingSpace()
            room = livingspace_instance.create_room(room_name, 'livingspace')
            self.living_spaces.append(room)
            print('A Livingspace called {0} has been successfully created!\n'.format(room_name))

    def add_person(self, name, person_type, wants_accommodation):
        '''
        Function to add individuals to the amity
        :param name: List of new persons name [first_name, second_name]
        :param wants_accommodation: argument that specifies if person to be added wants accommodation or not. Should be either 'Y', 'N', 'y' or 'n' 
        :param person_type: New person type, either 'Staff' or 'Fellow'
        :return: prints to the console on successful creation, returns relevant error messages on errors
        '''

        if not self.names_check(name[0]) or not self.names_check(name[1]):
            print('Invalid Person Name.')
            return

        if wants_accommodation:
            if person_type == 'Staff':
                print('Staff are not entitled to accommodation\n')
                return

            if wants_accommodation.lower() == 'y':
                accommodation = True

            elif wants_accommodation.lower() == 'n':
                accommodation = False

            else:
                print('Argument for Accommodation can only be either Y/y or N/n\n')
                return
        else:
            accommodation = False

        if person_type == 'Fellow':
            person_class = Fellow()
            person = person_class.add_person(name, accommodation, self.personnel_id)
            self.fellows.append(person)
            self.allocate_office(person)
            self.personnel_id += 1
            if accommodation:
                self.allocate_livingspace(person)

        elif person_type == 'Staff':
            person_class = Staff()
            person = person_class.add_person(self.personnel_id, name)
            self.allocate_office(person)
            self.staff_members.append(person)
            self.personnel_id += 1

    def allocate_livingspace(self, person):
        '''Function to randomly allocate a livingroom to fellows'''

        if len(self.living_spaces) == 0:
            print('No Livingroom currently available for allocation\n')
            if person.person_name not in self.un_allocated_persons:
                self.un_allocated_persons.append(person)
            return

        available_rooms = [x for x in self.living_spaces if len(x.occupants) < 4]

        if len(available_rooms) == 0:
            print('Sorry, No livingspace currently available in any of the rooms\n')
            return

        random_room = random.choice(available_rooms)
        random_room.occupants.append(person)

        print('{0} has been allocated the livingspace {1}\n'.format(person.person_name[0], random_room.room_name))

    def allocate_office(self, person):
        '''Function to randomly allocate an office to fellows and staff'''
        if len(self.office_block) == 0:
            print('No Offices currently available for allocation\n')
            if person.person_name not in self.un_allocated_persons:
                self.un_allocated_persons.append(person)
            return

        available_rooms = [x for x in self.office_block if len(x.occupants) < 6]

        if len(available_rooms) == 0:
            print('\nSorry, No space currently available in any of the Offices')
            self.un_allocated_persons.append(person)
            return

        random_office = random.choice(available_rooms)
        random_office.occupants.append(person)

        print('{0} has been allocated the office {1}\n'.format(person.person_name[0], random_office.room_name))

    def print_room(self, room_name):
        '''Prints the names of all the people in ​specified room_name​.'''
        available_rooms = self.office_block + self.living_spaces
        available_room_names = [x.room_name for x in available_rooms]

        if room_name not in available_room_names:
            print('Room {} Seems not to exist. Kindly Confirm room name\n'.format(room_name))
            return

        room_object = [x for x in available_rooms if x.room_name == room_name][0]
        occupant_list = room_object.occupants

        if len(occupant_list) == 0: # When a room is empty
            print_output = 'Room {} is empty'.format(room_name)
        else:
            print_names = []
            for occupant in occupant_list:
                name = ' '.join(occupant.person_name)
                print_names.append(name)

            print_output = ', '.join(print_names)

        print('Occupants of room {} : {}\n'.format(room_name, print_output))

    def print_allocations(self, user_input):
        '''
        Function to print room allocations, and optionally output same to file
        :param user_input from which output filename if present is parsed from.
        :return: Returns relevant error messages, or prints out information on success
        '''


        if user_input['<-o=filename>']:
            output_file = user_input['<-o=filename>']

            if not output_file.endswith('.txt'):
                print('The output file not a valid text file')
                return 'The output file not a valid text file\n'

        rooms = self.office_block + self.living_spaces
        if len(rooms) == 0:
            print('No rooms currently occupied\n')
            return

        for room in rooms:
            occupant_list = room.occupants
            room_occupant_names = []
            if len(occupant_list) > 0:
                for occupant in occupant_list:
                    name = ' '.join(occupant.person_name)
                    room_occupant_names.append(name)
                out = {room.room_name : ', '.join(room_occupant_names)}

                for key, values in out.items():
                    print(key)
                    print('___________________')
                    print(values)
                    print('\n')

                if user_input['<-o=filename>']:
                    with open(output_file, 'a') as f:
                        f.writelines('{}\n_____\n{}'.format(k, v) for k, v in out.items())
                        f.write('\n\n')
                    print('Room allocations saved to file {}'.format(output_file))

    def print_unallocated(self, unallocated_file_name):
        '''
        Function to print list of the unallocated people
        :param unallocated_file_name: a text (.txt) file to which unallocated people names shall be saved.
        :return: prints list of unallocated people if available, or error messages.
        '''
        ''''''

        if len(self.un_allocated_persons) == 0:
            print('There are currently no unallocated people')
            return
        else:
            un_allocated_list = set(self.un_allocated_persons)
            names = [x.person_name for x in un_allocated_list] #list of names in the form [firstname, lastnames]
            list_of_names = [' '.join(x) for x in names] # Join names together
            out = '\n'.join(list_of_names)
            print(out)

            if unallocated_file_name:
                output_file = unallocated_file_name
                if not output_file.endswith('.txt'):
                    print('Invalid output file format')
                    return

                with open(output_file, 'w') as f:
                    f.write(out)
                print('List of the unallocated saved to {}'.format(output_file))

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
        '''
        Function to validate name variables
        :param name: String to be validated
        :return: True if validated, else False
        '''
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
            print('Employee {} does not exist'.format(relocate_id))
            return

        person_object = [x for x in available_people if x.person_id == int(relocate_id)][0]  # Get person object belonging to the specified ID
        available_rooms = self.office_block + self.living_spaces # Get list of all room object available.
        current_room_occupied = [x for x in available_rooms if person_object in x.occupants][0] # Find current room occupied by person

        if current_room_occupied.room_name == new_room:
            print('Cant relocate a person to a room he/she is currently occupying.')
            return

        available_rooms = self.office_block + self.living_spaces
        available_room_names = [x.room_name for x in available_rooms]

        if new_room not in available_room_names:
            print('Room {} Does Not Exist.'.format(new_room))
            return

        room_object = [x for x in available_rooms if x.room_name == new_room][0]

        if room_object.room_type == 'office':
            if len(room_object.occupants) == 6:
                print('Office {} is fully occupied'.format(new_room))
                return
            else:
                room_object.occupants.append(person_object)
                print('{} has been re-allocated to room {}'.format(person_object.person_name[0], new_room))
                current_room_occupied.occupants.remove(person_object)

        elif room_object.room_type == 'livingspace':
            if len(room_object.occupants) == 4:
                print('Livingspace {} is fully occupied'.format(new_room))
                return
            else:
                room_object.occupants.append(person_object)
                print('{} has been re-allocated to room {}'.format(person_object.person_name[0], new_room))
                current_room_occupied.occupants.remove(person_object)



