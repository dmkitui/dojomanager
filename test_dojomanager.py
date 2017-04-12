'''
Test cases for the dojo_manager.py module
'''

import unittest
from personel.person import Person, Staff, Fellow
from rooms.room import Office, LivingSpace, Room
from dojo_manager import DojoManager


class TestCreateRoom(unittest.TestCase):
    '''Test cases to test the functionality of the dojo_manager module
    '''

    def test_initial_state(self):
        self.instance = DojoManager()
        self.assertEqual([self.instance.office_block,
                             self.instance.fellows,
                             self.instance.staff_members],
                             [[],[],[]])

    def test_add_office(self):
        self.instance = DojoManager()
        self.instance.add_office('Kahawa')
        self.assertEqual(len(self.instance.office_block), 1, 'Office not '
                                                             'added')

    # Task 1 Tests

    def test_print_room_non_existent_room(self):
        self.instance = DojoManager()
        room_name = 'White'
        self.assertEqual(self.instance.do_print_room(room_name), 'Room {} '
                                                               'Seems not to exist. Kindly Confirm room name'.format(room_name))


if __name__ == '__main__':
    unittest.main()
