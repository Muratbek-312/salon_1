from django import forms
from snowpenguin.django.recaptcha3.fields import ReCaptchaField

from .models import Rating, RatingStar, MasterProfile, Comment


class RatingForm(forms.ModelForm):

    star = forms.ModelChoiceField(queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None)

    class Meta:
        # " Форма добавления рейтинга "
        model = Rating
        fields = ("star", )


class MasterProfileForm(forms.ModelForm):
    class Meta:
        model = MasterProfile
        fields = ['first_name', 'last_name', 'is_master']


class CommentForm(forms.ModelForm):
    """Форма комметария"""
    body = forms.CharField(widget=forms.Textarea(attrs={
        "class": "comment",
        "placeholder": "comment here",
        "row": 4}))

    class Meta:
        model = Comment
        fields = ("body", )

