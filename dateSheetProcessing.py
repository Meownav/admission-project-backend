import pandas as pd
import pdfplumber
import numpy as np
import roman
import re
import os

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


def process_file_nep(pages,courses):
    all_tables = []

    df = pd.DataFrame(columns=["TERM", "DATE", "UPC", "TIME","COURSE"])

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
            
            if type(courses)==list:#if parameter courses is a list
                for a in courses:
                    Course=rename_course(a)
                    df.loc[len(df)] = [
                        str(roman.fromRoman(str(row[1]))),
                        np.nan,
                        row[2],
                        row[4].replace("\n", " "),  # Removing the newline char because why not.
                        Course
                    ]
            else:# if courses parameter is a single course
                if not(np.isnan(courses)):
                    Course=rename_course(courses)
                else:
                    Course=courses
                df.loc[len(df)] = [
                    str(roman.fromRoman(str(row[1]))),
                    np.nan,
                    row[2],
                    row[4].replace("\n", " "),Course
                ]
    print(df)
    return df


def extract_dates_nep(df,pages):#extracting the dates for nep datesheets only
    search_line2=re.compile(r'_______')
    counter=False
    for page in pages:
        text=page.extract_text()
        for line in text.split('\n'):
            if any(day in line.lower() for day in days) and any (month in line.lower() for month in months) and ("printed" not in line.lower()):
                a=line.split('(')
                counter=True
                date=a[0]
            elif search_line2.match(line):
                counter=False
            elif counter:
                line_split=list(line.split())
                for c in line_split:
                    if re.match(r'\d{7}',c):
                        for idx in range(len(df)):
                            if df.loc[idx,"UPC"]==c and df.loc[idx,"TERM"]==semester:
                                df.loc[idx,"DATE"]=date
                                print(df.loc[idx])
                    elif any(sem==c for sem in semesters):
                         semester =str(roman.fromRoman(c))
    print(df)
    return df

