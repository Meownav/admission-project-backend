import os
import time
import pandas as pd
from flask_cors import CORS
from flask import Flask, request, jsonify, send_from_directory

import processStudentFile

app = Flask(__name__)
CORS(app)

# DEST_PATH = "./Data/InternalData/Data.xlsx"
# OUTPUT_DIR = "./Output/"
# OUTPUT_DIR = "./Data/ExternalData/dummy_uts.xlsx"


# src_path = "./Data/ExternalData/dummy_uts.xlsx"
# dest_path = "./Data/ExternalData/dummy_uts.xlsx"
# @app.route("/process_student_data", methods=["POST"])
# def process_student_data(src_path, dest_path):
@app.route("/Course_master", methods=["POST"])
def course_master(src_path, dest_path):
    processStudentFile.create_course_master(src_path,dest_path)
    print("course_master success")

@app.route("/subject_master", methods=["POST"])
def subjet_master():#(src_path):
    processStudentFile.create_subject_master(src_path,)
    print("subject_master success")


@app.route("/date_master", methods=["POST"])
def date_master():#(src_path,):
    processStudentFile.create_date_master(src_path,)
    print("date_master success")


@app.route("/final_dates", methods=["POST"])
def final_dates(src_path,):
    processStudentFile.map_dates(src_path,)
    print("mapping dates success")


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


# @app.route("/")
# def home():
#     return "<h1>Backend for the admission project.</h1>"


if __name__ == "__main__":
    print("Server Started.")
    app.run(host="0.0.0.0", port=5000)
