#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
import sys
from os import path
from io import StringIO
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from models.person import Person, Staff, Fellow


class TestAddPerson(unittest.TestCase):
    ''' Class to test the person model'''
    def setUp(self):
        '''Setup the Staff and Fellow instances'''
        self.staff_instance = Staff()
        self.fellow_instance = Fellow()

    def test_add_staff_successfully(self):
        '''Test add staff'''
        daniel = self.staff_instance.add_person(['Daniel', 'Kitui'], 3)
        self.assertIsInstance(daniel, Staff)
        self.assertEqual(daniel.person_id, 3)

    def test_add_fellow_with_accommodation_flag(self):
        '''Test add fellow with accommodation argument'''
        daniel = self.fellow_instance.add_person(['Daniel', 'Kitui'], 'Y', 56)
        self.assertIsInstance(daniel, Fellow)
        self.assertEqual(daniel.person_id, 56)

# if __name__ == '__main__':
#     unittest.main()
