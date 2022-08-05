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


## All Auth

Install Django AllAuth:
`pip3 install django-allauth`

update requirements.txt:
`pip3 freeze --local > requirements.txt`

Add allauth to codestar/urls.py
Add allauth to INSTALLED_APPS in settings.py

Then migrate:
`python3 manage.py migrate`

Run server to confirm:
`python3 manage.py runserver`

Allauth provides templates for sign-up, log-in and log-out
These may be accessed without said files in repository by appending /accounts/signup to the URL
These are not pretty, but may be customised later
In base.html, update anchor hrefs with URLs - {% url 'account_logout' %}, {% url 'account_login' %}, {% url 'account_signup' %}

### Modifying Allauth templates

Determine what version of Python the project is using:
`ls ../.pip-modules/lib`
Probably Python 3.8
This indicates the directory where all of the modules and libraries that have been installed are located
This is above the workspace in the directory structure

Then copy the allauth templates into the templates folder, so that we can modify them:
`cp -r ../.pip-modules/lib/python3.8/site-packages/allauth/templates/* ./templates`
cp -r is the command to copy recursively, so that any directories are included
Then we specify the file path to the templates
This is why we needed to determine the python version number
The ./templates is the paste location - the templates folder

This should copy and paste the account, openid, socialaccount and tests folders into templates. The account folder is the one we are interested in, since that is where the signin, login and logout templates are located, along with many other HTML files that deal with accounts

Note that Allauth supplies a base.html file itself, and all of the other HTML files have templating statements that extend this base. The intention is, I suppose, to use those templates from project start. So, delete account/ from these extends statements

One thing to note is that these files have a tab indentation width of 2. By default, this will override global gitpod settings, so I have unchecked this option to make a tab indentation of 4 the standard


## Commenting

The model for comments already exists, and they can be approved/disapproved in the admin panel

Formatting forms can be tricky, so Django Crispy Forms will be used to help

Install Crispy forms:
`pip3 install django-crispy-forms`

Update requirements.txt:
`pip3 freeze --local > requirements.txt`

Add crispy_forms to settings.py INSTALLED_APPS

Instruct Crispy to use bootstrap classes by adding CRISPY_TEMPLATE_PACK = 'bootstrap4'
This project uses Bootstrap5, but Crispy does not yet have a compatibility pack for Bootstrap5
However, forms formatting should not require many of the weird features of Bootstrap, so there should be no issue

Create a forms.py file in the blog directory
Import comments model from models.py and the forms base from django

Now create the view for the comment

Import the CommentForm class into views.py, and add "comment_form": CommentForm() to the return render 

The add the form elements to post_detail, being sure to include {{ comment_form | crispy }}

This actually renders the form. Only the body CharField is rendered, because that is what we have specified in the CommentForm class in forms.py, which is then imported into views.py for rendering in the return render statement

This renders the form, but it won't actually work

To make it work, there needs to be a POST method in the PostDetail class in views.py

The code in views.py and post_detail.html means that comments are not automatically displayed, and must be approved in the django admin panel. Login to that, go to comments and then approve the comment. When the site is viewed again, the comment will display

## Likes

To enable likes, a new view is needed - create the code, create the template and wire up the URL


## Messages

Django has the capacity to issue messages to users when actions are performed

Add:
`from django.contrib.messages import constants as messages`
to settings.py

Add a MESSAGE_TAGS variable as a dictionary. This assigns various message types to bootstrap classes, so that the colour of the message will change depending on the type of message

A message display element can be added to base.html. This goes above the main element that holds injected block content


### Challenge

Add code to views.py to flash a message when a user leave a comment
"comment_posted": True 
has been added to return render statements, to be used much like "commented": True is used to display the submission / approval message 


## Final deployment

The DEBUG variable must be set to False in settings.py

Add:
X_FRAME_OPTIONS = 'SAMEORIGIN'
just below DEBUG
This will allow the use of summernote in the admin panel of the deployed version

On Heroku, remove the DISABLE_COLLECTSTATIC config var, or set it to 0








