class Person(object):
    '''
    Base class to manage the people objects in the Dojo
    '''

    def __init__(self, name='', job_group='', accommodation=False):

        self.person_name = name
        self.accommodation = accommodation
        self.job_group = job_group

    def add_person(self, name, job_group, accommodation):
        self.person_name = name
        self.accommodation = accommodation
        return self


class Fellow(Person):
    '''
    Subclass Fellow to model Andela Fellows
    '''

    def __init__(self, fellow_name='', accomodation=False):
        # Person().__init__(fellow_name, accomodation)
        self.fellow_name = fellow_name
        self.accommodation = accomodation

    def add_person(self, fellow_name, accomodation):
        self.fellow_name = fellow_name
        self.accommodation = accomodation
        print('Fellow {0} {1} has been successfully added.'.format(
            self.fellow_name[0], self.fellow_name[1]))
        if not accomodation:
            print('{0} does not wish to be accomodated'.format(fellow_name[0]))

        return self


class Staff(Person):
    '''
    subclass of Person to model staff members
    '''

    def __init__(self, staff_name=''):
        self.person_name = staff_name

    def add_person(self, staff_name=''):
        self.person_name = staff_name
        print('Staff {0} {1} has been successfully added.'.format(
            staff_name[0], staff_name[1]))
        print(self.person_name)
        return self