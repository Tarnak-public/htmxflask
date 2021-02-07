import requests

from FaceRecog import apiConstants

gallery_name_krzys = 'krzys'
server_api = ""
server_api_port = "5000"
server_ip = "192.168.1.6"


def setup_api_server():
    global server_api
    server_port = ":5000"
    server_http = "http://"
    server_api = server_http + server_ip + server_port


def get_api_server():
    return server_api


def show_response(header, response):
    print("---------------------------------------")
    print(header + response.text)
    print(response)
    print("---------------------------------------\n")


def get_gallery_faces(gallery):
    query = {apiConstants.API_FACE_GALLERY: gallery}
    response = requests.post(server_api + '/recognition/api/v1.0/faces', json=query)
    show_response("get_gallery_faces() Body:", response)
    return server_api
