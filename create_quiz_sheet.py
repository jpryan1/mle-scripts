from canvasapi import Canvas
import datetime
from datetime import timedelta

API_URL = "https://canvas.cornell.edu"
API_KEY = ""
COURSE_NUMBER = 20583
canvas = Canvas(API_URL, API_KEY)
course = canvas.get_course(COURSE_NUMBER)

# These are kindof annoying to autogen so we hardcode, note ZULU times
# Some days there was no class, one was on Sunday, no lec 19 etc
fmt ='%Y-%m-%dT%H:%M:%SZ'

lectures = {
  "Lecture 4": datetime.datetime.strptime("2020-09-08T15:00:00Z", fmt),
  "Lecture 5": datetime.datetime.strptime("2020-09-11T01:00:00Z", fmt),
  "Lecture 6": datetime.datetime.strptime("2020-09-15T15:00:00Z", fmt),
  "Lecture 7": datetime.datetime.strptime("2020-09-18T01:00:00Z", fmt),
  "Lecture 8": datetime.datetime.strptime("2020-09-22T15:00:00Z", fmt),
  "Lecture 9": datetime.datetime.strptime("2020-09-28T01:00:00Z", fmt),
  "Lecture 10": datetime.datetime.strptime("2020-09-29T15:00:00Z", fmt),
  "Lecture 11": datetime.datetime.strptime("2020-10-02T01:00:00Z", fmt),
  "Lecture 12": datetime.datetime.strptime("2020-10-06T15:00:00Z", fmt),
  "Lecture 13": datetime.datetime.strptime("2020-10-09T01:00:00Z", fmt),
  "Lecture 14": datetime.datetime.strptime("2020-10-16T01:00:00Z", fmt),
  "Lecture 15": datetime.datetime.strptime("2020-10-20T15:00:00Z", fmt),
  "Lecture 16": datetime.datetime.strptime("2020-10-26T01:00:00Z", fmt),
  "Lecture 17": datetime.datetime.strptime("2020-10-27T15:00:00Z", fmt),
  "Lecture 18": datetime.datetime.strptime("2020-10-30T01:00:00Z", fmt),
  "Lecture 20": datetime.datetime.strptime("2020-11-06T02:00:00Z", fmt),
  "Lecture 21": datetime.datetime.strptime("2020-11-10T16:00:00Z", fmt)
}

users = course.get_users(enrollment_type=['student'])
for user in users:
  user_grades = {}  
  assignments = user.get_assignments(course)

  #First collect all grades, times into user_grades
  for assignment in assignments:
    if("Lecture" in assignment.name and "Week" not in assignment.name):
      submission = assignment.get_submission(user)
      if(submission.attempt is None):
        user_grades[assignment.name.strip()] = [False, 0]
        print(",", end=',')
      else:
        print(str(submission.score), end=',')
        dt = datetime.datetime.strptime(submission.submitted_at, '%Y-%m-%dT%H:%M:%SZ')
        print((dt-lectures[assignment.name.strip()]).total_seconds()/60, end=',')
        did_in_lec = ((dt-lectures[assignment.name.strip()]).total_seconds()/60)<=60
        user_grades[assignment.name.strip()] = [did_in_lec, submission.score]
  print('')
