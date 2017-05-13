#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Test cases for the commandline program 'create_room.py'
'''

import unittest
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from models.person import Person, Staff, Fellow
from models.room import Office, LivingSpace, Room


class TestAddPerson(unittest.TestCase):

    def test_create_staff_successfully(self):
        my_class_instance = Staff()
        daniel = my_class_instance.add_person('Daniel Kitui')
        self.assertIsInstance(daniel, Staff, 'Formed object no of the '
                                             'required class')

    def test_adding_fellow_successfully(self):
        my_class_instance = Fellow()
        daniel = my_class_instance.add_person(['Daniel', 'Kitui'], 'Y')
        self.assertTrue(daniel)
        self.assertEqual(daniel.fellow_name, ['Daniel', 'Kitui'])
        self.assertIsInstance(daniel, Fellow, 'Formed object not of the '
                                             'required class')

    def test_wrong_argument(self):
        my_class = Staff()
        jeff = my_class.add_person(['Daniel', 'Kitui'])


class Test_add_person_to_a_room(unittest.TestCase):

    def test_add_to_existing_room(self):
        office_instance = Office()
        name = ['Steve', 'Man']
        new_office = office_instance.create_room('Kilimanjaro', 'Office')
        new_person = Staff().add_person(name)
        self.assertIsInstance(new_person, Staff, 'Incorrect instance')

if __name__ == '__main__':
    unittest.main()
