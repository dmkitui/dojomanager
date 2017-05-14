#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Test cases for the amity_manager.py module
'''

import unittest
# from io import StringIO
from io import StringIO
import sys
from os import path
from contextlib import contextmanager
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from amity.amity import AmityManager
from models.room import Office, LivingSpace

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
    # def setUp(self):
    #     amity_instance = AmityManager()

    def test_00_initial_state(self):
        amity_instance = AmityManager()
        self.assertEqual([amity_instance.office_block, amity_instance.fellows, amity_instance.staff_members], [[], [], []])

    def test_01_create_office(self):
        amity_instance = AmityManager()
        with screen_output() as (terminal_output, err):
            green_office = amity_instance.create_room(['Green'], 'Office')
        print_output = terminal_output.getvalue().strip()
        self.assertEquals(print_output, 'An Office called Green has been successfully created!')
        self.assertEqual(len(amity_instance.office_block), 1, 'Office not added')

    def test_02_create_livingspace(self):
        amity_instance = AmityManager()
        amity_instance.create_room(['Kenya'], 'Livingspace')
        self.assertEqual(len(amity_instance.living_spaces), 1, 'Livingspace not added')

    def test_03_create_multiple_offices(self):
        amity_instance = AmityManager()
        amity_instance.create_room(['Green', 'White', 'Blue'], 'Office')
        self.assertEqual(len(amity_instance.office_block), 3, 'Multiple rooms not created')

    def test_04_create_multiple_livingspace(self):
        amity_instance = AmityManager()
        amity_instance.create_room(['Kenya', 'Uganda', 'Tz', 'Rwanda'], 'Livingspace')
        self.assertEqual(len(amity_instance.living_spaces), 4, 'Multiple rooms not created')

    def test_05_create_already_existing_office(self):
        amity_instance = AmityManager()
        with screen_output() as (terminal_output, err):
            amity_instance.create_room(['Violet'], 'Office')
        print_output = terminal_output.getvalue().strip()
        self.assertEquals(print_output, 'An Office called Violet has been successfully created!')

        # Create second room with the same name
        with screen_output() as (terminal_output, err):
            amity_instance.create_room(['Violet'], 'Office')
            print_output = terminal_output.getvalue().strip()
        self.assertEqual(print_output, 'A room called Violet already exists')

    def test_06_add_person_no_rooms_available(self):
        amity_instance = AmityManager()
        amity_instance.office_block = []
        amity_instance.living_spaces = []
        with screen_output() as (terminal_output, err):
            dan = amity_instance.add_person(['Daniel', 'Kitui'], 'Staff', None)
        print_output = terminal_output.getvalue().strip()
        # self.assertEquals(print_output,
        self.assertEqual(len(amity_instance.staff_members), 1)
        self.assertEqual(len(amity_instance.un_allocated_persons), 1)

    def test_07_add_person_no_staff_with_wants_accommodation(self):
        amity_instance = AmityManager()
        with screen_output() as (terminal_output, err):
            dan = amity_instance.add_person(['Daniel', 'Kitui'], 'Staff', 'Y')
        print_output = terminal_output.getvalue().strip()
        self.assertEquals(print_output, 'Staff are not entitled to accommodation')
        self.assertEqual(len(amity_instance.staff_members), 1)

    def test_08_add_person_no_staff_with_wrong_wants_accommodation_argument(self):
        amity_instance = AmityManager()
        with screen_output() as (terminal_output, err):
            dan = amity_instance.add_person(['Daniel', 'Kitui'], 'Fellow', 'No')
        print_output = terminal_output.getvalue().strip()
        self.assertEquals(print_output, 'Argument for Accommodation can only be either Y/y or N/n')
        self.assertEqual(len(amity_instance.fellows), 0)

    def test_allocate_office_when_none_is_available(self):
        amity_instance = AmityManager()
        amity_instance.office_block = []
        amity_instance.add_person(['Daniel', 'Kitui'], 'Fellow', 'N')
        with screen_output() as (terminal_output, err):
            amity_instance.allocate_office(amity_instance.fellows[0])
        print_output = terminal_output.getvalue().strip()
        self.assertEquals(print_output, 'No Offices currently available for allocation')

    def test_allocate_livingspace_when_none_is_available(self):
        amity_instance = AmityManager()
        amity_instance.living_spaces = []
        amity_instance.add_person(['Daniel', 'Kitui'], 'Fellow', 'Y')
        with screen_output() as (terminal_output, err):
            amity_instance.allocate_livingspace(amity_instance.fellows[0])
        print_output = terminal_output.getvalue().strip()
        self.assertEquals(print_output, 'No Livingroom currently available for allocation')

    def test_print_room_empty(self):
        amity_instance = AmityManager()
        amity_instance.create_room(['Newly_Made_Room'], 'Office')
        with screen_output() as (terminal_output, err):
            amity_instance.print_room('Newly_Made_Room')
        print_output = terminal_output.getvalue().strip()
        self.assertEqual(print_output, 'Occupants of room Newly_Made_Room : Room Newly_Made_Room is empty')

    def test_print_room_non_existent_room(self):
        amity_instance = AmityManager()
        with screen_output() as (terminal_output, err):
            amity_instance.print_room('Does_not_exist')
        print_output = terminal_output.getvalue().strip()
        self.assertEqual(print_output, 'Room Does_not_exist Seems not to exist. Kindly Confirm room name')
    #
    # # Task 2 tests
    #
    # def test_valid_output_file_for_allocations(self):
    #     self.assertEqual(self.instance.print_allocations(self.user_inputs3), 'The output file not a valid text file\n')
    #
    #
    # def test_valid_output_file_for_print_unallocated(self):
    #     self.instance.un_allocated = ['daniel kitui', 'Dan M']
    #     self.assertEqual(self.instance.print_unallocated(self.user_inputs3),
    #                      'Invalid file format')

if __name__ == '__main__':
    # unittest.main()
    assert not hasattr(sys.stdout, "getvalue")
    unittest.main(module=__name__, buffer=False, exit=False)