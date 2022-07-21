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


## Database diagram

The Posts mdoel / table contains all of the information about a post:
 - Title (type Char(200))
 - Author (a one-to-many relationship, since 1 author can create many posts. Authors will be pulled in from the standard Django User table)
 - Created date (using DateTime)
 - Updated date (also using DateTime)
 - The actual content(TextField)
 - Featured image or thumbnail(a Cloudinary image)
 - an excerpt or preview (TextField)
 - Number of likes (many-to-many relationship, since many users can like many posts)
 - Slug (a label that can be used as part of a URL, will be automatically generated)
 - status field (draft or published)

The Comments model / table contains information about a comment:
- post (the post that the comment is attached to, set cascade on delete so that if a post is deleted, all comments are also deleted)
- name (the name of the commenter)
- email (the email of the commenter)
- body (the comment itself)
- created_on (the date the comment was created on)
- approved (a boolean yes / no)

Once models have been created in models.py, migrate them into the database with `makemigrations` and `migrate`, using `showmigrations` as well if desired

Create a superuse so that the Django administration backend can be accessed:
`python3 manage.py createsuperuser`

Test that superuser has been created successfully:
`python3 manage.py runserver` to run the project locally
append /admin to the URL
(if not working or errors thrown, check env.py to ensure that keys are correct)

Must install a WYSIWYG / "what you see is what you get" editor for the posts
The summernote library provides this:
`pip3 install django-summernote`

Update requirements.txt with:
`pip3 freeze --local > requirements.txt`

Add 'django_summernote' to settings.py INSTALLED_APPS
In urls.py in the urlpatterns list, add a path for summernote

Create a class in admin.py to specify which fields are summernote fields

More apps have been installed, so we need to migrate again:
`python3 manage.py migrate`

Then run the project again locally, access the admin panel and go to the Add Post section
Note the superior text editor 

Additional tweaks to admin.py:

- prepopulated_fields auto generates slug lines from the title
    This will eventually help in creating unique URLs for each blog post, since slugs do not separate words with spaces, but with hyphens

- list_filter adds a box that allows posts to be filtered by the supplied criteria

- list_display adds column headers for the supplied values. These column headers can be clicked to order posts by that criteria

- search_fields adds a search box

admin.py also contains a CommentAdmin class, which functions similarly to PostAdmin, but deals with comments
This class contains an actions property, which adds a drop-down box
actions takes a list of function names in square brackets, so multiple functions can be defined
These functions must be defined within the class
As these functions are in a class, technically they are called methods


## Views

As with Flask, Django uses a base.html file to provide a unified template for each page. This has been styled with Bootstrap v5.0.1. Though the latest version is 5.2.0, I felt that the meat of this project is Django and the databases, so the look is less important

There is also a pre-made style.css file

In the index.html file, there is some funky use of the templating language, which basically limits the number of posts per row to 3. 
In the Bootstrap cards which hold each post, more templating language checks to see if the post has an image. If so, the image is injected. If not, a default placeholder image is injected instead. This ensures that every post card always has an image












