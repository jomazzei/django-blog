from django.contrib import admin
# The .period infront of models is to indicate that models is in the same directory
# as this admin.py file
from .models import Post, Comment
from django_summernote.admin import SummernoteModelAdmin


# This code gives admin panel greater functionality and clarity
@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):

    list_display = ('title', 'slug', 'status')
    search_fields = ['title']
    list_filter = ('status',)
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)


# Register your models here.
admin.site.register(Comment)