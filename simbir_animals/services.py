from abc import ABC, abstractmethod

import requests
import uuid

from simbir_animals import db
from simbir_animals.models import Cat, Dog
from simbir_animals.utils import DiskWorker, PillowEnhancer


class AnimalService(ABC):
    service_url = None
    animal_type = None
    disk_worker = DiskWorker()

    def call_to_service(self):
        """Function responsible for call to service which provides random animal image.
        Function receives service URL and returns response object"""

        response = requests.get(self.service_url)
        if response.status_code == 200:
            json_response = response.json()
        else:
            return "Bad request"

        return json_response

    def process(self):
        response = self.call_to_service()

        if response == "Bad request":
            raise Exception("Service unavailable now. Please try again later")

        image_response = requests.get(self.get_image_url(response))
        animal_entity = self.create_entity_from_image_response(image_response)

        animal_entity.fullpath_to_file = self.disk_worker.save_to_disk(animal_entity.img_data, animal_entity.processed_image)
        PillowEnhancer.enhance(animal_entity.fullpath_to_file)

        db.session.add(animal_entity)
        db.session.commit()

        return animal_entity.processed_image

    def create_entity_from_image_response(self, image_response):
        image_ext = image_response.headers['Content-Type'].split('/')[-1]

        animal_entity = self.animal_type()
        animal_entity.img_data = image_response.content
        animal_entity.processed_image = self.generate_image_name(image_ext)

        return animal_entity

    def generate_image_name(self, extension):
        return str(uuid.uuid4()) + '.' + extension

    @abstractmethod
    def get_image_url(self, response):
        pass


class CatService(AnimalService):
    pass


class DogService(AnimalService):
    service_url = 'http://shibe.online/api/shibes'
    animal_type = Dog

    def get_image_url(self, response):
        return response[0]


class FoxService(AnimalService):
    pass
