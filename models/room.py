#!/usr/bin/python3
# -*- coding: utf-8 -*-


class Room(object):

    '''
    base class Room to instantiate and hold attributes for the facilities at the amity
    '''

    def __init__(self, room_name='', room_type=''):
        '''Initialize class Room'''
        self.room_name = room_name
        self.room_type = room_type
        self.occupants = []

    def create_room(self, room_name, room_type):
        '''
        Function to prototype a generic room
        :param room_name: String, name of the the room
        :param room_type: String, type of room, either 'Office' or 'Livingspace'
        :return: The created room objects.
        '''
        self.room_name = room_name
        self.room_type = room_type
        self.occupants = []
        return self


class Office(Room):

    '''
    Subclass of Room to model offices with attributes room_name and room_type
    '''
    def __init__(self, room_name='', room_type=''):
        '''Function to initialize the Office object'''
        self.room_name = room_name
        self.room_type = room_type
        self.occupants = []

    def create_room(self, room_name, room_type):
        '''
        Function to prototype a room object of type office
        :param room_name: string, name of the room to be created.
        :param room_type: Type of room, which is Office
        :return: room object.
        '''
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
        '''Function to initialize the LivingSpace class'''
        self.room_name = room_name
        self.room_type = room_type
        self.occupants = []

    def create_room(self, room_name, room_type):
        '''
        Function to protoype a room of livingspace class
        :param room_name: String, name of the room
        :param room_type: String, type of room
        :return: livingspace rooom object
        '''
        self.room_name = room_name
        self.room_type = room_type
        self.occupants = []
        return self
