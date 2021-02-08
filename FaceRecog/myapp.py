import os
import traceback

import flask
import jyserver.Flask as jsf
from flask import request, render_template
from werkzeug.utils import secure_filename

# File extension checking
import FRServiceConnector

gallery_name_krzys = 'krzys'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS_IMAGES = {'jpeg', 'jpg', 'png'}

app = flask.Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_PATH'] = 1024 * 1000


# https://dev.to/ftrias/access-js-dom-from-flask-app-using-jyserver-23h9
@jsf.use(app)
class App:
    def reset(self):
        pass
        # self.start0 = time.time()
        # self.js.dom.time.innerHTML = "{:.1f}".format(0)

    @jsf.task
    def main(self):
        pass
        # self.start0 = time.time()
        # while True:
        #     t = "{:.1f}".format(time.time() - self.start0)
        #     self.js.dom.time.innerHTML = t
        #     time.sleep(0.1)

    def faces_gallery(self, gallery_list):
        self.js.document.getElementById("ImagesInGalleryCombobox").innerHTML = '<option value="audi">Audi</option>'


def allowed_filename(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS_IMAGES


def upload_directory(filename):
    return os.path.join(app.config['UPLOAD_FOLDER'], filename)


# <option value="volvo">Volvo</option>
# <option value="saab">Saab</option>

@app.route('/', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
def index():
    App.main()
    FRServiceConnector.setup_api_server()
    option_faces = FRServiceConnector.get_gallery_faces(gallery_name_krzys)
    print("str=", option_faces)
    # return flask.render_template('index.html')
    main_page = App.render(render_template('index.html', gallery_options=option_faces))
    return main_page


@app.route('/loadImageToCompare', methods=['GET', 'POST'])
def pressed_load_image_to_compare():
    print("loadImageToCompare")
    return '', 204


@app.route('/galleryFaceSelected', methods=['GET', 'POST'])
def selected_gallery_item():
    print("galleryFaceSelected")
    return '', 204


@app.route('/galleryComboBox', methods=['GET', 'POST'])
def pressed_gallery_combobox():
    print("galleryComboBox")
    return '', 204


@app.route('/selectedImageForGallery', methods=['GET', 'POST'])
def pressed_file_selector_gallery():
    print("selectedImageForGallery: ", request.form['file'])
    path, filename = os.path.split(request.form['file'])
    print("selectedImageForGallery: ", filename)
    return '<input class="form-control" type="text" readonly="" id="addToGalleryTextbox" value = "' + filename + '">'


@app.route('/submitAddToGallery', methods=['GET', 'POST'])
def pressed_submit_to_gallery():
    print("submitAddToGallery: ", request)
    if request.method == 'POST':
        try:
            filename = request.form['addToGalleryTextbox']  # search by name="" of dom element
            new_face_name = request.form['NewFaceNameEditbox']
        except KeyError:
            print(traceback.format_exc())
            print("skip submitAddToGallery as no parameters in form")
            return '', 204

        if new_face_name is None or filename is None:
            print("skip submitAddToGallery as one or more parameters are empty")
            return '', 204

        f = request.files['file']
        print("submitAddToGallery: fileName=", filename)
        print("submitAddToGallery: faceName=", new_face_name)
        f.save(upload_directory(secure_filename(f.filename)))

    return '', 204


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
