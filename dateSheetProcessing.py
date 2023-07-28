import pandas as pd
import pdfplumber
import numpy as np
import roman
import re
import os


# TODO: SET DATE
def process_file_nep(pages):
    all_tables = []

    df = pd.DataFrame(columns=["TERM", "DATE", "UPC", "TIME"])

    for page in pages:
        for row_batch in page.extract_tables():
            for row in row_batch:
                all_tables.append(row)

    for rowIdx, row in enumerate(all_tables):
        if not any(
            "commencement" in str(_).lower() for _ in row
        ):  # If it is not the header.
            row[4] = (
                row[4]
                if row[4] != None and row[4] != "None"
                else all_tables[rowIdx - 1][4]
            )  # Using previous time value if current time in row is null.

            df.loc[len(df)] = [
                str(roman.fromRoman(str("IV"))) + " SEMESTER",
                "17 Jan, 2002",
                row[2],
                row[4].replace("\n", " "),  # Removing the newline char because why not.
            ]

    print(df)
    return df


def process_file_cbcs(pages):
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
    print("CBCS")
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


def process_file(datesheetPath):
    pdf = pdfplumber.open(datesheetPath)
    pages = pdf.pages
    text = ""

    for page in pages:
        text += page.extract_text()
    # print(text)

    if "CBCS-LOCF" in text.upper():
        print("CBCS")
        return process_file_cbcs(pages)
    elif "NEP-UGCF" in text.upper():
        return process_file_nep(pages)
    else:
        print("Some error occurred while processing.")


def map_files(dateTimeDf):
    print(dateTimeDf)
    studentDf = (
        pd.read_excel("Data/InternalData/Data.xlsx")
        if not os.path.exists("Data\InternalData\DatesheetResult.xlsx")
        else pd.read_excel("Data\InternalData\DatesheetResult.xlsx")
    )

    # data frame to store the students data excel file
    studentDf["PAPER CODE"] = studentDf["PAPER CODE"].astype(str)
    dateTimeDf["UPC"] = dateTimeDf["UPC"].astype(str)

    # First time
    if not any(column in ["TIME", "DATE"] for column in studentDf.columns):
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
    # Second time onwards
    else:
        for studentIdx in range(len(studentDf)):
            for dateIdx in range(len(dateTimeDf)):
                # If paper code matches with upc code and term of excel file matches with term of df.
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


def startProcessing(datesheetPath):
    dateTimeDf = process_file(datesheetPath)
    map_files(dateTimeDf)


# process_file(r"C:/Users/coolm/Downloads/nw1.pdf")

