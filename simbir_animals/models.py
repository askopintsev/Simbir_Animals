import os
import random
import uuid
from datetime import datetime

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
        """Initialisation of parent class and basic attributes for children.
        Gets the value of child class name as animal_type value"""

        self.animal_type = animal_type
        self.img_data = None
        self.fullpath_to_file = None
        # Here the uuid name of image is generating without file extension
        # (extension will be added in Disksaver.save_to_disk)
        self.processed_image = str(uuid.uuid4())


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

        response = requests.get(self.service_url)
        json_response = response.json()
        image_response = requests.get(json_response['file'])
        image_ext = image_response.url.split('.')[-1]
        self.img_data = image_response.content
        self.processed_image = self.processed_image + '.' + image_ext

    def get_image_alt(self):
        """Function alternative to get_image if 'http://aws.random.cat/meow' not working"""

        image_response = requests.get('https://cataas.com/c')
        image_ext = image_response.headers['Content-Type'].split('/')[-1]
        self.img_data = image_response.content
        self.processed_image = self.processed_image + '.' + image_ext


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
        image_response = requests.get(json_response[0])
        image_ext = image_response.headers['Content-Type'].split('/')[-1]
        self.img_data = image_response.content
        self.processed_image = self.processed_image + '.' + image_ext


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
        image_response = requests.get(json_response['image'])
        image_ext = image_response.headers['Content-Type'].split('/')[-1]
        self.img_data = image_response.content
        self.processed_image = self.processed_image + '.' + image_ext


class DiskSaver:
    """Class performs saving of the random image of animal to local directory"""

    @staticmethod
    def save_to_disk(obj):
        """Function receives an object of random image,
         defines path to local directory 'static' and set it to object,
         and serialises the object to image file"""

        path_of_app = os.getcwd() + "/simbir_animals/static/"
        obj.fullpath_to_file = path_of_app + obj.processed_image

        if not os.path.exists(path_of_app):
            os.makedirs(path_of_app)

        with open(obj.fullpath_to_file, 'wb') as file:
            file.write(obj.img_data)


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


class FileSearcher:
    """Class performs file searching in directory when image is called by uuid"""

    @staticmethod
    def search_file(filename):
        """Function receives image uuid and scan static directory for match"""

        path = os.getcwd() + "/simbir_animals/static/"
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)) and file.split('.')[0] == filename:
                return file
