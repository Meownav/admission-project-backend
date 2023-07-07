import pandas as pd
import pdfplumber
import numpy as np
import roman
import re
import os


def process_file(datesheetPath):
    months = [
        "apr",
        "may",
        "jun",
        "jul",
        "aug",
        "sep",
        "oct",
        "nov",
        "dec",
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    days = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ]
    semesters = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]

    df = pd.DataFrame(
        columns=["TIME", "DATE", "UPC", "TERM"]
    )  # data frame to store time,upc,date

    pdf = pdfplumber.open(datesheetPath)
    pages = pdf.pages
    print("total pages", len(pages))

    for page in pages:
        text = page.extract_text()
        search_line2 = re.compile(r"_______")

        counter = False
        for line in text.split("\n"):
            if re.match("TIME OF COMMENCEMENT", line):
                c = line.split()
                d = " ".join(c[4:])
            if (
                any(day in line.lower() for day in days)
                and any(month in line.lower() for month in months)
                and ("printed" not in line.lower())
            ):
                a = line.split("(")
                counter = True
                y = a[0]
            elif search_line2.match(line):
                counter = False
            elif counter:
                line_split = list(line.split())
                for c in line_split:
                    if re.match(r"\d{7}", c):
                        row = [d, y, c, semester]
                        df.loc[len(df)] = row
                        break
                    elif any(sem == c for sem in semesters):
                        semester = str(roman.fromRoman(c)) + " SEMESTER"
    return df


def map_files(dateTimeDf):
    studentDf = (
        pd.read_excel("Data/InternalData/Data.xlsx")
        if not os.path.exists("Data\InternalData\DatesheetResult.xlsx")
        else pd.read_excel("Data\InternalData\DatesheetResult.xlsx")
    )
    if not os.path.exists("Data\InternalData\DatesheetResult.xlsx"):
        print("Data/InternalData/Data.xlsx")
    else:
        print("Data\InternalData\DatesheetResult.xlsx")

    # data frame to store the students data excel file
    studentDf["PAPER CODE"] = studentDf["PAPER CODE"].astype(str)
    dateTimeDf["UPC"] = dateTimeDf["UPC"].astype(str)
    print(len(studentDf))

    # First time
    if not any(column in ["TIME", "DATE"] for column in studentDf.columns):
        # print("Made to 1st")
        studentDf["TIME"] = [np.nan for _ in range(len(studentDf))]
        studentDf["DATE"] = [np.nan for _ in range(len(studentDf))]
        for studentIdx in range(len(studentDf)):
            for dateIdx in range(len(dateTimeDf)):
                if (
                    studentDf.loc[studentIdx, "PAPER CODE"]
                    == dateTimeDf.loc[dateIdx, "UPC"]
                ) and (
                    studentDf.loc[studentIdx, "TERM"] == dateTimeDf.loc[dateIdx, "TERM"]
                ):
                    studentDf.loc[studentIdx, "TIME"] = dateTimeDf.loc[dateIdx, "TIME"]
                    studentDf.loc[studentIdx, "DATE"] = dateTimeDf.loc[dateIdx, "DATE"]
            if studentIdx % 100 == 0:
                print(studentIdx)
        studentDf.to_excel("Data/InternalData/DatesheetResult.xlsx", index=False)
        return
    # Second time onwards
    else:
        # print("Made to 2nd")
        for studentIdx in range(len(studentDf)):
            for dateIdx in range(len(dateTimeDf)):
                # if paper code matches with upc code
                if (
                    studentDf.loc[studentIdx, "PAPER CODE"]
                    == dateTimeDf.loc[dateIdx, "UPC"]
                ) and (
                    studentDf.loc[studentIdx, "TERM"] == dateTimeDf.loc[dateIdx, "TERM"]
                ):
                    studentDf.loc[studentIdx, "TIME"] = dateTimeDf.loc[dateIdx, "TIME"]
                    studentDf.loc[studentIdx, "DATE"] = dateTimeDf.loc[dateIdx, "DATE"]

            if studentIdx % 100 == 0:
                print(studentIdx)
        studentDf.to_excel("Data/InternalData/DatesheetResult.xlsx", index=False)
        return


def startProcessing(datesheetPath):
    dateTimeDf = process_file(datesheetPath)
    map_files(dateTimeDf)
