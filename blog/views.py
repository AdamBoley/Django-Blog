from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Post

# Create your views here.
# the Django_Experimentation - ToDo list project uses function based views in its views.py file
# the Django-Blog project will use class-based views
# the idea is to write reusable code so that one view can inherit from another
# Django provides a generic view, which will be used

class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6


# queryset filters by status=1, so that only posts that have been set to Published will be displayed
# posts will also be ordered in descending order by created_on date
# paginate_by sets the maximum number of objects to be displayed on the front page to 6
# If there are more than 6 posts in the table, Django will automatically implement pagination, creating new pages to hold those additional posts


class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        
        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "liked": liked
            }
        )

# PostDetail is the functionality to display a single post's content
# This highlights a difference between class-based views and function-based views
# In a class-based view, we need to use class methods to handle HTTP requests, either GET or POST
# these methods are only ever given HTTP methods (get, post, etc) as names
