from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import AudioFileForm
from .models import AudioFile
from .utils import transcribe_audio
import os
from django.conf import settings

def upload_audio(request):
    # This if block handles the POST request (when the user submits the form)
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        form = AudioFileForm(request.POST, request.FILES)
        # Check if the form is valid
        if form.is_valid():
            # Create a new AudioFile object but don't save to the database yet
            new_audio_file = form.save(commit=False)
            # Save the original filename from the uploaded file
            new_audio_file.original_filename = request.FILES['file'].name
            # Now save the complete object to the database
            new_audio_file.save()


            # 1. Update status to "processing"
            new_audio_file.status = 'processing'
            new_audio_file.save(update_fields=['status']) # Efficiently save only this field

            # 2. Get the full path to the uploaded file
            audio_file_path = os.path.join(settings.MEDIA_ROOT, str(new_audio_file.file))

            # 3. Call the Whisper API utility function
            transcription_text = transcribe_audio(audio_file_path)
            print(f"[VIEW DEBUG] transcribe_audio function returned: {transcription_text}")

            # 4. Handle the API response
            if transcription_text:
                new_audio_file.status = 'transcribed'
                new_audio_file.raw_transcription = transcription_text
                # For now, also set corrected to the raw transcription
                new_audio_file.corrected_transcription = transcription_text
                messages.success(request, f'File uploaded and transcribed successfully! <a href="/file/{new_audio_file.pk}/">Go correct the transcription</a>.')
            else:
                new_audio_file.status = 'error'
                messages.error(request, 'File uploaded, but transcription failed. Please try again.')

            # 5. Save the final state of the object
            new_audio_file.save()
            # Redirect the user back to the upload form.
            return redirect('transcriber:upload_audio')
    else:
        # This block handles the GET request (when the user just loads the page)
        # Create a new, empty form for the user to fill out
        form = AudioFileForm()

    # Render the HTML template, passing the form to it so it can be displayed
    return render(request, 'transcriber/upload.html', {'form': form})

def audiofile_detail(request, pk):
    """
    Displays the details of a specific AudioFile and allows for correction.
    """
    # Fetch the specific AudioFile object from the database, or return a 404 if not found.
    audio_file = get_object_or_404(AudioFile, pk=pk)

    # This if block handles saving the corrected text from the form
    if request.method == 'POST':
        # Get the corrected text from the form submission
        corrected_text = request.POST.get('corrected_text')
        # Update the model instance
        audio_file.corrected_transcription = corrected_text
        audio_file.save()
        # Add a success message and reload the page
        messages.success(request, 'Corrections saved successfully!')
        return redirect('transcriber:audiofile_detail', pk=audio_file.pk)

    # If it's a GET request, just render the page with the AudioFile data
    return render(request, 'transcriber/audiofile_detail.html', {'audio_file': audio_file})