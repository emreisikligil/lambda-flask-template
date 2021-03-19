from datetime import datetime, timezone
from enum import Enum
from typing import List
from logging import getLogger
from os.path import join, dirname, exists
from werkzeug.exceptions import HTTPException, Unauthorized, InternalServerError, NotFound
from flask import jsonify, send_file
from http import HTTPStatus

from application import Application
from application.models import Pet, session_scope

logger = getLogger(__name__)
app = Application.app
db = Application.db
schema = Application.schema
auth = Application.auth


@app.route("/", methods=["GET"])
def health():
    return dict(status="UP"), 200


@app.route("/spec", methods=["GET"])
def apidocs():
    filename = join(dirname(__file__), "../docs/index.html")
    if not exists(filename):
        raise NotFound("API documentation not found")
    return send_file(filename)


@app.route("/pets", methods=["POST"])
@schema.validate("AddPetRequest")
@auth.authenticated
def addPet(body, claims):
    # Check if claims.sub has access to this resource. JWT is already verified at this stage.
    # We can use body dict as it is since it is already validated
    pet = Pet(**body)
    with session_scope() as s:
        s.add(pet)
    return pet.todict(), HTTPStatus.CREATED


@app.route("/pets", methods=["GET"])
@auth.authenticated
def getPets(claims):
    # Check if claims.sub has access to this resource. JWT is already verified at this stage.
    # This is just a template. Remember to add pagination here :)
    pets = Pet.query.all()
    return jsonify([p.todict() for p in pets]), HTTPStatus.OK


@app.errorhandler(InternalServerError)
def handle_unauthorized_error(e):
    logger.exception(e)
    return dict(error="An internal server error occured."), e.code


@app.errorhandler(HTTPException)
def handle_http_error(e):
    logger.exception(e)
    return dict(msg=e.description), e.code
