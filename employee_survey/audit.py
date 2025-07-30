import csv
from datetime import datetime

def log_audit(username, action):
    with open('submissions_audit.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), username, action])

def save_survey_to_csv(survey, username):
    with open('survey_responses.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now(),
            username,
            survey.department,
            survey.age,
            survey.gender,
            survey.rating,
            survey.job_satisfaction,
            survey.work_life_balance,
            survey.comments,
            survey.suggestions
        ])
