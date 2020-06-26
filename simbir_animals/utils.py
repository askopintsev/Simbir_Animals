import os
import random

from PIL import Image, ImageFilter


class DiskWorker:
    """Class performs saving of the random image to local directory
    and search of image by given uuid"""

    def __init__(self):
        self.path = os.getcwd() + "/simbir_animals/static/"

    def save_to_disk(self, file_data, file_name):
        """Function receives an object of random image,
         defines path to local directory 'static' and set it to object,
         and serialises the object to image file"""

        fullpath_to_file = self.path + file_name

        if not os.path.exists(self.path):
            os.makedirs(self.path)

        with open(fullpath_to_file, 'wb') as file:
            file.write(file_data)

        return fullpath_to_file

    def search_file(self, uuid):
        """Function receives image uuid and scan static directory for match"""

        for file in os.listdir(self.path):
            if os.path.isfile(os.path.join(self.path, file)) and file.split('.')[0] == uuid:
                return file
        return "Not found"


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
