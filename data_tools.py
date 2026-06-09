# from libraries.tools.database import execute_query_add, execute_query_all
#
# #get list of subjects
# #create one course per subject for each of the past 5 years
#
# # query = "SELECT * FROM subject"
# # subjects = execute_query_all(query, ())
# #
# # from datetime import datetime
# #
# # course_count = 1
# #
# # current_year = datetime.now().year
# # for subject in subjects:
# #     for year in range(current_year, current_year - 6, -1):
# #         query = "INSERT INTO course (course_id, year, subject_id) VALUES (?,?,?)"
# #         execute_query_add(query, (course_count, f"{year}", subject[0],))
# #         course_count += 1
#
# query = "INSERT INTO room (department_id) VALUES (?)"
#
# from libraries.tools.database import execute_query_add
#
# for d in range(1, 6):
#     for i in range(5):
#         execute_query_add(query, (d, ))
#
