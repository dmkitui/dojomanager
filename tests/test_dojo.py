#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Test cases for the dojo_manager.py module
'''

import unittest
from person.person import Person, Staff, Fellow
from room.room import Office, LivingSpace, Room
from dojo.dojo import DojoManager


class TestCreateRoom(unittest.TestCase):
    '''Test cases to test the functionality of the dojo_manager module
    '''
    user_inputs = {'<person_name>': ['Daniel', 'Kitui'], '<room_name>': ['Kenya'], 'Office': True,
                   'Livingspace': False, '<wants_accommodation>': 'Y', 'Fellow': False, 'Staff':
                       True, '<room_name>': 'Kindaruma' }

    user_inputs2 = {'<person_name>': ['Daniel', 'Kitui'], '<room_name>': ['Kenya'], 'Office': True,
                   'Livingspace': False, '<wants_accommodation>': 'M', 'Fellow': False, 'Staff': True }

    instance = DojoManager()

    def test_initial_state(self):
        self.assertEqual([self.instance.office_block,
                             self.instance.fellows,
                             self.instance.staff_members],
                             [[],[],[]])

    def test_incorrect_arguments1(self):
        tom = self.instance.add_person(self.user_inputs)
        self.assertTrue(tom, 'Staff are not entitled to accommodation\n')

    def test_incorrect_arguments2(self):
        boss = self.instance.add_person(self.user_inputs)
        self.assertTrue(boss, 'Argument for Accomodation can only be either Y or N\n')

    def test_allocate_room_when_non_is_available(self):
        self.assertTrue(self.instance.allocate_livingroom(self.user_inputs['<person_name>']), 'Argument for Accomodation can only be either Y or N\n')


    def test_add_office(self):
        self.instance = DojoManager()
        self.instance.create_room(self.user_inputs)
        self.assertEqual(len(self.instance.office_block), 1, 'Office not added')

    # Task 1 Tests

    def test_print_room_non_existent_room(self):
        self.assertEqual(self.instance.print_room(self.user_inputs), 'Specified room Seems not to exist. Kindly Confirm room name\n')








if __name__ == '__main__':
    unittest.main()
