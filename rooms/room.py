class Room(object):

    '''
    base class Room to instantiate and hold attributes for the facilities at the dojo
    '''
    # room_name = ''

    def __init__(self, room_name='', room_type=''):
        self.room_name = room_name
        self.room_type = room_type
        all_rooms = []


    def create_room(self, room_name, room_type):
        self.room_name = room_name
        self.room_type = room_type
        print('Making Room Now')
        self.all_rooms.append(self)

        return self

class Office(Room):

    '''
    Subclass of Room to model offices
    with attributes room_name and room_type
    '''
    def __init__(self, room_name='', room_type=''):
        self.room_name = room_name
        self.room_type = room_type

    def create_room(self, room_name, room_type):
        self.room_name = room_name
        self.room_type = room_type
        return self


class LivingSpace(Room):
    '''
    Subclass of Room to model living spaces with attributes room_name and
    room_type
    '''

    def __init__(self, room_name='', room_type=''):
        self.room_name = room_name
        self.room_type = room_type
        self.occupants = []


    def create_room(self, room_name, room_type):

        self.room_name = room_name
        self.room_type = room_type

        return self
    #
    # def add_occupant(self, person):
    #     self.occupants.append(person)