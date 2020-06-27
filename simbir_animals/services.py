import uuid
from abc import ABC, abstractmethod

import requests

from simbir_animals import db
from simbir_animals.models import Cat, Dog, Fox
from simbir_animals.utils import DiskWorker, PillowEnhancer, MyError


class AnimalService(ABC):
    """
    Parent class for animals classes which contains all logic of work with image
    """

    def __init__(self, service_url=None, animal_type=None):
        """Initialising of basic parameters and local saving functionality"""

        self.service_url = service_url
        self.animal_type = animal_type
        self.disk_worker = DiskWorker()

    @abstractmethod
    def get_image_url(self, response):
        """Abstract method to define custom logic in each child class"""
        pass

    def call_to_service(self):
        """Function responsible for call to service which provides URL to random animal image.
        Function receives service URL and returns response object in json format"""

        response = requests.get(self.service_url)
        if response.status_code == 200:
            json_response = response.json()
        else:
            raise MyError("Service unavailable now. Please try again later")

        return json_response

    def generate_image_name(self, extension):
        """Function provides generation of random UUID4 name for image"""
        return str(uuid.uuid4()) + '.' + extension

    def create_entity_from_image_response(self, image_response):
        """Function handle the creating logic of image with custom animal type.
        It receives response object of image and
        returns corresponding child object of AnimalService"""

        image_ext = image_response.headers['Content-Type'].split('/')[-1]

        animal_entity = self.animal_type()
        animal_entity.img_data = image_response.content
        animal_entity.processed_image = self.generate_image_name(image_ext)

        return animal_entity

    def process(self):
        """
        Main logic function. With its call main web-service flow starts.
        Here happens: call to service-provider of images;
        creating of image object;
        applying of filter;
        saving to local directory;
        record to database.
        Function returns name of the image file.
        """

        response = self.call_to_service()

        image_response = requests.get(self.get_image_url(response))
        if image_response.status_code == 200:
            animal_entity = self.create_entity_from_image_response(image_response)
        else:
            raise MyError("Problems with image request. Please try again later")

        animal_entity.img_data = PillowEnhancer.enhance(animal_entity.img_data)

        animal_entity.fullpath_to_file = self.disk_worker.save_to_disk(animal_entity.img_data,
                                                                       animal_entity.processed_image)

        try:
            db.session.add(animal_entity)
            db.session.commit()
        except:
            db.session.rollback()
            raise MyError("Database problem. Failed to save request data")

        return animal_entity.processed_image


class CatService(AnimalService):
    """Class of Cat object which supports logic of work with image object
    and connect to cat model object"""

    def __init__(self):
        """Initialising child class with custom parameters"""

        self.service_url = 'http://aws.random.cat/meow'
        self.animal_type = Cat
        super().__init__(self.service_url, self.animal_type)

    def get_image_url(self, response):
        """Function of custom image URL retrieving from service response in json format.
        Receives - response data and returns URL to image"""

        return response['file']


class DogService(AnimalService):
    """Class of Dog object which supports logic of work with image object
    and connect to dog model object"""

    def __init__(self):
        """Initialising child class with custom parameters"""

        self.service_url = 'http://shibe.online/api/shibes'
        self.animal_type = Dog
        super().__init__(self.service_url, self.animal_type)

    def get_image_url(self, response):
        """Function of custom image URL retrieving from service response in json format.
        Receives - response data and returns URL to image"""

        return response[0]


class FoxService(AnimalService):
    """Class of Fox object which supports logic of work with image object
    and connect to fox model object"""

    def __init__(self):
        """Initialising child class with custom parameters"""

        self.service_url = 'https://randomfox.ca/floof/'
        self.animal_type = Fox
        super().__init__(self.service_url, self.animal_type)

    def get_image_url(self, response):
        """Function of custom image URL retrieving from service response in json format.
        Receives - response data and returns URL to image"""

        return response['image']
