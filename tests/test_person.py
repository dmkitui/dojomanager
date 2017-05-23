#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Test cases for the commandline program 'create_room.py'
'''

import unittest
import sys
from os import path
from io import StringIO
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from models.person import Person, Staff, Fellow
from contextlib import contextmanager


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


class TestAddPerson(unittest.TestCase):
    ''' Class to test the person model'''
    def setUp(self):
        '''Setup the Staff and Fellow instances'''
        self.staff_instance = Staff()
        self.fellow_instance = Fellow()

    def test_add_staff_successfully(self):
        '''Test add staff'''
        with screen_output() as (terminal_output, err):
            daniel = self.staff_instance.add_person(3, ['Daniel', 'Kitui'])

        print_output = terminal_output.getvalue().strip()
        self.assertEqual(print_output, 'Staff Daniel Kitui has been successfully added.')
        self.assertIsInstance(daniel, Staff, 'Formed object not of the required class')
        self.assertEqual(daniel.person_id, 3)

    def test_add_fellow_with_accommodation_flag(self):
        '''Test add fellow with accommodation argument'''
        with screen_output() as (terminal_output, err):
            daniel = self.fellow_instance.add_person(['Daniel', 'Kitui'], 'Y', 56)

        print_output = terminal_output.getvalue().strip()
        self.assertEqual(print_output, 'Fellow Daniel Kitui has been successfully added.')
        self.assertIsInstance(daniel, Fellow, 'Formed object no of the required class')
        self.assertEqual(daniel.person_id, 56)

    def test_add_fellow_without_accommodation_flag(self):
        '''Test add fellow without accommodation flag'''
        with screen_output() as (terminal_output, err):
            daniel = self.fellow_instance.add_person(['Daniel', 'Kitui'], None, 56)

        print_output = terminal_output.getvalue().strip()
        self.assertEqual(print_output, 'Fellow Daniel Kitui has been successfully added.\n\nDaniel does not wish to be accommodated')

# if __name__ == '__main__':
#     unittest.main()
