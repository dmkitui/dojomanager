#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Test cases for the amity_manager.py module
'''

import unittest
from io import StringIO
import sys
import os
from os import path
from contextlib import contextmanager
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from amity.amity import AmityManager


# Context manager to capture terminal output of print statements as most of the functions don't return value but print to t he screen.
@contextmanager
def screen_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr # Return stdout as a generator.
    finally:
        sys.stdout, sys.stderr = old_out, old_err


class TestAmityModule(unittest.TestCase):
    '''Test cases to test the functionality of the amity_manager module
    '''
    def setUp(self):
        '''Setup the test instance'''
        self.amity_instance = AmityManager()

    # Manual implemetation of the tearDown() method, while I learn how to make it make work properly
    def reset(self):
        '''Reset the test environment'''

        self.amity_instance.fellows = []
        self.amity_instance.office_block = []
        self.amity_instance.living_spaces = []
        self.amity_instance.staff_members = []
        self.amity_instance.personnel_id = 0
        self.amity_instance.un_allocated_persons = {'fellows_acc': [], 'fellows_office': [], 'staff': []}
        self.amity_instance.personnel_id = 0  # Initial personnel number digit.
        self.amity_instance.office_max_occupants = 6  # number of maximum occupants an office can accommodate
        self.amity_instance.livingspace_max_occupants = 4  # number of maximum occupants a livingspace can accommodate
        self.amity_instance.data_saved = False
        try:
            os.unlink('data/*')
        except:
            pass

    def test_initial_state(self):
        '''Test initial states of the various lists'''

        self.reset()
        self.assertEqual([self.amity_instance.office_block, self.amity_instance.fellows, self.amity_instance.staff_members], [[], [], []])

    def test_add_invalid_person_name(self):
        '''Test adding a person with name abbreviations'''

        self.reset()
        with screen_output() as (terminal_output, err):
            self.amity_instance.add_person(['Daniel', 'Kitui'], 'person', 'Y')
        print_output = terminal_output.getvalue().strip()
        self.assertIn('Invalid person type specified. Valid options are Fellow and Staff only', print_output)

    def test_add_person_invalid_name(self):
        '''Test add person with invalid person name'''
        self.reset()

        with screen_output() as (terminal_output, err):
            self.amity_instance.add_person(['D@niel', 'K$tui'], 'fellow', 'Y')
        print_output = terminal_output.getvalue().strip()
        self.assertIn('Invalid Person Name. Person Name should not include any special characters or digits.', print_output)





    def test_create_office(self):
        '''Test successful creation of office.'''

        self.reset()
        with screen_output() as (terminal_output, err):
            green_office = self.amity_instance.create_room(['Green'], 'office')
        print_output = terminal_output.getvalue().strip()
        self.assertIn('An Office called Green has been successfully created!', print_output)
        self.assertEqual(len(self.amity_instance.office_block), 1, 'Office not added')

    def test_create_livingspace(self):
        '''Test creating livingspace'''

        self.reset()
        self.amity_instance.create_room(['Kenya'], 'livingspace')
        self.assertEqual(len(self.amity_instance.living_spaces), 1, 'Livingspace not added')

    def test_create_invalid_room_type(self):        # use wrong argument for room_type
        self.reset()
        with screen_output() as (terminal_output, err):
            self.amity_instance.create_room(['Uganda'], 'accommodation')
        print_output = terminal_output.getvalue().strip()
        self.assertIn('Invalid argument for room type. Valid room types are Office or Livingspace.', print_output)


    def test_create_multiple_offices(self):
        '''Test creating multiple offices'''

        self.reset()
        self.amity_instance.create_room(['Green', 'White', 'Blue'], 'office')
        self.assertEqual(len(self.amity_instance.office_block), 3, 'Multiple rooms not created')

    def test_create_multiple_livingspace(self):
        '''Test creating multiple living spaces'''

        self.reset()
        self.amity_instance.create_room(['Kenya', 'Uganda', 'Tz', 'Rwanda'], 'livingspace')
        self.assertEqual(len(self.amity_instance.living_spaces), 4, 'Multiple rooms not created')

    def test_create_already_existing_office(self):
        '''Test creating an already existing room'''

        self.reset()
        with screen_output() as (terminal_output, err):
            self.amity_instance.create_room(['Violet'], 'office')
        print_output = terminal_output.getvalue().strip()
        self.assertIn('An Office called Violet has been successfully created!', print_output)

        # Create second room with the same name
        with screen_output() as (terminal_output, err):
            self.amity_instance.create_room(['Violet'], 'office')
        print_output = terminal_output.getvalue().strip()
        self.assertIn('A room called Violet already exists', print_output)

    def test_invalid_room_names(self):
        '''Test invalid room names'''

        self.reset()
        with screen_output() as (terminal_output, err):
            self.amity_instance.create_room(['#Dojo'], 'office')

        print_output = terminal_output.getvalue().strip()
        self.assertIn('#Dojo is not a valid room name. Room names should not include special characters or digits. Room not created', print_output)

    def test_add_person_no_rooms_available(self):
        '''Test adding person when no room is available'''

        self.reset()
        with screen_output() as (terminal_output, err):
            dan = self.amity_instance.add_person(['Daniel', 'Kitui'], 'staff', None)
        print_output = terminal_output.getvalue().strip()
        # self.assertEquals(print_output,
        self.assertEqual(len(self.amity_instance.staff_members), 1)
        self.assertEqual(len(self.amity_instance.un_allocated_persons['staff']), 1)

    def test_add_person_staff_with_wants_accommodation(self):
        '''Test adding staff with a argument for wants accommodation'''

        self.reset()
        with screen_output() as (terminal_output, err):
            dan = self.amity_instance.add_person(['Daniel', 'Kitui'], 'staff', 'Y')
        print_output = terminal_output.getvalue().strip()
        self.assertIn('Staff are not entitled to accommodation', print_output)

    def test_add_person_with_wrong_wants_accommodation_argument(self):
        '''Tests adding a person with an invalid wants_accommodation argument'''

        self.reset()
        with screen_output() as (terminal_output, err):
            dan = self.amity_instance.add_person(['Daniel', 'Kitui'], 'fellow', 'No')
        print_output = terminal_output.getvalue().strip()
        self.assertIn('Option for Accommodation can only be either Y/y or N/n', print_output)
        self.assertEqual(len(self.amity_instance.fellows), 0)

    def test_add_person_no_office_available(self):
        '''Tests adding person when no office is available'''

        self.reset()
        self.amity_instance.office_block = [] # reset available offices to zero
        with screen_output() as (terminal_output, err):
            self.amity_instance.add_person(['Daniel', 'Kitui'], 'fellow', 'N')
        print_output = terminal_output.getvalue().strip()
        self.assertIn('No Offices currently available for allocation', print_output)

    def test_add_person_fellow_all_options(self):
        '''Tests adding person when no livingspace is available'''

        self.reset()
        with screen_output() as (terminal_output, err):
            self.amity_instance.add_person(['Daniel', 'Kitui'], 'fellow', 'Y')
            print_output = terminal_output.getvalue().strip()

        self.assertIn('No Livingroom currently available for allocation', print_output)

        self.amity_instance.create_room(['Kenya'], 'livingspace')
        with screen_output() as (terminal_output, err):
            self.amity_instance.add_person(['Daniella', 'Mwangi'], 'fellow', 'y')

        print_output = terminal_output.getvalue().strip()
        self.assertIn('Daniella has been allocated the livingspace Kenya', print_output)

    def test_print_room_empty(self):
        '''Tests printing an empty room'''

        self.reset()
        self.amity_instance.create_room(['NewlyMadeRoom'], 'office')
        with screen_output() as (terminal_output, err):
            self.amity_instance.print_room('NewlyMadeRoom')
        print_output = terminal_output.getvalue().strip()
        self.assertIn('Room is empty', print_output)

    def test_print_room_non_existent_room(self):
        '''Tests printing a room that does not exist yet'''

        self.reset()
        with screen_output() as (terminal_output, err):
            self.amity_instance.print_room('Does_not_exist')
        print_output = terminal_output.getvalue().strip()
        self.assertIn('Room Does_not_exist does not exist', print_output)

    def test_print_unallocated_no_one_unallocated(self):
        '''Tests the print_unallocated_functionality'''

        self.reset()
        # Test print_unallocated when none is present
        with screen_output() as (terminal_output, err):
            self.amity_instance.print_unallocated(None) # No output file specified.
        print_output = terminal_output.getvalue().strip()
        self.assertIn('There are currently no unallocated people', print_output)

    def test_print_unallocated_when_one_is_present(self):
        '''Test print_unallocated when one is present'''

        self.reset()
        # Add person
        with screen_output() as (terminal_output, err):
            self.amity_instance.add_person(['Daniel', 'Kitui'], 'fellow', 'Y')

        # Run print_unallocated
        with screen_output() as (terminal_output, err):
            self.amity_instance.print_unallocated(None)
        print_output = terminal_output.getvalue().strip()
        self.assertIn('Daniel Kitui', print_output)

    def test_print_unallocated_with_file_output_specified(self):
        '''Test print_unallocated with output file specified'''

        # Add person
        self.amity_instance.add_person(['Daniel', 'Kitui'], 'fellow', 'Y')
        with screen_output() as (terminal_output, err):
            self.amity_instance.print_unallocated('Unallocated_People.txt')
        print_output = terminal_output.getvalue().strip()
        self.assertIn('List of the unallocated saved to Unallocated_People.txt', print_output)
        self.assertTrue(os.path.isfile('Unallocated_People.txt')) # Confirm file exists in current directory
        self.reset()
        os.unlink('Unallocated_People.txt') # Finally delete the 'Unallocated_People.txt' to clean up the test environment

    def test_print_unallocated_wrong_output_file_format(self):
        '''print_unallocated with invalid output file format'''

        self.reset()
        with screen_output() as (terminal_output, err):
            self.amity_instance.add_person(['Daniel', 'Kitui'], 'fellow', 'Y')

        with screen_output() as (terminal_output, err):
            self.amity_instance.print_unallocated('Unallocated_People.pdf')

        print_output = terminal_output.getvalue().strip()
        self.assertIn('Invalid output file format', print_output)
        self.assertFalse(os.path.isfile('Unallocated_People.pdf')) # Confirm specified file has not been created

    def test_load_people_file_format(self):
        '''Test for the file input format'''
        self.reset()

        with screen_output() as (terminal_output, err):
            self.amity_instance.load_people('input_file.pdf') # Incorrect file name

        print_output = terminal_output.getvalue().strip()
        self.assertIn('Invalid input file name', print_output)

        with screen_output() as (terminal_output, err):
            self.amity_instance.load_people('file_does_not_exist.txt')  # Incorrect file name

        print_output = terminal_output.getvalue().strip()
        self.assertIn('The specified file does not exist', print_output)

    def test_load_people(self):
        self.reset()

        self.amity_instance.load_people('input.txt')

        self.assertEqual(len(self.amity_instance.un_allocated_persons['staff']), 3)

    def test_print_allocation_output_filename(self):
        '''Test for the print_allocation functionality'''

        self.reset()

        self.amity_instance.create_room(['Bungoma'], 'office') # Create new office
        self.amity_instance.add_person(['Daniel','Kitui'], 'staff', None) # Staff will be allocated to the available Bungoma office
        self.amity_instance.create_room(['kitale'], 'office') # Create new office, for relocation testing
        self.amity_instance.add_person(['Daniel', 'Kitui'], 'staff', None)
        self.amity_instance.print_allocations('output.txt')

        self.assertTrue('output.txt')

        with screen_output() as (terminal_output, err):
            self.amity_instance.print_allocations('output.pdf')

        print_output = terminal_output.getvalue().strip()
        self.assertIn('The output file specified is not a valid text file. Data will not be saved', print_output)




    def test_reallocate_person(self):
        '''Test reallocate_person functionality'''

        self.reset()
        self.amity_instance.create_room(['Bungoma'], 'office')  # Create new office
        self.amity_instance.add_person(['Daniel','Kitui'], 'staff', None) # Staff will be allocated to the available Bungoma office
        self.amity_instance.add_person(['Jackson','Wafula'], 'fellow', 'y') # Staff will be allocated to the available Bungoma office

        self.amity_instance.create_room(['kitale'], 'office')   # Create new office, for relocation testing

        self.amity_instance.create_room(['kenya'], 'livingspace')
        assert len(self.amity_instance.office_block) == 2

        with screen_output() as (terminal_output, err):
            self.amity_instance.reallocate_person('AND/S/001', 'kitale')

        print_output = terminal_output.getvalue().strip()

        self.assertIn('Daniel has been re-allocated to room kitale', print_output)

        with screen_output() as (terminal_output, err):
            self.amity_instance.reallocate_person('AND/F/002', 'kenya')  # Reallocate fellow
        print_output = terminal_output.getvalue().strip()
        self.assertIn('Jackson has been re-allocated to room kenya', print_output)

        with screen_output() as (terminal_output, err):
            self.amity_instance.reallocate_person('AND/S/001', 'Morroco')  # Reallocate to room that does not exist
        print_output = terminal_output.getvalue().strip()

        self.assertIn('Room Morroco does not exist', print_output)

        with screen_output() as (terminal_output, err):
            self.amity_instance.reallocate_person('AND/S/009', 'Morroco')  # Person does not exist
        print_output = terminal_output.getvalue().strip()

        self.assertIn('Employee AND/S/009 does not exist', print_output)



    def test_reallocate_person_same_room_they_already_occupy(self):
        '''Test reallocate_person to a non-existent room'''

        self.reset()
        self.amity_instance.create_room(['Bungoma'], 'office') # Create new office
        self.amity_instance.add_person(['Daniel','Kitui'], 'staff', None) # Staff will be allocated to the available Bungoma office

        with screen_output() as (terminal_output, err):
            self.amity_instance.reallocate_person('AND/S/001', 'Bungoma') # Relocate to same office currently occupied

        print_output = terminal_output.getvalue().strip()
        self.assertIn('You cannot relocate a person to a room they are currently occupying.', print_output)

    def test_reallocate_person_to_non_existent_room(self):
        '''Test reallocate_person to a room that doesnt currently exist'''

        self.reset()
        self.amity_instance.create_room(['Bungoma'], 'office') # Create new office
        self.amity_instance.add_person(['Daniel','Kitui'], 'staff', None) # Staff will be allocated to the available Bungoma office

        with screen_output() as (terminal_output, err):
            self.amity_instance.reallocate_person('AND/S/001', 'Mombasa')  # Relocate to an office that currently doesnt exist.

        print_output = terminal_output.getvalue().strip()
        self.assertIn('Room Mombasa does not exist.', print_output)

    def test_load_state_db_does_not_exist(self):
        '''Test load_state functionality'''
        self.reset()
        with screen_output() as (terminal_output, err):
            self.amity_instance.load_state('db_doesnt_exist.db')

        print_output = terminal_output.getvalue().strip()
        self.assertIn('The specified database does not exist.', print_output, )

    def test_load_state_invalid_database(self):
        '''Test load_state for invalid name'''

        self.reset()

        fake_db = open('not_db.txt', 'w+')
        fake_db.close()

        with screen_output() as (terminal_output, err):
            self.amity_instance.load_state('not_db.txt') # Load a wrong format file

        print_output = terminal_output.getvalue().strip()
        self.assertIn('The specified file is not a valid database file.', print_output)

        os.unlink('not_db.txt')

        self.reset()

        with screen_output() as (terminal_output, err):
            self.amity_instance.load_state('db_does_not_exist.db') # Load a db that doesnt exist

        print_output = terminal_output.getvalue().strip()
        self.assertIn('The specified database does not exist.', print_output)


    def test_save_state_database_name(self):
        '''Test save state functionalities- naming of database'''
        self.reset()
        with screen_output() as (terminal_output, err):
            self.amity_instance.save_state('amity_data')  # wrong database name

        print_output = terminal_output.getvalue().strip()
        self.assertIn('Invalid database name. Make sure the name ends with ".db".', print_output)



    def test_save_state_specified_db_name(self):
        '''Test that save_state method with a specified name'''

        self.reset()

        self.amity_instance.create_room(['Bungoma'], 'office') # Create new office
        self.amity_instance.add_person(['Daniel','Kitui'], 'staff', None) # Staff will be allocated to the available Bungoma office

        with screen_output() as (terminal_output, err):
            self.amity_instance.save_state('test_amity.db')     #

        print_output = terminal_output.getvalue().strip()
        self.assertIn('Program data successfully saved to data/test_amity.db!', print_output)

        self.assertTrue('data/test_amity.db!')      # Assert db exists.

        # Save state functionality

        self.reset()  # reset to simulate restarted program state

        self.amity_instance.load_state('test_data.db')

        assert len(self.amity_instance.office_block) == 0
        assert len(self.amity_instance.staff_members) == 0

    def test_save_state_all_data_present(self):
        '''Test save_state'''

        self.reset()
        self.amity_instance.add_person(['Daniels', 'Masake'], 'fellow', 'Y')  # will create an unallocated fellow
        self.amity_instance.add_person(['Daniel','Kitui'], 'staff', None) # Will create an unallocated staff
        self.amity_instance.create_room(['Bungoma'], 'office') # Create new office
        self.amity_instance.add_person(['Daniel','Kitui'], 'staff', None) # Staff will be allocated to the available Bungoma office
        self.amity_instance.add_person(['Daniel', 'Kitui'], 'fellow', 'Y')
        self.amity_instance.create_room(['kenya'], 'livingspace')

        with screen_output() as (terminal_output, err):
            self.amity_instance.save_state('trial_data.db')

        print_output = terminal_output.getvalue().strip()
        self.assertIn('Program data successfully saved to data/trial_data.db!', print_output)

        self.assertTrue('data/trial_data.db') # test file exists






    def test_remove_person(self):
        '''Tests remove_person functionality'''

        self.reset()

        self.amity_instance.add_person(['Albert', 'Einstein'], 'fellow', 'y')

        self.amity_instance.create_room(['Bungoma'], 'office') # Create new office
        self.amity_instance.add_person(['Daniel','Kitui'], 'staff', None)
        self.amity_instance.add_person(['Daniel', 'Kitui'], 'fellow', 'Y')

        assert len(self.amity_instance.staff_members) == 1
        assert len(self.amity_instance.fellows) == 2

        self.amity_instance.remove_person('AND/S/002')
        self.amity_instance.remove_person('AND/F/003')

        assert len(self.amity_instance.staff_members) == 0
        assert len(self.amity_instance.fellows) == 1  # One fellow removed.

        with screen_output() as (terminal_output, err):
            self.amity_instance.remove_person('AND/F/001')

        print_output = terminal_output.getvalue().strip()

        self.assertIn('Fellow Albert Einstein has been removed from Fellows list.', print_output)
        self.assertIn('Employee No: AND/F/001 Has been removed from the records', print_output)


    def test_delete_room(self):
        '''Tests thhe delete_room functionality'''

        self.reset()

        self.amity_instance.create_room(['Bungoma'], 'office') # Create new office
        self.amity_instance.add_person(['Daniel','Kitui'], 'staff', None)  # Person added to room Bungoma
        self.amity_instance.add_person(['Daniel', 'Kitui'], 'fellow', 'Y')

        self.amity_instance.delete_room('Bungoma')

        assert len(self.amity_instance.office_block) == 0

        assert len(self.amity_instance.un_allocated_persons['staff']) == 1  # unallocated list has one more person
        assert len(self.amity_instance.un_allocated_persons['fellows_office']) == 1     # Unallocated list has one person.

