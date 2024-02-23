from django.db import models
from django.contrib.auth.models import User

# Tuple constant defines post state
STATUS = ((0, "Draft"), (1, "Published"))


# Create your models here.
class Post(models.Model):
    # Unique so that there can't be posts with the same title, max length is 200 char for the title.
    title = models.CharField(max_length=200, unique=True)
    # Slug is a term for article in production, for Django it will build the URL for posts.
    slug = models.SlugField(max_length=200, unique=True)
    # 1 User can have multiple posts, 1-to-many / Foreign Key. on delete of user account "CASCADE" will also delete all user's posts
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    # Main blog article content
    content = models.TextField()
    # Time of creation, "auto_now_add=True" means default created time is time of post entry
    created_on = models.DateTimeField(auto_now_add=True)
    # A draft is defined as zero and published as one, so you can see the default is to save as a draft.
    status = models.IntegerField(choices=STATUS, default=0)
