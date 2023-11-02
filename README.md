# Kiwi Civil Calendar App -- In Progress

## What this app does:
This app allow you to easily track site photos taken on a calendar.


## Technology:
- Python 3
- Django
- GeoDjango
- HTML/CSS/SCSS
- Javascript

## Preparation for virtualenv and .env_example file:
1. Once clone or download this code, [create a virtualenv](https://docs.python.org/3/library/venv.html).
2. Acticate the virtualenv.
3. From terminal, install all the requirements with `pip install -r requirements.txt`.
4. I use [python-dotenv](https://pypi.org/project/python-dotenv/) to access environment variables.
5. rename `.env_example` to `.env`.


## Run the app:
1. From terminal, run below commands to launch the site, then go to `127.0.0.1:8000` in your browser.:
- `python manage.py migrate`
- `python manage.py runserver`



