from django import forms
from blog.models import Post, Comments
from django.utils import timezone


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

    def clean_pub_date(self):
        pub_date = self.cleaned_data.get('pub_date')
        if not pub_date:
            pub_date = timezone.now()
        return pub_date


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)
