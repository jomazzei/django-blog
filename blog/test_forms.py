from django.test import TestCase
from .forms import CommentForm

# Create your tests here.
class TestCommentForm(TestCase):

    def test_form_is_valid(self):
        # Fills out a dummy comment with data
        comment_form = CommentForm({'body': 'This is a great post'})
        # assertTrue checks if form is valid
        self.assertTrue(comment_form.is_valid(), msg="Form is invalid")
    
    def test_form_is_invalid(self):
        comment_form = CommentForm({'body': ''})
        self.assertFalse(comment_form.is_valid(), msg="Form is valid")