## Getting your Canvas API key

In order to use the Canvas REST API, you will need an OAuth2 token. You can generate one for yourself in Canvas by going to Account>Settings>, scroll down to "Approved Integrations" and click the "+New Access Token" button.

## create_quiz_sheet

* python3 create_quiz_sheet.py > output.csv
* output contains all lecture quizzes' scores and time to completion (from start of lecture) for all students
* can be put into Quiz Report Google sheet with nice conditional formatting
* required work: insert your Canvas API key, edit Lectures dict appropriately

## post_weekly_scores

* python3 post_weekly_scores.py
* reads lecture scores, aggregates into weekly grades, posts to canvas
* by default variable ACTUALLY_POST is false, and found grades are just printed
* you **must** double check that WEEK_RANGE is only for weeks that are not yet posted, else duplicates may be made (todo, prevent this from possible happening)
* required work: insert your Canvas API key, edit Lectures dict, WEEK_RANGE and ACTUALLY_POST appropriately

## run_tests

* Requires downloading GitHub Classroom assignment repos via Classroom Assistant, download here https://classroom.github.com/assistant
* Put run_tests.sh in same directory as student submission folders, run ./run_tests.sh > test_output.txt

## get_all_scores

* python3 get_all_scores.py
* outputs csv with rows as students and columns as all grades pulled from canvas, plus comments when available
* required work: insert your Canvas API key, edit output file appropriately
