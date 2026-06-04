from libraries.tools.database import execute_query_add, execute_query_all

#get list of subjects
#create one course per subject for each of the past 5 years

query = "SELECT * FROM subject"
subjects = execute_query_all(query, ())

from datetime import datetime

course_count = 1

current_year = datetime.now().year
for subject in subjects:
    for year in range(current_year, current_year - 6, -1):
        query = "INSERT INTO course (course_id, year, subject_id) VALUES (?,?,?)"
        execute_query_add(query, (course_count, f"{year}", subject[0],))
        course_count += 1


