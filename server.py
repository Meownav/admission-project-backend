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


@app.route("/get_report", methods=["GET", "POST"])
def get_report():
    try:
        df = pd.read_excel("./Data/ExternalData/dummy_uts.xlsx")
        x = df.groupby(['Programme Name','Paper Type'])
        out = x['Paper Type'].value_counts()
        out = pd.DataFrame(out)
        cols = list(set(df['Paper Type']))
        ind = list(set(df['Programme Name']))
        data = pd.DataFrame(data = out,columns=cols,index=ind)
        for idx, row in out.iterrows():
            data.loc[idx] = row['count'] if row['count'] else "NAN"

        for i in ind:
            data.loc[i,'Total'] = data.loc[i,:].sum()
        for i in cols:
            data.loc['Total',[i]] = data.loc[:,[i]].sum()

        data.loc['Total','Total'] = data.loc[:,'Total'].sum()
        series_json = data.reset_index().to_json(orient="records")
        print(type(series_json))
        return jsonify(message="Success", data=series_json)
    except Exception as e:
        print(str(e))
        return jsonify(message="An error occurred.", error=str(e)), 500
    
@app.route("/get_reporttwo", methods=["GET", "POST"])
def get_reporttwo():
    try:
        df = pd.read_excel("./Data/ExternalData/dummy_uts.xlsx")
        df['Gender'].replace('M','Male',inplace=True)
        df['Gender'].replace('F','Female',inplace=True)
        x = df.groupby(['Programme Name','Gender'])
        out = x['Gender'].value_counts()
        out = pd.DataFrame(out)
        cols = list(set(df['Gender']))
        ind = list(set(df['Programme Name']))
        data = pd.DataFrame(data = out,columns = cols,index = ind)
        for idx, row in out.iterrows():
            data.loc[idx] = row['count'] if row['count'] else "NAN"

        for i in ind:
            data.loc[i,'Total'] = data.loc[i,:].sum()
        for i in cols:
            data.loc['Total',i] = data.loc[:,i].sum()
        data.loc['Total','Total'] = data.loc[:,'Total'].sum()
        series_json = data.reset_index().to_json(orient="records")
        print(type(series_json))
        return jsonify(message="Success", data=series_json)
    except Exception as e:
        print(str(e))
        return jsonify(message="An error occurred.", error=str(e)), 500

@app.route("/get_options", methods=["GET", "POST"])
def get_options():
    try:
        df=pd.read_excel(SRC_PATH,sheet_name="course_master")
        options=df['Programme Name'].to_json()
        return jsonify(message="Success",data=options)
    except Exception as e:
        print(str(e))
        return jsonify(message="An error occurred.", error=str(e)), 500

@app.route("/submit_selected_options",methods=["GET","POST"])
def selected_options():
    try:
        courses=list(request.form.get('array').split(","))
        df=pd.read_excel(SRC_PATH,sheet_name="student_data")
        a=df[df["Programme Name"].isin(courses)]
        a=a[["Name","Exam Roll Number","Email"]].drop_duplicates()
        a=a.to_json(orient="records")
        return jsonify(message="Success",data=a)
    except Exception as e:
        print(str(e))
        return jsonify(message="An error occurred.", error=str(e)), 500

@app.route("/")
def home():
    return "<h1>Backend for the admission project.</h1>"


if __name__ == "__main__":
    print("Server Started.")
    app.run(host="0.0.0.0", debug=True, port=5000)
