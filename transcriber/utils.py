import openai
from django.conf import settings
import os

def transcribe_audio(audio_file_path):
    """
    Sends an audio file to the OpenAI Whisper API for transcription.
    Returns the transcribed text or None if an error occurs.
    """
    # Set the API key from our settings
    openai.api_key = settings.OPENAI_API_KEY

    # Check if the file exists at the given path
    if not os.path.exists(audio_file_path):
        print(f"Error: File not found at {audio_file_path}")
        return None

    try:
        # Open the audio file in read-binary mode
        with open(audio_file_path, "rb") as audio_file:
            # Make the API call to the Whisper model
            transcript = openai.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text" # Ask for plain text directly
            )
        # Return the transcribed text
        return transcript

    except Exception as e:
        # Print any errors that occur during the API call
        print(f"An error occurred during transcription: {e}")
        return None

# def transcribe_audio(audio_file_path):
#     """
#     Sends an audio file to the OpenAI Whisper API for transcription.
#     Returns the transcribed text or None if an error occurs.
#     """
#     print(f"[DEBUG] Attempting to transcribe: {audio_file_path}") # Debug 1

#     # Check if the API key is loaded
#     if not settings.OPENAI_API_KEY:
#         print("[ERROR] OPENAI_API_KEY is not set in settings.") # Debug 2
#         return None

#     openai.api_key = settings.OPENAI_API_KEY

#     if not os.path.exists(audio_file_path):
#         print(f"[ERROR] File not found at {audio_file_path}") # Debug 3
#         return None

#     try:
#         print("[DEBUG] Opening file and calling API...") # Debug 4
#         with open(audio_file_path, "rb") as audio_file:
#             transcript = openai.audio.transcriptions.create(
#                 model="whisper-1",
#                 file=audio_file,
#                 response_format="text"
#             )
#         print(f"[DEBUG] API call successful. Transcript: {transcript}") # Debug 5
#         return transcript

#     except openai.AuthenticationError as e:
#         # This is the specific error for a bad API key
#         print(f"[ERROR] Authentication failed. Invalid API key or no payment set up. Details: {e}") # Debug 6
#         return None
#     except openai.APIConnectionError as e:
#         print(f"[ERROR] Failed to connect to OpenAI API: {e}") # Debug 7
#         return None
#     except openai.APIError as e:
#         print(f"[ERROR] OpenAI API returned an error: {e}") # Debug 8
#         return None
#     except Exception as e:
#         # This catches any other unexpected errors
#         print(f"[ERROR] An unexpected error occurred: {e}") # Debug 9
#         return None