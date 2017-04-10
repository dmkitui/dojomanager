'''
Test cases for the commandline program 'create_room.py'
'''

import unittest
from dojo_manager import Person, Fellow, Staff, Dojo, Room, Office, \
    LivingSpace

class TestCreateRoom(unittest.TestCase):
    '''

    '''
    def test_create_room_successfully(self):
        my_class_instance = Room()
        initial_room_count = len(my_class_instance.all_rooms)
        blue_office = my_class_instance.create_room('blue', 'office')
        self.assertTrue(blue_office)
        new_room_count = len(my_class_instance.all_rooms)
        self.assertEqual(new_room_count - initial_room_count, 1)

    def test_create_office(self):
        my_class = Office()
        rhino_office = my_class.create_room('Rhino', 'Office')
        self.assertIsInstance(rhino_office, Room, 'Formed Object not of the '
                                                  'right class')

    def test_create_living_space(self):
        my_class = LivingSpace()
        comfy_livingspace = my_class.create_room('Comfy', 'livingspace')
        self.assertIsInstance(comfy_livingspace, Room, 'Formed Object not of the '
                                                  'right class')

    def test_create_staff_successfully(self):
        my_class_instance = Staff()
        daniel = my_class_instance.add_person('Daniel Kitui')
        self.assertIsInstance(daniel, Staff, 'Formed object no of the '
                                             'required class')

    def test_create_fellow_successfully(self):
        my_class_instance = Fellow()
        daniel = my_class_instance.add_person('Daniel Kitui', 'Y')
        self.assertIsInstance(daniel, Fellow, 'Formed object not of the '
                                             'required class')

    def test_adding_fellow_successfully(self):
        my_class_instance = Fellow()
        daniel = my_class_instance.add_person(['Daniel', 'Kitui'], 'Y')
        self.assertTrue(daniel)
        self.assertEqual(daniel.fellow_name, ['Daniel', 'Kitui'])


if __name__ == '__main__':
    unittest.main()
