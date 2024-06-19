from flask import Flask, make_response, jsonify
from api.v1.views import app_views


app = Flask(__name__)

app.register_blueprint(app_views)

@app.errorhandler(415)
def notAJSON(error):
    return make_response(jsonify({"error": "Not a JSON"}), 415)

@app.errorhandler(400)
def missing(error):
    return make_response(jsonify({"error": "Missing Required Parameters"}), 400)


if __name__ == "__main__":
    app.run(debug=True)