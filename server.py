import os
import time
import pandas as pd
from flask_cors import CORS
from flask import Flask, request, jsonify, send_from_directory

import processStudentFile

app = Flask(__name__)
CORS(app)

DEST_PATH = "./Data/InternalData/Data.xlsx"
OUTPUT_DIR = "./Output/"


@app.route("/process_student_data", methods=["POST"])
def process_student_data(src_path, dest_path):
    processStudentFile.create_course_master(src_path, dest_path)

    processStudentFile.create_subject_master(
        os.path.join(OUTPUT_DIR, "new_student_data_course_master.xlsx"),
        os.path.join(dest_path),
    )


process_student_data(r"Data/ExternalData/dummy_uts.xlsx", OUTPUT_DIR)


# @app.route("/")
# def home():
#     return "<h1>Backend for the admission project.</h1>"


# if __name__ == "__main__":
#     print("Server Started.")
#     app.run(host="0.0.0.0", port=5000)
