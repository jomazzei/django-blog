from django.contrib import admin
# The .period infront of models is to indicate that models is in the same directory
# as this admin.py file
from .models import Post

# Register your models here.
admin.site.register(Post)