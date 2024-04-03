steps to run this project

1. get into the root directory where run.py file is located
2. python3 -m venv venv (create a virtual environment)
3. source venv/bin/activate (activate the newly created environment)
4. pip install -r requirements.txt install all required libraries in activated environment
5. update variables in blog/constants.py file if you want
6. flask --app run.py db init (to initialize db)
7. flask --app run.py db migrate (to create initial tables)
8. flask --app run.py db upgrade (to apply migrations)
9. python3 run.py (run the project)

# My-Projects
