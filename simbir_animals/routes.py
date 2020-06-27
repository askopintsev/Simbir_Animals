from flask import render_template

from simbir_animals import app
from simbir_animals.models import DBAnimal
from simbir_animals.services import CatService, DogService, FoxService
from simbir_animals.utils import DiskWorker, MyError


@app.route('/', methods=['GET'])
def hello_world():
    """Function returns render of web-service starting page"""

    return render_template('index.html')


@app.route('/animal/cat', methods=['GET'])
def cat_service():
    """Function returns render of page with random cat image.
    Before render all image logic is happening in CatService().process() call"""

    try:
        processed_image = CatService().process()
    except MyError as error:
        return str(error)
    except Exception as err:
        return str(err)

    return render_template('cat.html', content='/static/' + processed_image)


@app.route('/animal/dog', methods=['GET'])
def dog_service():
    """Function returns render of page with random dog image.
    Before render all image logic is happening in DogService().process() call"""

    try:
        processed_image = DogService().process()
    except MyError as error:
        return str(error)
    except Exception as err:
        return str(err)

    return render_template('dog.html', content='/static/' + processed_image)


@app.route('/animal/fox', methods=['GET'])
def fox_service():
    """Function returns render of page with random fox image.
    Before render all image logic is happening in FoxService().process() call"""

    try:
        processed_image = FoxService().process()
    except MyError as error:
        return str(error)
    except Exception as err:
        return str(err)

    return render_template('fox.html', content='/static/' + processed_image)


@app.route('/history', methods=['GET'])
def get_history():
    """Function returns render of page with history of image queries from database"""

    try:
        history = DBAnimal.query.all()
    except Exception as err:
        return str(err)

    return render_template('history.html', history=history)


@app.route('/history/static/', methods=['GET'])
@app.route('/history/static/<uuid>', methods=['GET'])
def get_history_uuid(uuid=None):
    """Function returns render of page with image by image name (uuid)"""

    if uuid:
        disk_worker = DiskWorker()
        try:
            image_name = disk_worker.search_file(uuid)
        except MyError as error:
            return str(error)
        except Exception as err:
            return str(err)

        return render_template('static.html', image_path='/static/' + image_name)
    else:
        return "Please enter uuid of image like this (file extension not allowed): /history/static/uuid"
