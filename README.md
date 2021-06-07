## Software Trainee Project by Bonface Mwicwiri

This system has two users the admin and applicant. It uses Custom User models for authentication
admin is able to:
1. Add a micro task 
2. Post job
3. View registered applicants.
4. view applicants profile.
5. view Feedback
6. Receive feedback via email

Applicant is able to:
1. Register
2. Apply for a job
3. view applied jobs
4. send feedback
5. update their profile

The system is uses memcache as cache back-end. the system also allows users to change and reset passwords.
the system uses ajax to submit forms asynchronously.

instructions:
create virtual environment
run:
`pip install -r requirements.txt`
configure a personal gmail for sending emails and then allow less secure apps in gmail account.
after that you can run: `python manage.py runserver`

below is the link to the hosted project:
https://varaltrainee.pythonanywhere.com/
