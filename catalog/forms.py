from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'rows': '4',
            'style': 'resize: none;',
        }),
        label='')

    class Meta:
        model = Review
        fields = ['rating', 'comment',]
        labels = {'rating': ''}

