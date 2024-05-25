from flask import Flask, jsonify, render_template, request, send_from_directory
from flask_cors import CORS

# APP
#
# The purpose of this file is to render the built frontend found in
# resume-creator/frontend/dist/, provide this to a user when this flask
# server is accessed, and allow the rendered frontend to access
# the PDF creation functionality.

# Select dist/ folder from frontend that contains the built Vue frontend
# dist/static/ contains all JS, CSS, and image assets of the Vue build
app = Flask(__name__, static_folder = "../frontend/dist/static", template_folder="../frontend/dist")

# enable CORS for all routes
CORS(app)

# Render main index.html, all JS, CSS, and images of the Vue build
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def index(path):
    return render_template("index.html")
