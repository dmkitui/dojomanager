class Person(object):
    '''
    Base class to manage the people objects in the Dojo
    '''

    def __init__(self, name='', job_group='', accommodation=False):
        '''Initialize class'''
        self.person_name = name
        self.accommodation = accommodation

    def add_person(self, name, accommodation):
        '''
        Function to protoype the person object
        :param name: Person name in the form ['first_name', 'last_name']
        :param job_group: Person's job group. Either 'Fellow' or 'Staff'
        :param accommodation: Flag to indicate if a person wants accommodation. Either 'Y/y' or 'N/n'
        :return: created new person object
        '''
        self.person_name = name
        self.accommodation = accommodation
        return self


class Fellow(Person):
    '''
    Subclass Fellow to model Andela Fellows
    '''

    def __init__(self, fellow_name='', accommodation=False):
        '''Function to initialise the Fellow() class'''
        self.person_name = fellow_name
        self.accommodation = accommodation
        self.person_id = None # Personnel number

    def add_person(self, fellow_name, accommodation, id):
        '''
        Function to create a new person object of type Fellow, and add the object to the list of fellows
        :param fellow_name: list in the form ['first_name', 'second_name']
        :param accommodation: Flag for want_accommodation. Either 'Y/y' or 'N/n'
        :param id: Person_id that represent employee unique number.
        :return: the created person object.
        '''
        self.person_name = fellow_name
        self.accommodation = accommodation
        self.person_id= id
        print('Fellow {0} {1} has been successfully added.\n'.format(self.person_name[0], self.person_name[1]))
        if not accommodation:
            print('{0} does not wish to be accommodated\n'.format(fellow_name[0]))
        return self


class Staff(Person):
    '''
    subclass of Person to model staff members
    '''

    def __init__(self, staff_name=''):
        '''
        Function to initialize the Staff() class
        :param staff_name: 
        '''
        self.person_name = staff_name
        self.person_id = None  # Personnel number

    def add_person(self, id, staff_name=''):
        '''
        Function to create a new person of type staff object.
        :param id: Person_id that represent employee unique number
        :param staff_name: Name of staff member in the form ['first_name', 'Last_name']
        :return: The created new person object.
        '''
        self.person_name = staff_name
        self.person_id = id

        print('Staff {0} {1} has been successfully added.\n'.format(staff_name[0], staff_name[1]))
        return self
