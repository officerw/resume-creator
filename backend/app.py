from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

# APP
#
# The purpose of this file is to render the built frontend found in
# resume-creator/frontend/dist/, offer this rendering to the user when this
# flask server is accessed, and create PDF's based on the 
# user provided information.

# Select dist/ folder from frontend that contains the built Vue frontend
# dist/static/ contains all JS, CSS, and image assets of the Vue build
app = Flask(__name__, static_folder = "../frontend/dist/static", template_folder = "../frontend/dist")

# Enable CORS
CORS(app)

# Render main index.html, all JS, CSS, and images of the Vue build
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def index(path):
    return render_template("index.html")
