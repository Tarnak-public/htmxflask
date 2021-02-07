import flask
from flask_bootstrap import Bootstrap

# URLS Served:
# / OR /index.html
# /models/
# /static/js/htmx.js  (really, cause got nothing else )

app = flask.Flask(__name__, static_url_path='/static')
bootstrap = Bootstrap(app)


@app.route('/')
@app.route('/index.html')
def index():
    return flask.render_template('index.html')


@app.route('/loadImageToCompare', methods=['GET', 'POST'])
def pressed_load_image_to_compare():
    print("loadImageToCompare")
    return '', 204


@app.route('/galleryComboBox', methods=['GET', 'POST'])
def pressed_gallery_combobox():
    print("galleryComboBox")
    return '', 204


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
