from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from .models import Post
from .forms import CommentForm
from django.http import HttpResponseRedirect

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
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            }
        )
    

    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        
        comment_form = CommentForm(data=request.POST)
        # this variable holds the data from the form

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        # this if statement checks if the comment_form has been filled out correctly
        # if so, it grabs the user's email and username
        # the comment variable saves the data from the form, but does not yet commit it to the database
        # comment.post assigns the parent post that the comment is being made on
        # comment.save saves this
        # the else block handles invalid forms, and returns and empty instance of CommentForm, essentially restting the form

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "liked": liked,
                "comment_form": CommentForm()
            }
        )
        # the commented key is used in post_detail.html to display a message to the user that their comment has been submitted and is awaiting approval

# PostDetail is the functionality to display a single post's content
# This highlights a difference between class-based views and function-based views
# In a class-based view, we need to use class methods to handle HTTP requests, either GET or POST
# these methods are only ever given HTTP methods (get, post, etc) as names


class PostLike(View):

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)

        if post.likes.filter(id=request.user.id).exists():
            # checks to see if a user has already liked a post
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        
        return HttpResponseRedirect(reverse('post_detail', args=[slug]))
        # when a post is liked or unliked, the page will reload
