import unittest
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from models.room import Office, LivingSpace, Room


class TestCreateRoom(unittest.TestCase):
    '''
    Class to run test cases for the rooms class
    '''
    def setUp(self):
        self.office_instance = Office()
        self.living_space_instance = LivingSpace()

    def test_create_office(self):
        green_office = self.office_instance.create_room('Green', 'Office')
        self.assertIsInstance(green_office, Office, 'Formed Object not of the right class')
        self.assertTrue(green_office.room_name, 'Green')
        self.assertEquals(green_office.occupants, [])
        self.assertEquals(green_office.room_type, 'Office')

    def test_create_living_space(self):
        comfy_livingspace = self.living_space_instance.create_room('Comfy', 'Livingspace')
        self.assertIsInstance(comfy_livingspace, Room, 'Formed Object not of the right class')
        self.assertEqual(comfy_livingspace.room_name, 'Comfy')
        self.assertEquals(comfy_livingspace.occupants, [])
        self.assertEquals(comfy_livingspace.room_type, 'Livingspace')

if __name__ == '__main__':
    unittest.main()