def process_file_cbcs(pages,courses):
    df = pd.DataFrame(
        columns=["TIME", "DATE", "UPC", "TERM","COURSE"]
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
                        if type(courses)==list:
                            for a in courses:
                                Course=rename_course(a)
                                row = [d, y, c, semester,Course]
                                df.loc[len(df)] = row
                                break
                        else:
                            if not(np.isnan(courses)):
                                Course=rename_course(courses)
                            else:
                                Course=courses
                            row = [d, y, c, semester,Course]
                            df.loc[len(df)] = row
                            break
                    elif any(sem == c for sem in semesters):
                        semester = str(roman.fromRoman(c))
    return df

def extract_course(pages):
    # extracting the courses for which the datesheet is designed(can be a single course or a list of courses)
    special_courses=["skillenhancementcourse","valueadditioncourses","valueadditioncourses","genericelective"]
    li=["b.sc.","b.a.","b.","com","bachelor","commerce","arts","science","(hons)","(honours)","(programme)","(prog)",",","/","skill","enhancement","ability","course","value","addition","courses","generic","elective"]
    course_continue=False
    was_bachelor=False
    was_b=False
    is_first=True
    course_str=" "
    for page in pages:
        text=page.extract_text()
        for line in text.split('\n'):
            a=line.split()
            if is_first and any (ds in line.lower() for ds in ["date sheet for","date-sheet for"]):
                d=line.split("for")
                a=d[1]
                a= d[1].split()
                print(a)
                course_continue=True
                is_first=False
            if course_continue:
                for word in a:
                    print(word)
                    if any (r in word.lower() for r in li):
                        if word.lower()=="bachelor":
                            was_bachelor=True
                        elif word.lower()=="of" and was_bachelor:
                            was_bachelor=False
                            course_str+="bachelor of"
                        elif word.lower()=="of" and was_bachelor==False:
                            course_continue=False
                            break
                        elif word.lower()=="b.":
                            was_b=True
                        elif word.lower()=="com" and was_b:
                            was_b=False
                            course_str+="b. com"
                        elif word.lower()=="com" and was_b==False:
                            course_continue=False
                            break
                        else:
                            course_str+=word
                    else:
                        course_continue=False
                        break
    print(course_str)
    without_space="".join(course_str.split())
    if any(sub in without_space.lower() for sub in special_courses):
        diff_courses=np.nan
    elif "/" in course_str:
        diff_courses=course_str.split("/")
    elif "," in course_str:
        diff_courses=list(course_str.split(","))
    else:
        diff_courses=course_str
    
    return diff_courses

def rename_course(course):
    # the course names extracted from datesheet is not like those present in student data hence this function rename the courses present in datesheet dataframe
    str=""
    course="".join(course.split())
    if any(sub in course.lower() for sub in["bachelorofarts","b.a."]):
        str+="bachelorofarts"
    elif any(sub in course.lower() for sub in["bachelorofcommerce","b.com."]):
        str+="bachelorofcommerce"
    elif any(sub in course.lower() for sub in["bachelorofscience","b.sc."]):
        str+="bachelorofscience"
    if any(sub in course.lower() for sub in["honors","hons"]):
        str+="(honourscourse)"
        
    return str
def process_file(datesheetPath):
    pdf = pdfplumber.open(datesheetPath)
    pages = pdf.pages
    text = ""

    for page in pages:
        text += page.extract_text()
    courses=extract_course(pages)
    # courses=rename_course(courses)
    if "CBCS-LOCF" in text.upper():
        print("CBCS")
        return process_file_cbcs(pages,courses)
    elif "NEP-UGCF" in text.upper():
        df=process_file_nep(pages,courses)
        return extract_dates_nep(df,pages)
    else:
        print("Some error occurred while processing.")


def split_ProgrammeName(DF):
    #in student data,courses are like bsc(H) physics but we are only concerned about course i.e.bsc(H) not domain physics
    DF["Programme Name"] = DF["Programme Name"].astype(str)
    for idx in range(len(DF)):
        if "master of arts" in DF.loc[idx,"Programme Name"].lower():
            DF.loc[idx,"Course"]="masterofarts"
        elif "master of science" in DF.loc[idx,"Programme Name"].lower():
            DF.loc[idx,"Course"]="masterofscience"
        elif "honours course" in DF.loc[idx,"Programme Name"].lower():
            DF.loc[idx,"Course"]="".join((str.split(DF.loc[idx,"Programme Name"],")")[0]+")").split()).lower()
        else:
            DF.loc[idx,"Course"]="".join(DF.loc[idx,"Programme Name"].split()).lower()
    return DF

def add_columns(DF):# these columns will be used at the time of printing of examination schedule
    abbrevations={
    "Master of Arts (English)":"M.A. English",
    "Master of Science (Mathematics)":"MSc. Maths",
    "Bachelor of Arts (Honours Course) Economics":"B.A. (Hons.) Eco",
    "Bachelor of Arts (Honours Course) Geography":"B.A. (Hons.) Geo",
    "Bachelor of Arts (Honours Course) History":"B.A. (Hons.) History",
    "Bachelor of Arts (Honours Course) (Philosophy)":"B.A. (Hons.) Philosophy",
    "Bachelor of Arts (Honours Course) (Political Science)":"B.A. (Hons.) Pol Sci",
    "Bachelor of Arts (Honours Course) Punjabi":"B.A. (Hons.) Pjb",
    "Bachelor of Arts (Honours Course) (Sanskrit)":"B.A. (Hons.) Skt",
    "Bachelor of Arts (Honours Course) (Urdu)":"B.A. (Hons.) Urd",
    "Bachelor of Arts (Honours Course) English":"B.A. (Hons.) Eco",
    "Bachelor of Commerce":"Bcom",
    "Bachelor of Science (Honours Course) Botany":"BSc (Hons.) Bot",
    "Bachelor of Science (Honours Course) Chemistry":"BSc (Hons.) Chm",
    "Bachelor of Science (Honours Course) Computer Science":"BSc (Hons.) CS",
    "Bachelor of Commerce (Honours Course)":"Bcom (Hons.)", 
    "Bachelor of Science (Honours Course) Mathematics":"BSc (Hons.) Maths",
    "Bachelor of Science (Honours Course) Physics":"BSc (Hons.) Phy",
    "Bachelor of Science (Honours Course) Zoology":"BSc (Hons.) Zoo",
    "Bachelor of Arts (Honours Course) Hindi":"BA (Hons) hindi",
    "Bachelor of Arts":"BA",
    "Bachelor of Science (Life Sciences)":"Bsc Life Sci",
    "Bachelor of Science (Physical Sciences)":"BSc. Phy Sci"}
    DF["Programme Name"]=DF["Programme Name"].astype(str)
    for idx in range(len(DF)):
        for a in abbrevations:
            if a==DF.loc[idx,"Programme Name"]:
                DF.loc[idx,"Short Form"]=abbrevations[a]
    DF["col1"]=DF["Short Form"].astype(str)+"-"+DF["Paper Term"].astype(str)+"-SMT"
    DF["col2"]=DF["Paper Code"].astype(str)+" "+DF["Paper Name"].astype(str)
    return DF
        

def map_files(dateTimeDf):
    print(dateTimeDf)
    # if not os.path.exists("Data\InternalData\DatesheetResult.xlsx"):
    #     DF=pd.read_excel("Data/InternalData/Data.xlsx")
    studentDf = (
        pd.read_excel("Data/InternalData/Data.xlsx")
        if not os.path.exists("Data\InternalData\DatesheetResult.xlsx")
        else pd.read_excel("Data\InternalData\DatesheetResult.xlsx")
    )

    # data frame to store the students data excel file
    studentDf["Paper Code"] = studentDf["Paper Code"].astype(str)
    dateTimeDf["UPC"] = dateTimeDf["UPC"].astype(str)

    # First time
    if not any(column in ["TIME", "DATE"] for column in studentDf.columns):
        studentDf=add_columns(split_ProgrammeName(studentDf))
        studentDf["Course"]=studentDf["Course"].astype(str)
        studentDf["TIME"] = [" " for _ in range(len(studentDf))]
        studentDf["DATE"] = [" " for _ in range(len(studentDf))]
        for studentIdx in range(len(studentDf)):
            for dateIdx in range(len(dateTimeDf)):
                if (
                    studentDf.loc[studentIdx, "Paper Code"]
                    == dateTimeDf.loc[dateIdx, "UPC"]
                ) and (
                    studentDf.loc[studentIdx, "Paper Term"] == dateTimeDf.loc[dateIdx, "TERM"]
                ) and ((np.isnan(dateTimeDf.loc[dateIdx,"COURSE"]))
                       or(studentDf.loc[studentIdx,"Course"]==dateTimeDf.loc[dateIdx,"COURSE"]) 
                       ):
                    studentDf.loc[studentIdx, "TIME"] = dateTimeDf.loc[dateIdx, "TIME"]
                    studentDf.loc[studentIdx, "DATE"] = dateTimeDf.loc[dateIdx, "DATE"]
            if studentIdx % 100 == 0:
                print(studentIdx)
        studentDf.to_excel("Data/InternalData/DatesheetResult.xlsx", index=False)
    # Second time onwards
    else:
        studentDf["Course"]=studentDf["Course"].astype(str)
        for studentIdx in range(len(studentDf)):
            for dateIdx in range(len(dateTimeDf)):
                # If paper code matches with upc code and term of excel file matches with term of df.
                if (
                    studentDf.loc[studentIdx, "Paper Code"]
                    == dateTimeDf.loc[dateIdx, "UPC"]
                ) and (
                    studentDf.loc[studentIdx, "Paper Term"] == dateTimeDf.loc[dateIdx, "TERM"]
                )and ((np.isnan(dateTimeDf.loc[dateIdx,"COURSE"]))
                       or(studentDf.loc[studentIdx,"Course"]==dateTimeDf.loc[dateIdx,"COURSE"]) 
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

