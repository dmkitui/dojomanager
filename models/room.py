#!/usr/bin/python3
# -*- coding: utf-8 -*-


class Room(object):

    '''
    base class Room to instantiate and hold attributes for the facilities at the amity
    '''

    def __init__(self, room_name='', room_type=''):
        self.room_name = room_name
        self.room_type = room_type
        self.all_rooms = []
        self.occupants = []

    def create_room(self, room_name, room_type):
        self.room_name = room_name
        self.room_type = room_type
        self.all_rooms.append(self)
        self.occupants = []
        return self


class Office(Room):

    '''
    Subclass of Room to model offices with attributes room_name and room_type
    '''
    def __init__(self, room_name='', room_type=''):
        self.room_name = room_name
        self.room_type = room_type
        self.occupants = []

    def create_room(self, room_name, room_type):
        self.room_name = room_name
        self.room_type = room_type
        self.occupants = []
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
        self.occupants = []
        return self