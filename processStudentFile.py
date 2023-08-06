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


def create_course_master(src_path, dest_dir):
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
def create_subject_master(src_path, dest_dir):
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

    course_master_df = pd.read_excel(src_path, sheet_name="course_master")

    print(course_master_df)

    subject_master_df["Course"] = course_master_df["Programme Code"].replace(mappings)


    # print(
    #     subject_master_df[
    #         ["Course", "Programme Code", "Programme Name", "Exam Roll Number"]
    #     ]
    # )

    # src_file = pd.ExcelFile(src_path)

    # with pd.ExcelFile(src_path) as course_master_file:
    #     all_sheets = course_master_file.sheet_names

    #     with pd.ExcelWriter(
    #         os.path.join(dest_dir, "new_student_data_subject_master.xlsx")
    #     ) as writer:
    #         for sheet_name in src_file.sheet_names:
    #             df_original = pd.read_excel(src_file, sheet_name=sheet_name)
    #             df_original.to_excel(writer, sheet_name=sheet_name, index=False)

    #         subject_master_df.to_excel(writer, sheet_name="subject_master", index=False)
