from django import forms
from django.forms import modelformset_factory
from .models import Service, ServiceImage


class CreateServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'


class ImageForm(forms.ModelForm):
    class Meta:
        model = ServiceImage
        fields = ('image', )


ImagesFormSet = modelformset_factory(ServiceImage, form=ImageForm, extra=3, max_num=5, can_delete=True)


class UpdateServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'
