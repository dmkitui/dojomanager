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
from models.person import Fellow, Staff
from models.room import LivingSpace, Office

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

class TestDatabaseFunctionality(unittest.TestCase):
    '''Test cases for the various database functionality'''

    def setUp(self):
        self.amity_instance = AmityManager()

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

    def test_a_save_state_invalid_database_name(self):
        '''Test save state functionality- naming of database'''
        self.reset()
        with screen_output() as (terminal_output, err):
            self.amity_instance.save_state('amity_data')  # wrong database name

        print_output = terminal_output.getvalue().strip()
        self.assertIn('Invalid database name. Make sure the name ends with ".db".', print_output)

    def test_b_save_state_specified_db_name(self):
        '''Test that save_state method with a specified name'''

        self.amity_instance.create_room(['Bungoma'], 'office') # Create new office
        self.amity_instance.add_person(['Daniel','Kitui'], 'staff', None) # Staff will be allocated to the available Bungoma office

        with screen_output() as (terminal_output, err):
            self.amity_instance.save_state('test_amity.db')     # Vslid database name

        print_output = terminal_output.getvalue().strip()
        self.assertIn('Program data successfully saved to data/test_amity.db!', print_output)

        self.assertTrue('data/test_amity.db!')      # Assert db exists.

    def test_c_load_state_defined_name(self):
        '''Test the load_state for a defined and existing database.'''

        # Load the databse created.

        self.amity_instance.load_state('test_amity.db')

        assert len(self.amity_instance.office_block) == 1
        assert len(self.amity_instance.staff_members) == 1

    def test_d_save_state_all_data_present(self):
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

        # Load the databse created.

        self.amity_instance.load_state('trial_data.db')

        assert len(self.amity_instance.office_block) == 1
        assert len(self.amity_instance.staff_members) == 2
        assert len(self.amity_instance.un_allocated_persons['fellows_office']) == 1
        assert len(self.amity_instance.un_allocated_persons['staff']) == 1
        assert len(self.amity_instance.living_spaces) == 1
        assert self.amity_instance.personnel_id == 4

    def test_e_load_state_invalid_database(self):
        '''Test load_state for invalid name'''

        fake_db = open('not_db.txt', 'w+')
        fake_db.close()

        with screen_output() as (terminal_output, err):
            self.amity_instance.load_state('not_db.txt')  # Load a wrong format file

        print_output = terminal_output.getvalue().strip()
        self.assertIn('The specified file is not a valid database file.', print_output)

        os.unlink('not_db.txt')

        self.reset()

        with screen_output() as (terminal_output, err):
            self.amity_instance.load_state('db_does_not_exist.db')  # Load a db that doesnt exist

        print_output = terminal_output.getvalue().strip()
        self.assertIn('The specified database does not exist.', print_output)

