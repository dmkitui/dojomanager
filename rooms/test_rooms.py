import unittest
from rooms.room import Office, LivingSpace, Room
from dojo_manager import DojoManager


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
        self.assertEqual(comfy_livingspace.room_name, 'Comfy')

class Test_allocate_no_rooms(unittest.TestCase):
    def test_office_allocation(self):
        x = DojoManager()
        self.assertIsNone(x.allocate_office(['Daniel', 'Kitui']))

if __name__ == '__main__':
    unittest.main()
