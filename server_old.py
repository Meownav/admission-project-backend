import os
import time
import pandas as pd
from flask_cors import CORS
from flask import Flask, request, jsonify, send_from_directory
import dateSheetProcessing

app = Flask(__name__)
CORS(app)

DEST_PATH = "./Data/InternalData/Data.xlsx"
OUTPUT_DIR = "./Output/"


def process_files(src_path, dest_path, res_path):
    src_df = pd.read_excel(src_path)

    if os.path.exists(dest_path):
        dest_df = pd.read_excel(dest_path)
        new_data = (
            src_df[~src_df.isin(dest_df)].drop_duplicates().reset_index(drop=True)
        )
        # dest_df = pd.concat([dest_df, new_data]).reset_index(drop=True)
        src_df.to_excel(dest_path, index=False)
        new_data.reset_index(drop=True).to_excel(res_path, index=False)
        return True
    else:
        src_df.to_excel(dest_path, index=False)
        src_df.to_excel(res_path, index=False)
        return True


@app.route("/process-file", methods=["POST"])
def process_file():
    file = request.files["file"]

    if file.filename == "":
        return jsonify({"message": "No file selected."}), 400

    try:
        src_path = (
            "./Data/ExternalData/uploaded_file"
            + time.strftime("%d-%m-%Y_%H_%M_%S")
            + ".xlsx"
        )
        file.save(src_path)

        res_path = OUTPUT_DIR + "Result_" + time.strftime("%d-%m-%Y_%H_%M_%S") + ".xlsx"

        if process_files(src_path, DEST_PATH, res_path):
            return jsonify(message="File processed successfully.", result_path=res_path)
        else:
            return (
                jsonify({"message": "An error occurred during file processing."}),
                500,
            )
    except Exception as e:
        return jsonify(message="An error occurred.", error=str(e)), 500


@app.route("/download-result", methods=["GET"])
def download_result():
    try:
        res_path = request.args.get("resultPath")
        filename = res_path.split("/")[-1]
        print(" filename is : ", filename)
        return send_from_directory(
            OUTPUT_DIR,
            filename,
            as_attachment=True,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    except Exception as e:
        return (
            jsonify(
                message="An error occurred while downloading the result file.",
                error=str(e),
            ),
            500,
        )

    # @app.route("/process-datesheet", methods=["POST"])
    # def process_datesheet():
    try:
        datesheet_files = request.files.getlist("datesheet")
        for file in datesheet_files:
            file.save("Data/ExternalData/" + file.filename)

        for file in datesheet_files:
            dateSheetProcessing.startProcessing(
                datesheetPath="Data/ExternalData/" + file.filename
            )

        result_path = "Data/InternalData/DatesheetResult.xlsx"
        return jsonify(
            message="Datesheet processed successfully", result_path=result_path
        )
    except Exception as e:
        return jsonify(message="An error occured.", error=str(e)), 500

    # @app.route("/download-datesheet", methods=["GET"])
    # def download_datesheet():
    try:
        res_path = request.args.get("resultPath")
        filename = res_path.split("/")[-1]
        print(" filename is : ", filename)
        return send_from_directory(
            "Data/InternalData",
            filename,
            as_attachment=True,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    except Exception as e:
        return (
            jsonify(
                message="An error occurred while downloading the result file.",
                error=str(e),
            ),
            500,
        )


@app.route("/")
def home():
    return "<h1>Backend For The Admission Project.</h1>"


if __name__ == "__main__":
    print("Server Started.")
    app.run(host="0.0.0.0", port=5000)
