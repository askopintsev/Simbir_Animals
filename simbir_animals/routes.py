from flask import render_template

from simbir_animals import app, db
from simbir_animals.models import DBAnimal, Cat, Dog, Fox, DiskSaver, PillowEnhancer, FileSearcher

# creating of service objects
image_enhancer = PillowEnhancer()
disk_saver = DiskSaver()


@app.route('/', methods=['GET'])
def hello_world():
    """Function returns render of web-service starting page"""

    return render_template('index.html')


@app.route('/animals/cat', methods=['GET'])
def cat_service():
    """Function returns render of page with random cat image.
    Before render all image logic is happening: object creation,
    retrieving from Internet, saving to the directory and filter applying.
    After all actions with image record about event is recorded to database"""

    cat_image = Cat()
    cat_image.get_image_alt()
    disk_saver.save_to_disk(cat_image)
    image_enhancer.enhance(cat_image.fullpath_to_file)

    db.session.add(cat_image)
    db.session.commit()

    return render_template('cat.html', content='/static/' + cat_image.processed_image)


@app.route('/animals/dog', methods=['GET'])
def dog_service():
    """Function returns render of page with random dog image.
    Before render all image logic is happening: object creation,
    retrieving from Internet, saving to the directory and filter applying.
    After all actions with image record about event is recorded to database"""

    dog_image = Dog()
    dog_image.get_image()
    disk_saver.save_to_disk(dog_image)
    image_enhancer.enhance(dog_image.fullpath_to_file)

    db.session.add(dog_image)
    db.session.commit()

    return render_template('dog.html', content='/static/' + dog_image.processed_image)


@app.route('/animals/fox', methods=['GET'])
def fox_service():
    """Function returns render of page with random fox image.
    Before render all image logic is happening: object creation,
    retrieving from Internet, saving to the directory and filter applying.
    After all actions with image record about event is recorded to database"""

    fox_image = Fox()
    fox_image.get_image()
    disk_saver.save_to_disk(fox_image)
    image_enhancer.enhance(fox_image.fullpath_to_file)

    db.session.add(fox_image)
    db.session.commit()

    return render_template('fox.html', content='/static/' + fox_image.processed_image)


@app.route('/history', methods=['GET'])
def get_history():
    """Function returns render of page with history about image queries from database"""

    return render_template('history.html', history=DBAnimal.query.all())


@app.route('/history/static/', methods=['GET'])
@app.route('/history/static/<uuid>', methods=['GET'])
def get_history_uuid(uuid=None):
    """Function returns render of page with image by image name (uuid)"""

    if uuid:
        file_searcher = FileSearcher()
        image_path = file_searcher.search_file(uuid)
        return render_template('static.html', image_path='/static/' + image_path)
    else:
        return "Please enter uuid of image like this: /history/static/uuid"
