import re
import pandas as pd
import pdfplumber
import numpy as np

df = pd.DataFrame(columns=['TIME', 'DATE','UPC'])#data frame to store time,upc,date 
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
                        row=[d,y,c]
                        df.loc[len(df)]=row
def read_df():
    print(df.head())
#     df.to_csv('datesheet_dataframe.csv',index=False)  #to download the csv file of the datesheet data frame(in case you want)
def map_files():   #yhi hai vo function jo kaam nhi kr rha sad:(
    data=pd.read_excel('student_data.xlsx')#data frame to store the students data excel file
#     data['TIME OF EXAM']=np.nan  #insert empty column time of exam in data frame 'data'
#     data['DATE OF EXAM']=np.nan
    for a in range(len(data)):
        for b in range(len(df)):
            upc=df['UPC'][b]
            t=df['TIME'][b]
            data.loc[data["PAPER CODE"]==upc,"TIME OF EXAM"]=t
#             if data['PAPER CODE'][a]==df['UPC'][b]:
#                  data['TIME OF EXAM'][a]=df['TIME'][b]
#                  data['DATE OF EXAM'][a]=df['DATE'][b]
    print(data.head())
#     data.to_csv('final_studentrecord.csv',index=False)

    
processss_file(path)
read_df() 
map_files()