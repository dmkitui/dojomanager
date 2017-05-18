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
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


class TestAmityModule(unittest.TestCase):
    '''Test cases to test the functionality of the amity_manager module
    '''
    def setUp(self):
        '''Setup the test instance'''
        self.amity_instance = AmityManager()

    def test_00_initial_state(self):
        '''Test initial states of the various lists'''
        self.assertEqual([self.amity_instance.office_block, self.amity_instance.fellows, self.amity_instance.staff_members], [[], [], []])

    def test_01_add_abbreviated_invalid_person_name(self):
        '''Test adding a person with name abbreviations'''
        with screen_output() as (terminal_output, err):
            self.amity_instance.add_person(['D', 'K'], 'Fellow', 'Y')
        print_output = terminal_output.getvalue().strip()
        self.assertEquals(print_output, 'Invalid Person Name.')

    def test_02_create_office(self):
        '''Test successful creation of office.'''
        with screen_output() as (terminal_output, err):
            green_office = self.amity_instance.create_room(['Green'], 'Office')
        print_output = terminal_output.getvalue().strip()
        self.assertEquals(print_output, 'An Office called Green has been successfully created!')
        self.assertEqual(len(self.amity_instance.office_block), 1, 'Office not added')

    def test_03_create_livingspace(self):
        '''Test creating livingspace'''
        self.amity_instance.create_room(['Kenya'], 'Livingspace')
        self.assertEqual(len(self.amity_instance.living_spaces), 1, 'Livingspace not added')

    def test_04_create_multiple_offices(self):
        '''Test creating multiple offices'''
        self.amity_instance.create_room(['Green', 'White', 'Blue'], 'Office')
        self.assertEqual(len(self.amity_instance.office_block), 3, 'Multiple rooms not created')

    def test_05_create_multiple_livingspace(self):
        '''Test creating multiple living spaces'''
        self.amity_instance.create_room(['Kenya', 'Uganda', 'Tz', 'Rwanda'], 'Livingspace')
        self.assertEqual(len(self.amity_instance.living_spaces), 4, 'Multiple rooms not created')

    def test_06_create_already_existing_office(self):
        '''Test creating an already existing room'''
        with screen_output() as (terminal_output, err):
            self.amity_instance.create_room(['Violet'], 'Office')
        print_output = terminal_output.getvalue().strip()
        self.assertEquals(print_output, 'An Office called Violet has been successfully created!')

        # Create second room with the same name
        with screen_output() as (terminal_output, err):
            self.amity_instance.create_room(['Violet'], 'Office')
        print_output = terminal_output.getvalue().strip()
        self.assertEqual(print_output, 'A room called Violet already exists')

    def test_07_invalid_room_names(self):
        with screen_output() as (terminal_output, err):
            self.amity_instance.create_room(['#Dojo'], 'Office')

        print_output = terminal_output.getvalue().strip()
        self.assertEqual(print_output, '#Dojo is not a valid room name. Room not created')

    def test_08_add_person_no_rooms_available(self):
        '''Test adding person when no room is available'''
        self.amity_instance.office_block = []
        self.amity_instance.living_spaces = []
        with screen_output() as (terminal_output, err):
            dan = self.amity_instance.add_person(['Daniel', 'Kitui'], 'Staff', None)
        print_output = terminal_output.getvalue().strip()
        # self.assertEquals(print_output,
        self.assertEqual(len(self.amity_instance.staff_members), 1)
        self.assertEqual(len(self.amity_instance.un_allocated_persons), 1)

    def test_09_add_person_staff_with_wants_accommodation(self):
        '''Test adding staff with a argument for wants accommodation'''
        with screen_output() as (terminal_output, err):
            dan = self.amity_instance.add_person(['Daniel', 'Kitui'], 'Staff', 'Y')
        print_output = terminal_output.getvalue().strip()
        self.assertEquals(print_output, 'Staff are not entitled to accommodation')
        self.assertEqual(len(self.amity_instance.staff_members), 1)

    def test_10_add_person_with_wrong_wants_accommodation_argument(self):
        '''Tests adding a person with an invalid wants_accommodation argument'''
        with screen_output() as (terminal_output, err):
            dan = self.amity_instance.add_person(['Daniel', 'Kitui'], 'Fellow', 'No')
        print_output = terminal_output.getvalue().strip()
        self.assertEquals(print_output, 'Argument for Accommodation can only be either Y/y or N/n')
        self.assertEqual(len(self.amity_instance.fellows), 0)

    def test_11_allocate_office_when_none_is_available(self):
        '''Tests adding person when no office is available'''
        self.amity_instance.office_block = [] # reset available offices to zero
        self.amity_instance.add_person(['Daniel', 'Kitui'], 'Fellow', 'N')
        with screen_output() as (terminal_output, err):
            self.amity_instance.allocate_office(self.amity_instance.fellows[0])
        print_output = terminal_output.getvalue().strip()
        self.assertEquals(print_output, 'No Offices currently available for allocation')

    def test_12_allocate_livingspace_when_none_is_available(self):
        '''Tests adding person when no livingspace is available'''
        self.amity_instance.living_spaces = [] # reset available livingspaces to zero
        self.amity_instance.add_person(['Daniel', 'Kitui'], 'Fellow', 'Y')
        with screen_output() as (terminal_output, err):
            self.amity_instance.allocate_livingspace(self.amity_instance.fellows[0])
        print_output = terminal_output.getvalue().strip()
        self.assertEquals(print_output, 'No Livingroom currently available for allocation')

    def test_13_print_room_empty(self):
        '''Tests printing an empty room'''
        self.amity_instance.create_room(['Newly_Made_Room'], 'Office')
        with screen_output() as (terminal_output, err):
            self.amity_instance.print_room('Newly_Made_Room')
        print_output = terminal_output.getvalue().strip()
        self.assertEqual(print_output, 'Occupants of room Newly_Made_Room : Room Newly_Made_Room is empty')

    def test_14_print_room_non_existent_room(self):
        '''Tests printing a room that does not exist yet'''
        with screen_output() as (terminal_output, err):
            self.amity_instance.print_room('Does_not_exist')
        print_output = terminal_output.getvalue().strip()
        self.assertEqual(print_output, 'Room Does_not_exist Seems not to exist. Kindly Confirm room name')

    def test_15_print_unallocated(self):
        '''Tests the print_unallocated_functionality'''
        self.amity_instance.un_allocated_persons = [] # Reset list of unallocated people.
        # Test print_unallocated when none is present
        with screen_output() as (terminal_output, err):
            self.amity_instance.print_unallocated(None) # No output file specified.
        print_output = terminal_output.getvalue().strip()
        self.assertEqual(print_output, 'There are currently no unallocated people')

    def test_16_print_unallocated_when_one_is_present(self):
        '''Test print_unallocated when one is present'''
        self.amity_instance.fellows = []  # reset amity lists.
        self.amity_instance.office_block = []
        self.amity_instance.living_spaces = []
        self.amity_instance.staff_members = []
        self.amity_instance.un_allocated_persons = []
        # Add person
        with screen_output() as (terminal_output, err):
            self.amity_instance.add_person(['Daniel', 'Kitui'], 'Fellow', 'Y')

        # Run print_unallocated
        with screen_output() as (terminal_output, err):
            self.amity_instance.print_unallocated(None)
        print_output = terminal_output.getvalue().strip()
        self.assertEqual(print_output, 'Daniel Kitui')

    def test_17_print_unallocated_with_file_output_specified(self):
        '''Test print_unallocated with output file specified'''
        self.amity_instance.fellows = [] # reset amity lists.
        self.amity_instance.office_block = []
        self.amity_instance.living_spaces = []
        self.amity_instance.staff_members = []
        self.amity_instance.un_allocated_persons = []

        # Add person
        with screen_output() as (terminal_output, err):
            self.amity_instance.add_person(['Daniel', 'Kitui'], 'Fellow', 'Y')

        with screen_output() as (terminal_output, err):
            self.amity_instance.print_unallocated('Unallocated_People.txt')
        print_output = terminal_output.getvalue().strip()
        self.assertEqual(print_output, 'Daniel Kitui\nList of the unallocated saved to Unallocated_People.txt')
        self.assertTrue(os.path.isfile('Unallocated_People.txt')) # Confirm file exists in current directory

        # Test print_unallocated with wrong output file format
    def test_18_print_unallocated_wrong_output_file_format(self):
        '''print_unallocated with invalid output file format'''
        self.amity_instance.fellows = [] # reset amity lists.
        self.amity_instance.office_block = []
        self.amity_instance.living_spaces = []
        self.amity_instance.staff_members = []
        self.amity_instance.un_allocated_persons = [] # Reset list of unallocated people

        with screen_output() as (terminal_output, err):
            self.amity_instance.add_person(['Daniel', 'Kitui'], 'Fellow', 'Y')

        with screen_output() as (terminal_output, err):
            self.amity_instance.print_unallocated('Unallocated_People.pdf')
        print_output = terminal_output.getvalue().strip()
        self.assertEqual(print_output, 'Daniel Kitui\nInvalid output file format')
        self.assertFalse(os.path.isfile('Unallocated_People.pdf')) # Confirm specified file has not been created

    def test_19_load_people_file_format(self):
        '''Test for the file input format'''
        with screen_output() as (terminal_output, err):
            self.amity_instance.load_people('input_file.pdf') # Incorrect file name

        print_output = terminal_output.getvalue().strip()
        self.assertEqual(print_output, 'Invalid input file name')

        with screen_output() as (terminal_output, err):
            self.amity_instance.load_people('file_does_not_exist.txt')  # Incorrect file name

        print_output = terminal_output.getvalue().strip()
        self.assertEqual(print_output, 'The specified file does not exist')

    def test_20_reallocate_person(self):
        '''Test reallocate_person functionality'''
        self.amity_instance.fellows = [] # reset amity lists.
        self.amity_instance.office_block = []
        self.amity_instance.living_spaces = []
        self.amity_instance.staff_members = []
        self.amity_instance.personnel_id = 1 # Reset personel ids list

        self.amity_instance.create_room(['Bungoma'], 'Office') # Create new office
        self.amity_instance.add_person(['Daniel','Kitui'], 'Staff', None) # Staff will be allocated to the available Bungoma office

        self.amity_instance.create_room(['Kitale'], 'Office') # Create new office, for relocation testing
        with screen_output() as (terminal_output, err):
            self.amity_instance.reallocate_person(1, 'Kitale')

        print_output = terminal_output.getvalue().strip()
        self.assertEquals(print_output, 'Daniel has been re-allocated to room Kitale')

    def test_21_reallocate_person_same_room_they_already_occupy(self):
        '''Test reallocate_person to a non-existent room'''
        self.amity_instance.fellows = [] # reset amity lists.
        self.amity_instance.office_block = []
        self.amity_instance.living_spaces = []
        self.amity_instance.staff_members = []
        self.amity_instance.personnel_id = 1 # Reset personel ids list

        self.amity_instance.create_room(['Bungoma'], 'Office') # Create new office
        self.amity_instance.add_person(['Daniel','Kitui'], 'Staff', None) # Staff will be allocated to the available Bungoma office

        with screen_output() as (terminal_output, err):
            self.amity_instance.reallocate_person(1, 'Bungoma') # Relocate to same office currently occupied

        print_output = terminal_output.getvalue().strip()
        self.assertEquals(print_output, 'Cant relocate a person to a room he/she is currently occupying.')

    def test_22_reallocate_person_non_existent_room(self):
        '''Test reallocate_person to a room that doesnt currently exist'''
        self.amity_instance.fellows = [] # reset amity lists.
        self.amity_instance.office_block = []
        self.amity_instance.living_spaces = []
        self.amity_instance.staff_members = []
        self.amity_instance.personnel_id = 1 # Reset personel ids list

        self.amity_instance.create_room(['Bungoma'], 'Office') # Create new office
        self.amity_instance.add_person(['Daniel','Kitui'], 'Staff', None) # Staff will be allocated to the available Bungoma office

        with screen_output() as (terminal_output, err):
            self.amity_instance.reallocate_person(1, 'Mombasa') # Relocate to an office that currently doesnt exist.

        print_output = terminal_output.getvalue().strip()
        self.assertEquals(print_output, 'Room Mombasa Does Not Exist.')




if __name__ == '__main__':
    unittest.main()
