from mainApp.MainFoldersSystem import JSONMainFoldersController
from flask import jsonify, request
from mainApp import app


@app.route('/folders', methods=['GET'])
def getFolders():
    return jsonify(JSONMainFoldersController.getFolders()), 201


@app.route('/folders/<id>', methods=['GET', 'POST'])
def folder(id):
    if request.method == 'POST':
        JSONMainFoldersController.addFolder(id, request.get_json())
    return jsonify(JSONMainFoldersController.getFolders()), 201
