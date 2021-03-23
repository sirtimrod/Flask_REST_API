from flask import make_response, jsonify

from mainApp import app


# That handler handles the 404 error
@app.errorhandler(404)
def notFound(error):
    return make_response(jsonify({'Error': str(error)}), 404)


# That handler handles the 400 error
@app.errorhandler(400)
def badRequest(error):
    return make_response(jsonify({'Error': str(error)}), 400)
