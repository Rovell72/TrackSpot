from django import forms
from .models import Track

class TrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ['title', 'description', 'cover', 'audio_file']

    def clean_audio_file(self):
        file = self.cleaned_data.get('audio_file')
        if file:
            if not file.name.lower().endswith(('.mp3', '.wav', '.ogg')):
                raise forms.ValidationError("Разрешены только аудиофайлы форматов .mp3, .wav или .ogg!")
        return file
