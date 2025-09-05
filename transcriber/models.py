from django.db import models
import os

# A helper function to determine the upload path for audio files
def get_upload_path(instance, filename):
    # This will save files to 'media/audio_files/{filename}'
    return os.path.join('audio_files', filename)

class AudioFile(models.Model):
    # Choices for the status of the transcription process
    STATUS_CHOICES = [
        ('uploaded', 'Uploaded'),
        ('processing', 'Processing'),
        ('transcribed', 'Transcribed'),
        ('error', 'Error'),
    ]

    # The core fields for our model
    file = models.FileField(upload_to=get_upload_path)  # This handles file uploads
    original_filename = models.CharField(max_length=255) # Stores the original name
    uploaded_at = models.DateTimeField(auto_now_add=True) # Automatic timestamp

    # Fields for the transcription results
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='uploaded')
    raw_transcription = models.TextField(blank=True, null=True)  # From Whisper API
    corrected_transcription = models.TextField(blank=True, null=True) # After human edit

    # A string representation of the model (helpful for debugging/admin panel)
    def __str__(self):
        return f"{self.original_filename} ({self.status})"