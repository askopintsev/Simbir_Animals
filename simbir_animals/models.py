from datetime import datetime

from simbir_animals import db


class DBAnimal(db.Model):
    """
    Parent class for animal model classes.
    It also defines basic attributes for class logic
    """

    ID = db.Column(db.Integer, primary_key=True)
    animal_type = db.Column(db.String(50), nullable=False)
    processed_image = db.Column(db.String(64), nullable=False)
    created = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self):
        """Initialisation of parent class and basic attributes for children.
        Gets the value of child class name as animal_type value"""

        self.animal_type = self.__class__.__name__
        self.processed_image = None
        self.img_data = None
        self.fullpath_to_file = None


class Cat(DBAnimal):
    """
    Model class for random cat image
    """


class Dog(DBAnimal):
    """
    Model class for random dog image
    """


class Fox(DBAnimal):
    """
    Model class for random fox image
    """
