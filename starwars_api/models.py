from starwars_api.client import SWAPIClient
from starwars_api.exceptions import SWAPIClientError

api_client = SWAPIClient()

class BaseModel(object):

    def __init__(self, json_data):
        """
        Dynamically assign all attributes in `json_data` as instance
        attributes of the Model.
        """
        self.json_data = json_data

    @classmethod
    def get(cls, resource_id):
        """
        Returns an object of current Model requesting data to SWAPI using
        the api_client.
        """
        return cls(resources[cls.RESOURCE_NAME](resource_id))

    @classmethod
    def all(cls):
        """
        Returns an iterable QuerySet of current Model. The QuerySet will be
        later in charge of performing requests to SWAPI for each of the
        pages while looping.
        """
        return inquirers[cls.RESOURCE_NAME]()
    
    def __getattr__(self,field):
        return self.json_data[field]


class People(BaseModel):
    """Representing a single person"""
    RESOURCE_NAME = 'people'

    def __init__(self, json_data):
        super(People, self).__init__(json_data)

    def __repr__(self):
        return 'Person: {0}'.format(self.name)


class Films(BaseModel):
    RESOURCE_NAME = 'films'

    def __init__(self, json_data):
        super(Films, self).__init__(json_data)

    def __repr__(self):
        return 'Film: {0}'.format(self.title)


class BaseQuerySet(object):

    def __init__(self):
        self.json_data = resources[self.RESOURCE_NAME]()
        
    def count(self):
        return self.json_data['count']

    def __iter__(self):
        p = 1
        current = self.json_data
        for res in current['results']:
            yield self.constructor(res)
        while current['next']:
            p += 1
            current = resources[self.RESOURCE_NAME](page = p)
            for res in current['results']:
                yield self.constructor(res)

class PeopleQuerySet(BaseQuerySet):
    RESOURCE_NAME = 'people'
    constructor = People

    def __init__(self):
        super(PeopleQuerySet, self).__init__()

    def __repr__(self):
        return 'PeopleQuerySet: {0} objects'.format(str(len(self.objects)))


class FilmsQuerySet(BaseQuerySet):
    RESOURCE_NAME = 'films'
    constructor = Films

    def __init__(self):
        super(FilmsQuerySet, self).__init__()

    def __repr__(self):
        return 'FilmsQuerySet: {0} objects'.format(str(len(self.objects)))

resources = {'people':api_client.get_people, 'films':api_client.get_films}
inquirers = {'people':PeopleQuerySet, 'films':FilmsQuerySet}