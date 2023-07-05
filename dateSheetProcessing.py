import re
import pandas as pd
import pdfplumber
import numpy as np
import roman

df = pd.DataFrame(columns=['TIME', 'DATE','UPC','TERM']) #data frame to store time,upc,date 
path="B.SC.(H) 2023-SEM.-II-IV-VI(CBCS)-LOCF-10-04-2023 (1).pdf"
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
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    semesters=["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]
    pdf= pdfplumber.open(path)
    pages = pdf.pages
    print("total pages",len(pages))
    for page in pages:
        text=page.extract_text()
#         search_line=re.compile(r'(^[1-3][0-9]|[1-9])(st|nd|rd|th)(\s)([Jj]anuary|[Ff]ebruary|[Mm]arch|[Aa]pril|[Mm]ay|[Jj]une|[Jj]uly|[Aa]ugust|[Ss]emptember|[Oo]ctober|[nN]ovember|[Dd]ecember|JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER)(\s{0,1})(,{1})(\s{0,1})([0-9]{4})(\s{1})\(')
        search_line2=re.compile(r'_______')
        
        counter=False
        for line in text.split('\n'):
            if re.match("TIME OF COMMENCEMENT",line):
               c=line.split()
               d=" ".join(c[4:])
            if any(day in line.lower() for day in days) and any (month in line.lower() for month in months) and ("printed" not in line.lower()):
                a=line.split('(')
                counter=True
                y=a[0]
            elif search_line2.match(line):
                counter=False
            elif counter:
                line_split=list(line.split())
                for c in line_split:
                    if re.match(r'\d{7}',c):
                        row=[d,y,c,semester]
                        df.loc[len(df)]=row
                        break
                    elif any(sem==c for sem in semesters):
                         semester =str(roman.fromRoman(c))+" SEMESTER"
    return df
def read_df():
    print(df.head())
#     df.to_csv('datesheet_dataframe.csv',index=False)  #to download the csv file of the datesheet data frame(in case you want)
def map_files(dateTimeDf):
    studentDf =pd.read_excel('student_data.xlsx') #data frame to store the students data excel file
    studentDf ["PAPER CODE"] = studentDf ["PAPER CODE"].astype(str)
    dateTimeDf["UPC"] = dateTimeDf["UPC"].astype(str)
    print(len(studentDf ))
    mergedDf = pd.merge(
        dateTimeDf, studentDf , left_on=["UPC","TERM"], right_on=["PAPER CODE","TERM"], how="right"
    )

    mergedDf.to_excel("final_studentrecordrecord.xlsx")

    
dateTimeDf=processss_file(path)
map_files(dateTimeDf)
