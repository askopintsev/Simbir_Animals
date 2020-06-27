import uuid
from datetime import datetime

import requests

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

    def __init__(self, animal_type=None):
        """Initialisation of parent class and basic attributes for children.
        Gets the value of child class name as animal_type value"""

        self.animal_type = self.__class__.__name__
        self.img_data = None
        self.fullpath_to_file = None
        # Here the uuid name of image is generating without file extension
        # (extension will be added in get_image())
        self.processed_image = str(uuid.uuid4())

    def call_to_service(self):
        """Function responsible for call to service which provides random animal image.
        Function receives service URL and returns response object"""

        response = requests.get(self.service_url)
        if response.status_code == 200:
            json_response = response.json()
        else:
            return "Bad request"

        return json_response


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

    def get_image(self, response):
        """Function downloads image from service using address stored in object service.
        Image is stored in self.img_data parameter as binary data"""

        image_response = requests.get(response['file'])
        image_ext = image_response.headers['Content-Type'].split('/')[-1]
        self.img_data = image_response.content
        self.processed_image = self.processed_image + '.' + image_ext


class Dog(DBAnimal):
    """
    Class for random dog image.
    Dog supports method for retrieve image data from Internet
    """


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

    def get_image(self, response):
        """Function downloads image from service using address stored in object service.
        Image is stored in self.img_data parameter as binary data"""

        image_response = requests.get(response['image'])
        image_ext = image_response.headers['Content-Type'].split('/')[-1]
        self.img_data = image_response.content
        self.processed_image = self.processed_image + '.' + image_ext
