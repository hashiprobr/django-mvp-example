from django import forms
from django.core.exceptions import ValidationError

from .models import PublicFile, PrivateFile


class FileForm(forms.Form):
    description = forms.CharField(label='Description')
    data = forms.FileField(allow_empty_file=True)
    private = forms.BooleanField(label='This is a private file', required=False)

    def clean(self):
        data = super().clean()
        if data['private']:
            if PrivateFile.objects.filter(data=data['data']):
                raise ValidationError({'data': 'Private file with this name already exists'})
            file = PrivateFile(description=data['description'], data=data['data'])
        else:
            if PublicFile.objects.filter(data=data['data']):
                raise ValidationError({'data': 'Public file with this name already exists'})
            file = PublicFile(description=data['description'], data=data['data'])
        file.clean_fields()
        self.file = file
        return data
