import gin
import numpy as np
import pandas as pd
import pdfplumber
import tabula

from IMP_utils_py.config.logging import setup_logger

### logging setup
logger = setup_logger()

@gin.configurable
class GradeCalculator:

    def __init__(self, file_path: str):
        self.df_exams = self.extract_exams(file_path)
        self.df_modules = self.extract_modules(file_path)
    
    def get_text_no_tables_pdf(self, file_path: str) -> str:
        """ function to get text of pdf file with skipping tables"""

        def not_within_bboxes(obj):
            """Check if the object is in any of the table's bbox."""
            def obj_in_bbox(_bbox):
                """See https://github.com/jsvine/pdfplumber/blob/stable/pdfplumber/table.py#L404"""
                v_mid = (obj["top"] + obj["bottom"]) / 2
                h_mid = (obj["x0"] + obj["x1"]) / 2
                x0, top, x1, bottom = _bbox
                return (h_mid >= x0) and (h_mid < x1) and (v_mid >= top) and (v_mid < bottom)

            return not any(obj_in_bbox(__bbox) for __bbox in bboxes)
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    # Get the bounding boxes of the tables on the page.
                    bboxes = [
                        table.bbox
                        for table in page.find_tables(
                            table_settings={
                                "vertical_strategy": "explicit",
                                "horizontal_strategy": "explicit",
                                "explicit_vertical_lines": page.curves + page.edges,
                                "explicit_horizontal_lines": page.curves + page.edges,
                            }
                        )
                    ]

                    text += page.filter(not_within_bboxes).extract_text()
            
            return text
        except ValueError as e:
            return ""
        
    def extract_exams(self, file_path: str) -> pd.DataFrame:
        """ extract all passed exams (marked with 'MP' and 'BE' in Leistungsspiegel) """
        txt = self.get_text_no_tables_pdf(file_path)
        if txt == "":
            logger.warning("no exams detected")
            return pd.DataFrame({"ID": [], "name": [], "grade": []})

        lines = txt.split("\n")
        subject_names = []
        subject_numbers = []
        grades = []
        # get exam names + grades
        for line in lines:
            # all exams
            if " MP " in line:
                # all passed exam
                if " BE " in line:
                    subject_name = line.split("... ")[0].replace(".", "")
                    grade = float(line.split(" MP BE ")[1].split(" ")[0].replace(",", "."))
                    grades.append(grade)
                    subject_numbers.append(subject_name.split(" ")[0])
                    subject_names.append(" ".join(subject_name.split(" ")[1:]))

        return pd.DataFrame({"ID": subject_numbers, "name": subject_names, "grade": grades})
    
    def extract_modules(self, file_path: str) -> pd.DataFrame:
        """ extract all module header with 'Modulnote' and 'Modulpunkte' """
        tables = tabula.read_pdf(file_path, pages="all", silent=True)
        names = []
        grades = []
        credits = []
        for table in tables:
            name_col = list(table[table.columns[1:2][0]])
            for name in name_col:
                if "Modulpunkte" in name and "Modulnote" in name:
                    names.append(str(name.split(" Modulnote")[0]))
                    grades.append(float(name.split("Modulnote: ")[1].split(" ")[0].replace(",", ".")))
                    credits.append(int(name.split("Modulpunkte: ")[1].split(" ")[0]))
        
        return pd.DataFrame({"name": names, "grade": grades, "credit": credits})
    
    def modules_exams_diff(self, drop_idx: list):
        logger.info("calculation infos:")
        print()
        print("using the following modules for calculation:")
        print()
        print(self.df_modules.drop(index=drop_idx, inplace=False).to_markdown(index=False))
        if drop_idx:
            print("\n\n")
            print("not using the following modules because of Studienordnung IMP:")
            print()
            print(self.df_modules.iloc[drop_idx].to_markdown(index=False))
        print("\n\n")
        print("not using the following exams because of missing credits:")
        print()

        not_idx = [idx for idx in range(len(self.df_exams)) if not self.df_exams.name.iloc[idx] in list(self.df_modules.name)]
        if not_idx:
            print(self.df_exams.iloc[not_idx].to_markdown(index=False))
        else:
            print("--- no such exam detected ---")
        print()

    def get_better_LinA_Ana_result(self) -> list:
        """ 
        get better result if both are present from:
        - 'Lineare Algebra und Analytische Geometrie I' and 'Lineare Algebra und Analytische Geometrie II'
        - 'Analysis I' and 'Analysis II'

        @return: list with idx of result that will not be used for calculation
        """
        LinA = [10,10]
        LinA_idx = [None, None]
        Ana = [10,10]
        Ana_idx = [None, None]
        for idx in range(len(self.df_modules)):
            if self.df_modules.name.iloc[idx] == "Lineare Algebra und Analytische Geometrie I":
                LinA[0] = self.df_modules.grade.iloc[idx]
                LinA_idx[0] = idx
            elif self.df_modules.name.iloc[idx] == "Lineare Algebra und Analytische Geometrie II":
                LinA[1] = self.df_modules.grade.iloc[idx]
                LinA_idx[1] = idx
            elif self.df_modules.name.iloc[idx] == "Analysis I":
                Ana[0] = self.df_modules.grade.iloc[idx]
                Ana_idx[0] = idx
            elif self.df_modules.name.iloc[idx] == "Analysis II":
                Ana[1] = self.df_modules.grade.iloc[idx]
                Ana_idx[1] = idx

        drop_idx = []
        if sum(LinA) < 10:
            drop_idx.append(LinA_idx[np.argmax(LinA)])
        if sum(Ana) < 10:
            drop_idx.append(Ana_idx[np.argmax(Ana)])
        return drop_idx
    
    def calculate_total_grade(self, IMP: bool) -> float:
        """ 
        calculates grade with weighted by credits average of 'Modulnote' 

        @param:
            IMP: if True, only the better result of (LinA I and LinA II) and (Ana I and Ana II) will be used
        """
        drop_idx = []
        if IMP:
            drop_idx = self.get_better_LinA_Ana_result()
        self.modules_exams_diff(drop_idx)
        total_credits = sum(self.df_modules.drop(index=drop_idx, inplace=False).credit)
        total_product = sum([self.df_modules.grade.iloc[idx] * self.df_modules.credit.iloc[idx] for idx in range(len(self.df_modules)) if idx not in drop_idx])
        final_grade = total_product/total_credits
        logger.info(f"final grade: {final_grade}")
        return final_grade
