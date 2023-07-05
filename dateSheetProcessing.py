import re
import pandas as pd
import pdfplumber
import numpy as np

path = "C:/Users/coolm/Downloads/datesheet.pdf"
df = pd.DataFrame(columns=["TIME", "DATE", "UPC"])  # data frame to store time,upc,date


def processss_file(path):
    months = [
        "jan",
        "feb",
        "mar",
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
    pdf = pdfplumber.open(path)
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
                        row = [d, y, c]
                        df.loc[len(df)] = row
    return df


def read_df():
    print(df.head())


def map_files(dateTimeDf):  # Ab kar rha hai shayad kaam.
    studentDf = pd.read_excel("Data\ExternalData\studentData.xlsx")
    studentDf["PAPER CODE"] = studentDf["PAPER CODE"].astype(str)
    dateTimeDf["UPC"] = dateTimeDf["UPC"].astype(str)
    print(len(studentDf))

    mergedDf = pd.merge(
        dateTimeDf, studentDf, left_on="UPC", right_on="PAPER CODE", how="right"
    )

    mergedDf.to_excel("Output/result.xlsx")


dateTimeDf = processss_file(path)
map_files(dateTimeDf)
