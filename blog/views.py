# Http needs to be imported before render
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from .models import Post, Comment
from .forms import CommentForm


# Create your views here.
class PostList(generic.ListView):
    # Filters to only display published blogs on home page, not drafts
    queryset = Post.objects.all().order_by("-created_on").filter(status=1)
    template_name = "blog/index.html"
    paginate_by = 6


def post_detail(request, slug):
    """
    Display an individual :model:`blog.Post`.

    **Context**

    ``post``
        An instance of :model:`blog.Post`.+

    **Template:**

    :template:`blog/post_detail.html`
    """
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comments = post.comments.all().order_by("-created_on")
    comment_count = post.comments.filter(approved=True).count()

    if request.method == "POST":
        print("Received comment POST req")
        comment_form = CommentForm(data=request.POST)

        # The is_valid() method checks our model to see the constraints on our fields.
        # For example, the default behaviour in Django is that a field cannot be null.
        # The is_valid() method makes sure we don't try to write a null value to the database.
        # It also helps improve the security of our system because, even if an attacker bypasses the front-end form HTML validation, we still check it on the back-end.
        if comment_form.is_valid():
            # Call the comment_form's save method with commit=False. 
            # Calling the save method with commit=False returns an object that hasn't yet been saved to the database, so it can be further modified. 
            # We do this because we need to populate the post and author fields before we save. 
            # The object will not be written to the database until we call the save method again.
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()

            messages.add_message(
                request, messages.SUCCESS,
                'Comment submitted and awaiting approval'
            )
            # return redirect makes it so the page is automatically reloaded with a fresh form on submission. 
            # This prevents the form resubmitting twice when page is refreshed manually through browser
            return HttpResponseRedirect(request.path_info)

    comment_form = CommentForm()

    print("Rendering blog post template")
    return render(
        request,
        "blog/post_detail.html",
        {
            "post": post,
            "comments": comments,
            "comment_count": comment_count,
            "comment_form": comment_form,
        },
    )


def comment_edit(request, slug, comment_id):
    """
    View to edit comments
    """
    if request.method == "POST":
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comment = get_object_or_404(Comment, pk=comment_id)
        comment_form = CommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid() and comment.author == request.user:
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.approved = False
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Comment Updated!')
        else:
            messages.add_message(request, messages.ERROR, 'Error updating comment!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))