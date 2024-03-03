from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Tuple constant defines post state
STATUS = ((0, "Draft"), (1, "Published"))
APPROVE = ((0, "Not approved"), (1, "Approved"))


# Create your models here.
class Post(models.Model):
    # Unique so that there can't be posts with the same title, max length is 200 char for the title.
    title = models.CharField(max_length=200, unique=True)
    # Slug is a term for article in production, for Django it will build the URL for posts.
    slug = models.SlugField(max_length=200, unique=True)
    # 1 User can have multiple posts, 1-to-many / Foreign Key. on delete of user account "CASCADE" will also delete all user's posts, 
    # "RESTRICT" will require the posts to be manually deleted one by one
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    # Cloudinary image field
    featured_image = CloudinaryField('image', default='placeholder')
    # Main blog article content
    content = models.TextField()
    # Optional summary / teaser visible on main page
    excerpt = models.TextField(blank=True)
    # Time of creation, "auto_now_add=True" means default created time is time of post entry
    created_on = models.DateTimeField(auto_now_add=True)
    # Time of update / edit of post, auto_now is when it is saved, not just created
    updated_on = models.DateTimeField(auto_now=True)
    # A draft is defined as zero and published as one, so you can see the default is to save as a draft.
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        # - =Descending, most recent at the top, ? =Randomized, blank =Ascending, oldest first
        # First descends through created_on, then ascends that list in author
        ordering = ["-created_on", "author"]
        
    def __str__(self):
        # Returns the title of post in the string instead of "PostObject1"
        return f"{self.title} | Written by {self.author}"


class Comment(models.Model):
    # Post and Author are a 1-to-many relation, 1 user can have multiple posts/comments,
    # so they must be Foreign Keys. On delete of post or account, all comments will be deleted.
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    body = models.TextField()
    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment: {self.body} by {self.author}"