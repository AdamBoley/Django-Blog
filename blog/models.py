from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.

STATUS = ((0, "Draft"), (1, "Published"))
# Since a posts' status is either draft and published, it is a boolean value
# STATUS sets boolean 0 / false to Draft and boolean 1 / true to Published

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)


    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
    
    
    def number_of_likes(self):
        return self.likes.count()

# Post is a table in the database
# in author, the on_delete=models.CASCADE means that if the user who created to post is deleted, then all posts made by that user will be deleted as well
# updated_on has auto_now=True, which means that it will default to the current time, unless overridden
# The Meta class deals with ordering and indexing
# here, -created_on will order posts in descending order
# this means that posts will be displayed with the most recent first
# def str is a magic method that returns a string representation of an object
# Django suggests that this be included because the default is unhelpful
# def number_of_likes will return the total number of likes on a post
# the __str__ and number_of_likes methods are children of the Post class, not the Meta class. This caused problems with not displaying the number of likes properly


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"Comment {self.body} by {self.name}"


# this is the model for comments on a post
# post is a foreign key and has on delete cascade so that if a post is deleted, all comments on that post will be deleted too
# the magic string method overrides the standard to be more helpful
# the Meta created on is ordered by created date in ascending order, so that the oldest comments are displayed first
# this mimics a conversation, so that users can follow a discussion

 


