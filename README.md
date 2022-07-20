# Django Blog

## User Stories

What I want in a blog:
Relevant content
Easy to use
Easy to sign up
Positive user experience - nice layout, good colour palette
Easy access to content

User stories are stored on Project Kanban board

The goal is to create a blog site where the primary user (me) may create blog posts. Other users may create accounts, sign in and react to those posts by way of commenting and liking, but cannot create posts themselves. As the superuser, I have full access, and will be able to delete comments.

The project is hosted on Heroku, with images served via Cloudinary

Rather than tackling deployment toward the end of the project, deployment was instead conducted early on

The blog is related to software development matters, and is called CodeStar. Accordingly, the Django app directory is called codestar

## Project set up

Install Django and Gunicorn:
`pip3 install 'django<4' gunicorn`

Install libraries needed for PostgreSQL:
`pip3 install dj_database_url psycopg2`

Install libraries needed for Cloudinary:
`pip3 install dj3-cloudinary-storage`

Create requirements.txt:
`pip3 freeze --local > requirements.txt`

Create new Django app:
`django-admin startproject codestar .`
The dot is important. 

Check that Django is installed and that the Django app was installed correctly:
`python3 manage.py runserver`

Create an app:
`python3 manage.py startapp blog`
The add 'blog' to INSTALLED_APPS in settings.py

Make database migrations:
`python3 manage.py showmigrations` to see a list of the migrations to be made
`python3 manage.py migrate --plan` to see what the migrate command will do
`python3 manage.py migrate` to commence migrations

Create Heroku project and attach postgres database

Copy DATABASE_URL to env.py
Create a SECRET_KEY in env.py, and add to Heroku config vars

Wire up database in settings.py

Migrate the databases again
This will create the tables on the Heroku postgres database
Check the Heroku database to confirm this

Set up a Cloudinary account and get API key, copy to env.py, removing "CLOUDINAY_URL=" from the beginning

Add CLOUDINARY URL and PORT to Heroku config vars. Givce PORT a value of 8000

Add DISABLE_COLLECTSTATIC to config vars
this stops Heroku from acquiring the static files (JS and CSS files) because these don't exist yet





