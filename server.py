import os
import time
import pandas as pd
from flask_cors import CORS
from flask import Flask, request, jsonify, send_from_directory

import processStudentFile

app = Flask(__name__)
CORS(app)

SRC_DIR = "./Data/ExternalData/"
SRC_PATH = "./Data/ExternalData/dbFile.xlsx"
DEST_PATH = "./Data/ExternalData/dbFile.xlsx"


# Saves the submitted db_file.
@app.route("/submit_file", methods=["POST", "GET"])
def save_submitted_file():
    file = request.files["dbFile"]
    try:
        file.save("./Data/ExternalData/dbFile.xlsx")
        return jsonify(message="File processed successfully")

    except Exception as e:
        return jsonify(message="An error occurred.", error=str(e)), 500


# Creates the course master sheet.
@app.route("/course_master", methods=["POST", "GET"])
# def course_master(src_path, dest_path):
def course_master():
    try:
        processStudentFile.create_course_master(SRC_PATH, DEST_PATH)
        print("course_master success")
        return jsonify(message="Course master created successfully")
    except Exception as e:
        return jsonify(message="An error occurred.", error=str(e)), 500


# Creates the subject master sheet.
@app.route("/subject_master", methods=["POST", "GET"])
def subjet_master():
    try:
        processStudentFile.create_subject_master(
            SRC_PATH,
        )
        print("subject_master success")
        return jsonify(message="Subject master created successfully.")
    except Exception as e:
        return jsonify(message="An error occurred.", error=str(e)), 500


# Creates the subject date sheet.
@app.route("/date_master", methods=["POST", "GET"])
def date_master():
    try:
        processStudentFile.create_date_master(
            SRC_PATH,
        )
        print("date_master success")
        return send_from_directory(
            SRC_DIR,
            SRC_PATH.split("/")[-1],
            as_attachment=True,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    except Exception as e:
        return jsonify(message="An error occurred.", error=str(e)), 500


# Saves the date_file.
@app.route("/submit_date_file", methods=["POST", "GET"])
def submit_date_file():
    file = request.files["dateFile"]
    try:
        file.save("./Data/ExternalData/dbFile.xlsx")
        return jsonify(message="File processed successfully")

    except Exception as e:
        return jsonify(message="An error occurred.", error=str(e)), 500


# Maps the dates.
@app.route("/final_dates", methods=["POST", "GET"])
def final_dates():
    try:
        processStudentFile.map_dates(
            SRC_PATH,
        )
        print("mapping dates success")
        return send_from_directory(
            SRC_DIR,
            SRC_PATH.split("/")[-1],
            as_attachment=True,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    except Exception as e:
        print(str(e))
        return jsonify(message="An error occurred.", error=str(e)), 500


# process_student_data(r"Data/ExternalData/dummy_uts.xlsx", OUTPUT_DIR)


# @app.route("/process_student_data", methods=["POST"])
# def process_student_data(src_path, dest_path):
#     if (
#         input(
#             "Press D to process the dates. OR Press Enter to create the course master"
#         ).lower()
#         != "d"
#     ):
#         processStudentFile.create_course_master(src_path, dest_path)
#         print("Course master has been created.")

#         input("Press enter to create subject master.")
#         processStudentFile.create_subject_master(
#             # os.path.join(OUTPUT_DIR, "new_student_data_course_master.xlsx"),
#             src_path,
#         )
#         print("Subject master has been created.")

#         input("Press enter to create data master.")
#         processStudentFile.create_date_master(
#             # os.path.join(OUTPUT_DIR, "new_student_data_course_master.xlsx"),
#             src_path,
#         )
#         print("Subject master has been created. Please write the dates in the file.")
#     else:
#         if (
#             input(
#                 "Press Q to go back and write the dates in the subject master OR press enter to map dates."
#             ).lower()
#             == "q"
#         ):
#             pass
#         else:
#             processStudentFile.map_dates(
#                 # os.path.join(OUTPUT_DIR, "new_student_data_course_master.xlsx")
#                 src_path
#             )
#             print("OO")


# process_student_data(r"Data/ExternalData/dummy_uts.xlsx", OUTPUT_DIR)


@app.route("/")
def home():
    return "<h1>Backend for the admission project.</h1>"


if __name__ == "__main__":
    print("Server Started.")
    app.run(host="0.0.0.0", port=5000)
