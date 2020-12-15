from canvasapi import Canvas
import datetime
import pandas as pd
from datetime import timedelta

# Canvas API URL
API_URL = "https://canvas.cornell.edu"
# Canvas API key
API_KEY = ""
# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)
course = canvas.get_course(20583)
users = course.get_users(enrollment_type=['student'])

grades_dict = {}
column_names = []

for user in users:
  assignments = user.get_assignments(course)
  for assignment in assignments:
    column_names.append(assignment.name+" overall score")
    if "rubric" in dir(assignment):
      for item in assignment.rubric:
        column_names.append(assignment.name+" "+item["description"])
        column_names.append(assignment.name+" grader comment for "+item["description"])
  break

for user in users:
  assignments = user.get_assignments(course)
  student_grades = []
  for assignment in assignments:
    submission = assignment.get_submission(user, include=['rubric_assessment'])
    student_grades.append(submission.score)
    if "rubric" in dir(assignment):
      if("rubric_assessment" in dir(submission) and submission.score != 0):
        assessment = submission.rubric_assessment
        for rubric_item in assessment.values():
          if "points" in rubric_item:
            student_grades.append(rubric_item["points"])
          else:
            student_grades.append(0)
          if "comments" in rubric_item:
            student_grades.append(rubric_item["comments"])
          else:
            student_grades.append("")
      else:
        for item in assignment.rubric:
          student_grades.append(0)
          student_grades.append("")

  grades_dict[user.name] = student_grades
    # print(assignment.points_possible)

df = pd.DataFrame.from_dict(grades_dict, orient='index',
                       columns=column_names)
df.to_csv("grades_df.csv")
