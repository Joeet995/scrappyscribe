from django import forms
from .models import AudioFile

class AudioFileForm(forms.ModelForm):
    class Meta:
        model = AudioFile
        fields = ['file']  # This form will only show the file upload field
        

