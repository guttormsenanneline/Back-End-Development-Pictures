from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return jsonify(data), 200

    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for picture in data:
        if picture["id"] == id:
            return jsonify(picture), 200

    return {"message": "Picture not found"}, 404

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    request_picture = {
        "id": request.json["id"],
        "pic_url": request.json["pic_url"],
        "event_country": request.json["event_country"],
        "event_state": request.json["event_state"],
        "event_city": request.json["event_city"],
        "event_date": request.json["event_date"],
    }

    for picture in data:
        if picture["id"] == request_picture["id"]:
            return make_response({"Message": f'picture with id {request_picture["id"]} already present'}, 302)
    
    data.append(request_picture)

    return make_response(request_picture, 201)

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    request_picture = {
        "id": request.json["id"],
        "pic_url": request.json["pic_url"],
        "event_country": request.json["event_country"],
        "event_state": request.json["event_state"],
        "event_city": request.json["event_city"],
        "event_date": request.json["event_date"],
    }

    for picture in data:
        if picture["id"] == request_picture["id"]:
            data.remove(picture)
            data.append(request_picture)
            return make_response(request_picture, 200)
    
    return make_response({"message": "picture not found"}, 404)

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for picture in data:
        if picture["id"] == id:
            data.remove(picture)
            return make_response("", 204)
    
    return make_response({"message": "picture not found"}, 404)
