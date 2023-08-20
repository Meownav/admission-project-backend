import os
import time

import pandas as pd


mappings = {
    22510: "BA(H)EC",
    22511: "BA(H)EN",
    22513: "BA(H)GR",
    22516: "BA(H)HN",
    22518: "BA(H)HS",
    22526: "BA(H)PH",
    22527: "BA(H)PS",
    22524: "BA(H)PU",
    22529: "BA(H)SK",
    22533: "BA(H)UR",
    22501: "BAPR",
    22503: "BCOM",
    22504: "BCOM(H)",
    22556: "BSC(H)BT",
    22557: "BSC(H)CH",
    22570: "BSC(H)CS",
    22563: "BSC(H)MT",
    22567: "BSC(H)PH",
    22569: "BSC(H)ZL",
    22583: "BScLSc",
    22582: "BscPhySc",
}

# def create_course_master(src_path, dest_dir):
#     src_df = pd.read_excel(src_path, engine='openpyxl')

#     unique_pcode_names = src_df.drop_duplicates(subset=["Programme Code"])

#     unique_pcode_names["Course"] = unique_pcode_names["Programme Code"].map(mappings)

#     course_master_df = unique_pcode_names[["Programme Code", "Programme Name", "Course"]].sort_values(by="Programme Code").reset_index(drop=True)

#     with pd.ExcelWriter(os.path.join(dest_dir, "new_student_data_course_master.xlsx"), engine='openpyxl') as writer:
#         src_df.to_excel(writer, sheet_name="student_data", index=False)
#         course_master_df.to_excel(writer, sheet_name="course_master", index=False)


def create_course_master(src_path, dest_dir):
    # print("1st function.")
    src_df = pd.read_excel(src_path)
    unique_pcode_names = src_df.drop_duplicates(subset=["Programme Code"])[
        ["Programme Code", "Programme Name"]
    ]

    course_master_df = unique_pcode_names.sort_values(by="Programme Code").reset_index(
        drop=True
    )

    course_master_df["Course"] = course_master_df["Programme Code"].replace(mappings)

    with pd.ExcelWriter(
        os.path.join(dest_dir, "new_student_data_course_master.xlsx")
    ) as writer:
        src_df.to_excel(writer, sheet_name="student_data", index=False)
        course_master_df.to_excel(writer, sheet_name="course_master", index=False)


# src_path here should be the path to the course master file.
# This will add a new sheet to the same excel file.
def create_subject_master(src_path):
    with pd.ExcelWriter(
        src_path, engine="openpyxl", mode="a", if_sheet_exists="overlay"
    ) as writer:
        # print("2nd function.")
        src_df = pd.read_excel(src_path)
        subject_master_df = src_df[
            [
                "Exam Roll Number",
                "Address",
                "Programme Code",
                "Programme Name",
                "Current Semester Term",
                "Paper Term",
                "Paper Code",
                "Paper Name",
                "Paper Type",
            ]
        ].reset_index(drop=True)

        subject_master_df["Course"] = subject_master_df["Programme Code"].replace(
            mappings
        )
        subject_master_df["Exam Roll No."] = subject_master_df["Exam Roll Number"]
        subject_master_df["CSMT"] = (
            subject_master_df["Course"].astype(str)
            + "-"
            + subject_master_df["Paper Term"].astype(str)
            + "-SMT"
        )
        subject_master_df["Subject"] = (
            subject_master_df["Paper Code"].astype(str)
            + "-"
            + subject_master_df["Paper Type"]
            + "-"
            + subject_master_df["Paper Name"].astype(str)
        )

        subject_master_df.to_excel(writer, sheet_name="subject_master", index=False)


# src_path here should be the path to the subject_master file.
# This will add a new sheet to the same file.
def create_date_master(src_path):
    with pd.ExcelWriter(
        src_path, engine="openpyxl", mode="a", if_sheet_exists="overlay"
    ) as writer:
        # print("3rd function.")
        subject_master_df = pd.read_excel(src_path, sheet_name="subject_master")
        cur_sem_col = subject_master_df["CSMT"]
        subject_col = subject_master_df["Subject"]

        course_subject = (
            cur_sem_col.astype(str) + " - " + subject_col.astype(str)
        ).unique()

        date_master_df = pd.DataFrame(
            {
                "Course/Subject": course_subject,  # Get the unique courses
                "Date": [None for _ in range(len(course_subject))],
                "Time": [None for _ in range(len(course_subject))],
            }
        )
        date_master_df.to_excel(writer, sheet_name="date_master", index=False)


# src_path here should be the path to the file.
def map_dates(src_path):
    with pd.ExcelWriter(
        src_path, engine="openpyxl", mode="a", if_sheet_exists="overlay"
    ) as writer:
        date_master_df = pd.read_excel(src_path, sheet_name="date_master")
        subject_master_df = pd.read_excel(src_path, sheet_name="subject_master")

        date_master_df["key"] = date_master_df["Course/Subject"]
        subject_master_df["key"] = (
            subject_master_df["CSMT"] + " - " + subject_master_df["Subject"]
        )

        merged_df = subject_master_df.merge(
            date_master_df[["key", "Date", "Time"]], on="key", how="left"
        )

        merged_df.drop(columns=["key"], inplace=True)

        merged_df.to_excel(writer, sheet_name="subject_master", index=False)
