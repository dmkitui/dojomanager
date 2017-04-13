#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Test cases for the commandline program 'create_room.py'
'''

import unittest
from person.person import Person, Staff, Fellow
from room.room import Office, LivingSpace, Room
from dojo_manager import DojoManager


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
        jeff = my_class.add_person({['Daniel', 'Kitui'], 'M'})


class Test_add_person_to_a_room(unittest.TestCase):
    def test_add_to_existing_room(self):
        office_instance = Office()
        new_office = office_instance.create_room('Kilimanjaro', 'Office')
        new_person = Staff().add_person(['Steve', 'Man'])
        name = ['Steve', 'Man']
        DojoManager.allocate_office(name)



if __name__ == '__main__':
    unittest.main()
