import re
from PyPDF2 import PdfReader

sourceFile = "C:/Users/coolm/Downloads/datesheet.pdf"
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


def getText(sourceFile):
    reader = PdfReader(sourceFile)
    print("Num Pages:", len(reader.pages))

    fullText = ""

    for i in range(len(reader.pages)):
        # print("Page:", i)
        page = reader.pages[i]
        fullText += page.extract_text()
    return fullText


def get_core_subjects(fullText):
    # get core subjects starting with CORE SUBJECT and ending with a dot(.)
    core_subjects = re.search(r"CORE  SUBJECT  :- (.*?)\s*\.", fullText, re.DOTALL)

    core_subjects = core_subjects.group(1).strip().split(",") if core_subjects else []

    for i in range(len(core_subjects)):
        core_subjects[i] = core_subjects[i].strip()
    return core_subjects


def get_dates(fullText):
    dates = []
    lines = fullText.split("\n")
    for line in lines:
        for month in months:
            for day in days:
                if (
                    (month in line)
                    and (day.lower() in line.lower())
                    and ("printed" not in line.lower())  # extra data
                ):
                    dates.append(line.strip().lower())

    return dates


# def get_subjects(fullText, dates):
#     table = {}
#     lines = fullText.split("\n")

#     for date in dates:
#         table[date] = []

#     try:
#         for dateIdx, date in enumerate(dates):
#             for lineIdx, line in enumerate(lines):
#                 if date.lower() in line.lower():
#                     curLineIdx = lineIdx + 1  # Start from the next line after the date

#                     # Extract subject information until an empty line is encountered
#                     while curLineIdx < len(lines) and lines[curLineIdx].strip() != "":
#                         subject_info = lines[curLineIdx].strip().split()
#                         if len(subject_info) >= 4:
#                             if (
#                                 (
#                                     subject_info[0].lower() == "biomedical"
#                                     and subject_info[1].lower() == "science"
#                                 )
#                                 or (
#                                     subject_info[0].lower() == "computer"
#                                     and subject_info[1].lower() == "science"
#                                 )
#                                 or (
#                                     subject_info[0].lower() == "electronics"
#                                     and subject_info[1].lower() == "science"
#                                 )
#                                 or (
#                                     subject_info[0].lower() == "food"
#                                     and subject_info[1].lower() == "technology"
#                                 )
#                                 or (
#                                     subject_info[0].lower() == "home"
#                                     and subject_info[1].lower() == "science"
#                                 )
#                                 or (
#                                     subject_info[0].lower() == "environmental"
#                                     and subject_info[1].lower() == "science"
#                                 )
#                                 or (
#                                     subject_info[0].lower() == "polymer"
#                                     and subject_info[1].lower() == "science"
#                                 )
#                             ):
#                                 subject = {
#                                     "subject": subject_info[0] + " " + subject_info[1],
#                                     "semester": subject_info[2],
#                                     "paper_code": subject_info[3],
#                                     "paper_name": " ".join(subject_info[4:]),
#                                 }
#                             else:
#                                 subject = {
#                                     "subject": subject_info[0],
#                                     "semester": subject_info[1],
#                                     "paper_code": subject_info[2],
#                                     "paper_name": " ".join(subject_info[3:]),
#                                 }
#                             print("Date\n", date)
#                             print("Subject\n", subject)
#                             table[date].append(subject)
#                         curLineIdx += 1

#     except IndexError:
#         pass

#     return table


def get_subjects(fullText, dates):
    table = {}

    for date in dates:
        table[date] = []

    lines = fullText.split("\n")

    try:
        current_date = None  # Variable to track the current date

        for lineIdx, line in enumerate(lines):
            # Check if the line contains any of the dates
            if any(date.lower() in line.lower() for date in dates):
                for date in dates:
                    if date.lower() in line.lower():
                        current_date = date  # Set the current date
                        break

            # Extract subject information if the line contains relevant data
            if current_date is not None and line.strip() != "":
                subject_info = line.strip().split()

                if len(subject_info) >= 4:
                    if (
                        (
                            subject_info[0].lower() == "biomedical"
                            and subject_info[1].lower() == "science"
                        )
                        or (
                            subject_info[0].lower() == "computer"
                            and subject_info[1].lower() == "science"
                        )
                        or (
                            subject_info[0].lower() == "electronics"
                            and subject_info[1].lower() == "science"
                        )
                        or (
                            subject_info[0].lower() == "food"
                            and subject_info[1].lower() == "technology"
                        )
                        or (
                            subject_info[0].lower() == "home"
                            and subject_info[1].lower() == "science"
                        )
                        or (
                            subject_info[0].lower() == "environmental"
                            and subject_info[1].lower() == "science"
                        )
                        or (
                            subject_info[0].lower() == "polymer"
                            and subject_info[1].lower() == "science"
                        )
                    ):
                        subject = {
                            "subject": subject_info[0] + " " + subject_info[1],
                            "semester": subject_info[2],
                            "paper_code": subject_info[3],
                            "paper_name": " ".join(subject_info[4:]),
                        }
                    else:
                        subject = {
                            "subject": subject_info[0],
                            "semester": subject_info[1],
                            "paper_code": subject_info[2],
                            "paper_name": " ".join(subject_info[3:]),
                        }

                    table[current_date].append(subject)

            # Reset the current date if an empty line is encountered
            if line.strip() == "":
                current_date = None

    except IndexError:
        pass

    return table


fullText = getText(sourceFile)
CORE_SUBJECTS = get_core_subjects(fullText)
dates = get_dates(fullText)
subjects_table = get_subjects(fullText, dates)

# print(dates)
for i in dates:
    print(i)
    for j in subjects_table[i]:
        print(j)
