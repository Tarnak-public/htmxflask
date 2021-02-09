import base64
import io

import requests
from PIL import Image

import apiConstants
import myapp as myapp

server_http = "http://"
server_ip = "192.168.1.6"
server_api_port = "5000"
server_api = server_http + server_ip + ":" + server_api_port


def get_api_server():
    return server_api


def show_response(header, response):
    print("---------------------------------------")
    print(header + response.text)
    print(response)
    print("---------------------------------------\n")


def get_value_response_safe(response_json, key, default_value):
    if key not in response_json:
        return default_value
    return response_json[key]


def get_gallery_faces(gallery):
    query = {apiConstants.API_FACE_GALLERY: gallery}
    response = requests.post(server_api + '/recognition/api/v1.0/faces', json=query)
    show_response("get_gallery_faces() Body:", response)
    response_json = response.json()
    faces_array = get_value_response_safe(response_json, apiConstants.API_FACE_FACES, None)
    print("faces_array=", faces_array)
    return faces_array


def get_faces_image(gallery, face_guid):
    query = {apiConstants.API_FACE_GALLERY: gallery, apiConstants.API_FACE_UUID: face_guid}
    # print("get_faces_image=", server_api)
    response = requests.post(server_api + '/recognition/api/v1.0/image', json=query)
    # show_response("get_gallery_faces() Body:", response)
    response_json = response.json()
    b64_image = get_value_response_safe(response_json, apiConstants.API_FACE_CROPPED_IN_IMAGE, None)
    if b64_image is None:
        print("get_faces_image() no image in response")
        return
    # show_response("get_image_from_gallery() Body:", response)
    picture = Image.open(io.BytesIO(base64.b64decode(b64_image)))
    download_path = myapp.upload_directory("preview.jpeg")
    picture.save(download_path, "JPEG")
    myapp.App.update_preview_image(download_path)
    # myapp.update_preview_image_own()
