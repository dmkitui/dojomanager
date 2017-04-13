#!/usr/bin/python3
# -*- coding: utf-8 -*-
import random
from person.person import Staff, Fellow
from room.room import Office, LivingSpace


class DojoManager(object):
    '''
    Class Dojo to model the dojo complex, and manage all the data models
    '''
    fellows = []
    staff_members = []
    office_block = []
    livingspaces = []
    un_allocated = []

    def create_room(self, user_input):

        if user_input['Livingspace']:
            room_type = 'Livingspace'
        else:
            room_type = 'Office'

        room_names = user_input['<room_name>']
        existing_rooms = self.livingspaces + self.office_block
        existing_room_names = [x.room_name for x in existing_rooms] # Get list of already existing room names

        for room_name in room_names:
            if room_name in existing_room_names:
                print('A Room called {} already exists\n'.format(room_name))
                continue
            self.add_room(room_name, room_type)

    def add_room(self, room_name, room_type):
        '''Function to call create_room function for the case of multiple
        room arguments'''
        if room_type == 'Office':
            a = Office()
            room = a.create_room(room_name, 'office')
            self.office_block.append(room)
            print('An Office called {0} has been successfully created!\n'.format(room_name))

        elif room_type == 'Livingspace':
            b = LivingSpace()
            room = b.create_room(room_name, 'livingspace')
            self.livingspaces.append(room)
            print('A Livingspace called {0} has been successfully created!\n'.format(room_name))

    def add_person(self, user_input):

        '''Funcction to add individuals to the dojo'''
        name = user_input['<person_name>']
        wants_accommodation = user_input['<wants_accommodation>']

        if wants_accommodation:
            if user_input['Staff']:
                print('Staff are not entitled to accommodation\n')
                return 'Staff are not entitled to accommodation\n'

            if wants_accommodation.lower() == 'y':
                accommodation = True

            elif wants_accommodation.lower() == 'n':
                accommodation = False

            else:
                print('Argument for Accomodation can only be either Y or N\n')
                return 'Argument for Accomodation can only be either Y or N\n'
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
        '''Function to randomly allocate a livingroom to fellows'''

        if len(self.livingspaces) == 0:
            print('No Livingroom currently available for allocation\n')
            if name not in self.un_allocated:
                self.un_allocated.append(' '.join(name))
            return 'No Livingroom currently available for allocation\n'

        available_rooms = [x for x in self.livingspaces if len(x.occupants) < 4]

        if len(available_rooms) == 0:
            print('Sorry, No livingspace currently available in any of the rooms\n')
            return

        random_room = random.choice(available_rooms)
        random_room.occupants.append(name)

        print('{0} has been allocated the livingspace {1}\n'.format(name[0], random_room.room_name))

    def allocate_office(self, name):
        '''Function to randomly allocate an office to fellows and staff'''
        if len(self.office_block) == 0:
            print('No Offices currently available for allocation\n')
            if name not in self.un_allocated:
                self.un_allocated.append(' '.join(name))
            return

        available_rooms = [x for x in self.office_block if len(x.occupants) < 6]

        if len(available_rooms) == 0:
            print('\nSorry, No space currently available in any of the Offices')
            self.un_allocated.append(' '.join(name))
            return

        random_office = random.choice(available_rooms)
        random_office.occupants.append(name)

        print('{0} has been allocated the office {1}\n'.format(name[0], random_office.room_name))

    def print_room(self, user_input):
        '''Prints the names of all the people in ​room_name​ on the screen.'''

        room_name = user_input['<room_name>']
        available_rooms = self.office_block + self.livingspaces
        available_room_names = [x.room_name for x in available_rooms]

        if room_name not in available_room_names:
            print('Room {} Seems not to exist. Kindly Confirm room name\n'.format(room_name))
            return 'Specified room Seems not to exist. Kindly Confirm room name\n'

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

        print('Occupants of room {} : {}\n'.format(room_name, print_output))

    def print_allocations(self, user_input):
        '''Function to print room allocations, and optionally output same to file'''

        if user_input['<-o=filename>']:
            output_file = user_input['<-o=filename>']

            if not output_file.endswith('.txt'):
                print('The output file not a valid text file')
                return 'The output file not a valid text file\n'

        rooms = self.office_block + self.livingspaces
        if len(rooms) == 0:
            print('No rooms currently occupied\n')
            return

        for room in rooms:
            occupant_list = room.occupants
            room_occupant_names = []
            if len(occupant_list) > 0:
                for occupant in occupant_list:
                    name = ' '.join(occupant)
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

    def print_unallocated(self, user_input):
        '''prints list of the unallocated people'''

        if len(self.un_allocated) == 0:
            print('There are currently no unallocated people')
            return 'There are currently no unallocated people'
        else:
            un_allocated_list = set(self.un_allocated)
            out = '\n'.join(un_allocated_list)
            print(out)

            if user_input['<-o=filename>']:
                output_file = user_input['<-o=filename>']
                if not output_file.endswith('.txt'):
                    print('Invalid file format')
                    return 'Invalid file format'

                with open(output_file, 'w') as f:
                    f.write(out)
                print('List of the unallocated saved to {}'.format(output_file))



    def load_people(self, user_input):
        '''Function to laod people into rooms from a specified text file'''

        text_file = user_input['<people_file>']

        if not text_file.endswith('.txt'):
            print('Invalid text file name')
            return 'Invalid text file name'

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

