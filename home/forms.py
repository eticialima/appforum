from django import forms
from post.models import Post, SocialComment
 
class SocialPostForm(forms.ModelForm):
        body = forms.CharField(widget=forms.Textarea(attrs={'rows': '4','placeholder': 'Comentar alguma coisa...'}),required=True) 
        class Meta:
                model=Post
                fields=['body']


class SocialCommentForm(forms.ModelForm):
        comment = forms.CharField(widget=forms.Textarea(attrs={'rows': '2','placeholder': 'Responder comentário...'}),required=True)

        class Meta:
                model=SocialComment
                fields=['comment'] 