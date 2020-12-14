from canvasapi import Canvas
import datetime
from datetime import timedelta

# Canvas API URL
API_URL = "https://canvas.cornell.edu"
# Canvas API key
API_KEY = ""
# Initialize a new Canvas object

canvas = Canvas(API_URL, API_KEY)

WEEK_RANGE = range(8,10)
ACTUALLY_POST=False
course = canvas.get_course(20583)
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
  "Lecture 21": datetime.datetime.strptime("2020-11-10T16:00:00Z", fmt),
  "Lecture 22": datetime.datetime.strptime("2020-11-16T2:00:00Z", fmt),
  "Lecture 23": datetime.datetime.strptime("2020-11-20T2:00:00Z", fmt),
  "Lecture 24": datetime.datetime.strptime("2020-11-24T16:00:00Z", fmt),
  "Lecture 25": datetime.datetime.strptime("2020-12-01T16:00:00Z", fmt)
}


weekly_lectures =[
  ["4", "5"],
  ["6", "7"],
  ["8", "9"],
  ["10", "11"],
  ["12", "13"],
  ["14", "15"],
  ["16", "17"],
  ["18", "20"],
  ["21", "22"],
  ["23", "24"]
]

if(ACTUALLY_POST):
  for week in WEEK_RANGE:
    new_assignment = course.create_assignment({
        'name': 'Week '+str(week)+' Lecture Quizzes',
        'points_possible': 10,
        'published': True})

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
      else:
        dt = datetime.datetime.strptime(submission.submitted_at, '%Y-%m-%dT%H:%M:%SZ')
        did_in_lec = ((dt-lectures[assignment.name.strip()]).total_seconds()/60)<=60
        user_grades[assignment.name.strip()] = [did_in_lec, submission.score]
  # Now go through and apply lecture quiz rubric for grade
  for week in WEEK_RANGE:
    did_one_in_lec = False
    total_score = 0
    for day in weekly_lectures[week-1]:
      lec_name = "Lecture "+day
      did_one_in_lec = (user_grades[lec_name][0] or did_one_in_lec)
      total_score += user_grades[lec_name][1]

    week_grade = 0
    if(did_one_in_lec and total_score>=10):
      week_grade=10
    elif(total_score>0):
      week_grade=5
    print(user.name + " week "+str(week)+ " grade ", week_grade)
    if(ACTUALLY_POST):
      for assignment in assignments:
        if(assignment.name == 'Week '+str(week)+' Lecture Quizzes'):
          sub = assignment.get_submission(user)
          sub.edit(submission={"posted_grade":week_grade})
