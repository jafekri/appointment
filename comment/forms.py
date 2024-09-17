from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    # def clean_name(self):

    class Meta:
        model = Comment
        fields = ["author", 'body']