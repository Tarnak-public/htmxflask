API_FACE_UUID = "uuid"
API_FACE_USE_MODEL = "model"  # for future which model to use
API_FACE_NAME = "name"
API_FACE_ENCODINGS = "encodings"
API_FACE_UNCATEGORIZED_IMAGE = "uncategorized_image"
API_FACE_CHECK_ALL = "check_all"
API_FACE_GALLERY = "gallery"
API_FACE_GALLERIES = "galleries"
API_FACE_TOLERANCE = "tolerance"
API_FACE_FOUND_FACES = "found_faces"
API_FACE_CROPPED_IN_IMAGE = "image_with_face_cropped"  # could implement known_face_locations to speed up
API_FACE_FACES = "faces"

API_FACE_MODEL_DEFAULT_DLIB = "face_recognition_dlib"

"""
def face_encodings(face_image, known_face_locations=None, num_jitters=1, model="small"):
    Given an image, return the 128-dimension face encoding for each face in the image.
    :param known_face_locations: Optional - the bounding boxes of each face if you already know them.
    :param num_jitters: How many times to re-sample the face when calculating encoding. Higher is more accurate, but slower (i.e. 100 is 100x slower)
    :param model: Optional - which model to use. "large" or "small" (default) which only returns 5 points but is faster.
    :return: A list of 128-dimensional face encodings (one for each face in the image)
"""
