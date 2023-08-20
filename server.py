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
    if (
        input(
            "Press D to process the dates. OR Press Enter to create the course master"
        ).lower()
        != "d"
    ):
        processStudentFile.create_course_master(src_path, dest_path)
        print("Course master has been created.")

        input("Press enter to create subject master.")
        processStudentFile.create_subject_master(
            os.path.join(OUTPUT_DIR, "new_student_data_course_master.xlsx"),
        )
        print("Subject master has been created.")

        input("Press enter to create data master.")
        processStudentFile.create_date_master(
            os.path.join(OUTPUT_DIR, "new_student_data_course_master.xlsx"),
        )
        print("Subject master has been created. Please write the dates in the file.")
    else:
        if (
            input(
                "Press Q to go back and write the dates in the subject master OR press enter to map dates."
            ).lower()
            == "q"
        ):
            pass
        else:
            processStudentFile.map_dates(
                os.path.join(OUTPUT_DIR, "new_student_data_course_master.xlsx")
            )


process_student_data(r"Data/ExternalData/dummy_uts.xlsx", OUTPUT_DIR)


# @app.route("/")
# def home():
#     return "<h1>Backend for the admission project.</h1>"


# if __name__ == "__main__":
#     print("Server Started.")
#     app.run(host="0.0.0.0", port=5000)
