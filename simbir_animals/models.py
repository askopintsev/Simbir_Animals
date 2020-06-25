from datetime import datetime
import os
import random
import uuid

import requests
from PIL import Image, ImageFilter

from simbir_animals import db


class DBAnimal(db.Model):
    """
    Parent class for animal type classes.
    It also defines database model and basic attributes for class logic
    """

    ID = db.Column(db.Integer, primary_key=True)
    animal_type = db.Column(db.String(50), nullable=False)
    processed_image = db.Column(db.String(64), nullable=False)
    created = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, animal_type):
        """Initialisation of parent class and basic attributes for children"""

        self.animal_type = animal_type
        self.processed_image = str(uuid.uuid4()) + '.jpg'  # Here the name of image is generating
        self.img_data = None
        self.fullpath_to_file = None


class Cat(DBAnimal):
    """
    Class for random cat image.
    Cat supports method for retrieve image data from Internet
    """

    def __init__(self):
        """Initialisation of Cat object.
        API-service address is stored in self.service_url parameter.
        Basic attributes are initialized through parent call"""

        self.service_url = 'http://aws.random.cat/meow'
        super().__init__(self.__class__.__name__)

    def get_image(self):
        """Function downloads image from service using address stored in object service.
        Image is stored in self.img_data parameter as binary data"""
        # TODO Exceptions on code value
        response = requests.get(self.service_url)
        code = response.status_code
        json_response = response.json()
        self.img_data = requests.get(json_response['file'])


class Dog(DBAnimal):
    """
    Class for random dog image.
    Dog supports method for retrieve image data from Internet
    """

    def __init__(self):
        """Initialisation of Dog object.
        API-service address is stored in self.service_url parameter.
        Basic attributes are initialized through parent call"""

        self.service_url = 'http://shibe.online/api/shibes'
        super().__init__(self.__class__.__name__)

    def get_image(self):
        """Function downloads image from service using address stored in object service.
        Image is stored in self.img_data parameter as binary data"""

        response = requests.get(self.service_url)
        json_response = response.json()
        self.img_data = requests.get(json_response[0])


class Fox(DBAnimal):
    """
    Class for random fox image.
    Fox supports method for retrieve image data from Internet
    """

    def __init__(self):
        """Initialisation of Fox object.
        API-service address is stored in self.service_url parameter.
        Basic attributes are initialized through parent call"""

        self.service_url = 'https://randomfox.ca/floof/'
        super().__init__(self.__class__.__name__)

    def get_image(self):
        """Function downloads image from service using address stored in object service.
        Image is stored in self.img_data parameter as binary data"""

        response = requests.get(self.service_url)
        json_response = response.json()
        self.img_data = requests.get(json_response['image'])


class DiskSaver:
    """Class performs saving of the random image of animal to local directory"""

    @staticmethod
    def save_to_disk(obj):
        """Function receives an object of random image,
         defines path to local directory 'static' and set it to object,
         and serialises the object to image file"""

        path_of_app = os.getcwd()
        path_to_static = "/simbir_animals/static/"
        # absolute_path = os.path.dirname(os.path.abspath(__file__)) + '/static/'
        obj.fullpath_to_file = path_of_app + path_to_static + obj.processed_image

        if not os.path.exists(path_of_app + path_to_static):
            os.makedirs(path_of_app + path_to_static)

        with open(obj.fullpath_to_file, 'wb') as file:
            for part in obj.img_data.iter_content(512):
                file.write(part)


class PillowEnhancer:
    """Class serves to apply a filter from PIL library to image"""

    @staticmethod
    def enhance(filepath):
        """Function receives full path to stored image
        and applies random effect from 'filters' collection.
        After filter application upgraded image replace original in local directory"""

        filters = (ImageFilter.BLUR, ImageFilter.CONTOUR, ImageFilter.DETAIL,
                   ImageFilter.EDGE_ENHANCE, ImageFilter.EDGE_ENHANCE_MORE,
                   ImageFilter.EMBOSS, ImageFilter.FIND_EDGES, ImageFilter.SHARPEN,
                   ImageFilter.SMOOTH, ImageFilter.SMOOTH_MORE)

        image = Image.open(filepath)
        image = image.convert('RGB')
        random_filter = filters[random.randint(0, len(filters) - 1)]

        upgraded_image = image.filter(random_filter)
        upgraded_image.save(filepath)
