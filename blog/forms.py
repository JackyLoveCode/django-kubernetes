# core/blog/forms.py
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "body"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com"}),
            "body": forms.Textarea(attrs={"rows": 5, "placeholder": "Share your thoughts..."}),
        }

class SearchForm(forms.Form):
    q = forms.CharField(max_length=100, required=False)
