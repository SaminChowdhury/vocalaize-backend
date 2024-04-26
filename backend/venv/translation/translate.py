import tempfile
import os
import io

from transformers import MarianMTModel, MarianTokenizer
from TTS.api import TTS
import whisper
from pydub import AudioSegment

import requests
import json

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from google.oauth2 import service_account

import sys

# Google Drive Setup
SCOPES = ['https://www.googleapis.com/auth/drive']

# Create temp dir
temp_dir = tempfile.TemporaryDirectory()

### Language Mapping
nlp_codes = {
  'English': 'en',
  'Spanish': 'es',
  'French': 'fr',
  'Italian': 'it',
  'German': 'de',
  'Arabic': 'ar',
  'Chinese': 'zh',
  'Hindi': 'hi',
  'Russian': 'ru',
  'Japanese': 'ja',
}

### Non-Standard Model Names:
# es-zh, fr-it, en-ja tatoeba
# zh-ja uses tc-big
nlp_nonstandard = {
  ('es', 'zh'): 'Helsinki-NLP/opus-tatoeba',
  ('fr', 'it'): 'Helsinki-NLP/opus-tatoeba',
  ('en', 'ja'): 'Helsinki-NLP/opus-tatoeba',
  ('zj', 'ja'): 'Helsinki-NLP/opus-mt-tc-big',
}

### Unavailable
# es-hi, es-ja
# fr-zh, fr-hi, fr-ja
# it-zh, it-hi, it-ru, it-ja
# de-hi, de-ru, de-ja
# ar-zh, ar-hi, ar-ja
# zh-es, zh-fr, zh-ar, zh-hi, zh-ru
# hi-es, hi-fr, hi-it, hi-de, hi-ar, hi-zh, hi-ru, hi-ja
# ru-it, ru-de, ru-zh, ru-hi, ru-ja
# ja-zh, ja-hi
nlp_unavail = {
  ('es', 'hi'), ('es', 'ja'),
  ('fr', 'zh'), ('fr', 'hi'), ('fr', 'ja'),
  ('it', 'zh'), ('it', 'hi'), ('it', 'ru'), ('it', 'ja'),
  ('de', 'hi'), ('de', 'ru'), ('de', 'ja'),
  ('ar', 'zh'), ('ar', 'hi'), ('ar', 'ja'),
  ('zh', 'es'), ('zh', 'fr'), ('zh', 'ar'), ('zh', 'hi'), ('zh', 'ru'),
  ('hi', 'es'), ('hi', 'fr'), ('hi', 'it'), ('hi', 'de'), ('hi', 'ar'), ('hi', 'zh'), ('hi', 'ru'), ('hi', 'ja'),
  ('ru', 'it'), ('ru', 'de'), ('ru', 'zh'), ('ru', 'hi'), ('ru', 'ja'),
  ('ja', 'zh'), ('ja', 'hi')
}


# Path to the service account credentials file
SERVICE_ACCOUNT_FILE = 'config/service.json'
SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate_drive():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)
    return service


def download_file(service, folder_id, file_name, temp_dir):
    # Construct the query to find the file in the specified folder
    query = f"'{folder_id}' in parents and name = '{file_name}'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    items = results.get('files', [])

    # Handle the case where no files are found
    if not items:
        print('No files found.')
        return None

    # Assuming we want the first file matching the criteria
    input_file = items[0]
    request = service.files().get_media(fileId=input_file['id'])
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}% complete.")

    # Save the downloaded file to the specified local directory
    file_path = os.path.join(temp_dir, input_file['name'])
    with open(file_path, 'wb') as file:
        file.write(fh.getbuffer())
    
    return file_path


### Change audio format to wav if not already
def convert_wav(audio):
  # Set path
  dir, filename = os.path.split(audio)
  base_filename, ext = os.path.splitext(filename)

  wav_path = os.path.join(dir, base_filename + '.wav')

  # Check if already wav file
  if ext.lower() == '.wav':
    return audio

  # If not wav file
  raw = AudioSegment.from_file(audio)
  raw.export(wav_path, format='wav')

  # Remove original
  os.remove(audio)

  return wav_path

### Audio transcription function
def transcribe(audio, model_type = 'base', dir = temp_dir.name):
  base_filename = os.path.splitext(os.path.basename(audio))[0]
  transcribed_filename = os.path.join(dir, base_filename + '.txt')

  # Assignments
  whisper_model = whisper.load_model(model_type, device='cpu')
  transcribed = whisper_model.transcribe(audio)

  with open(transcribed_filename, 'w') as file:
    for segment in transcribed['segments']:
      start = segment['start']
      end = segment['end']
      text = segment['text']
      file.write(f"[{start:.2f}-{end:.2f}] {text}\n")

  #print(transcribed['text'])

  return transcribed_filename

### Merge timestamps & lines into single line w/ only text
def merge_lines(transcribed):

  # Get lines from file & merge
  with open(transcribed, 'r') as file:
    lines = file.readlines()
    merged = ' '.join([line.split('] ')[1].strip() for line in lines if '] ' in line])

  # Write merged line to file
  with open(transcribed, 'w') as file:
    file.write(merged)

### Define Model Paths
def model_name(init_lang, target_lang):
  if (init_lang, target_lang) in nlp_nonstandard:
    base_model = nlp_nonstandard[(init_lang, target_lang)]
    nlp_model = f'{base_model}-{init_lang}-{target_lang}'
    return nlp_model

  # No direct translation
  elif (init_lang, target_lang) in nlp_unavail:
    # Check if initial language -> English uses non-standard model name
    if (init_lang, 'en') in nlp_nonstandard:
      base_model_1 = nlp_nonstandard[(init_lang, 'en')]
      nlp_model_1 = f'{base_model_1}-{init_lang}-en'
    else:
      nlp_model_1 = f'Helsinki-NLP/opus-mt-{init_lang}-en'

    # Check if English -> translated language uses non-standard model name
    if ('en', target_lang) in nlp_nonstandard:
      base_model_2 = nlp_nonstandard[('en', target_lang)]
      nlp_model_2 = f'{base_model_2}-en-{target_lang}'
    else:
      nlp_model_2 = f'Helsinki-NLP/opus-mt-en-{target_lang}'

    return (nlp_model_1, nlp_model_2)

  # Direct translation
  else:
    nlp_model = f'Helsinki-NLP/opus-mt-{init_lang}-{target_lang}'
    return nlp_model

### Load Model & Tokenizer
def model_init(nlp_model):
  # If not direct path
  if isinstance(nlp_model, tuple):
    tokenizer1 = MarianTokenizer.from_pretrained(nlp_model[0])
    model1 = MarianMTModel.from_pretrained(nlp_model[0])

    tokenizer2 = MarianTokenizer.from_pretrained(nlp_model[1])
    model2 = MarianMTModel.from_pretrained(nlp_model[1])

    return [(tokenizer1, model1), (tokenizer2, model2)]

  # Direct path
  else:
    tokenizer = MarianTokenizer.from_pretrained(nlp_model)
    model = MarianMTModel.from_pretrained(nlp_model)

    return [(tokenizer, model)]

### Translate txt file to selected language
def translate_text(transcribed, tokenizer, model, dir = temp_dir.name):

  with open(transcribed, "r") as file:
    text = file.read()

  # Translate text
  model_inputs = tokenizer(text, return_tensors="pt", truncation=True, padding="longest")
  translated = model.generate(**model_inputs)
  translated_text = tokenizer.batch_decode(translated, skip_special_tokens=True)[0]

  # Create translated txt file
  name, ext = os.path.splitext(transcribed)
  translated_filename = f"{name}-Translation{ext}"
  translated = os.path.join(dir, translated_filename)

  with open(translated, 'w', encoding='utf-8') as file:
    file.write(translated_text)

  print(translated_text)

  return translated

# Generate translated & cloned speech
def generate_speech(translated_text, audio, target_lang, dir = temp_dir.name):

  # Create translated wav file
  name, ext = os.path.splitext(os.path.basename(audio))
  translated_audio_filename = f"{name}-Translation{ext}"
  print(translated_audio_filename)
  translated_audio = os.path.join(dir, translated_audio_filename)

  with open(translated_text, "r", encoding='utf-8') as file:
    text = file.read()

  # Initialize model
  tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cpu")

  # Translate text
  tts.tts_to_file(text=text,
    file_path=translated_audio,
    speaker_wav=audio,
    language=target_lang
  )

  return translated_audio

def main():
  # Command line to get translation_id
  translation_id = sys.argv[1]

  print(translation_id)

  # API GET - get input_drive_path, source_language, target_language from backend
  GET_url = f"http://127.0.0.1:5000/translation/{translation_id}"

  response = requests.get(GET_url)

  data = response.json()

  print("Status Code:", response.status_code)
  print("Response Body:", response.text) 

  file_name = data.get("input_drive_path")
  init_lang = data.get("source_language")
  target_lang = data.get("target_language")

  print(file_name, init_lang, target_lang)

  # Get NLP codes from nlp_codes mapping
  init_lang = nlp_codes.get(init_lang)
  target_lang = nlp_codes.get(target_lang)

  # Authenticate & download audio file
  service = authenticate_drive()

  # Path to 'input' folder
  input_folder ="1a6q5sEvEBMz7zNSsKRqfolaTlq9L2bvv"

  # Download audio file
  input_audio = download_file(service, input_folder, file_name, temp_dir.name)

  # Make sure audio is wav format
  input_audio = convert_wav(input_audio)

  # Transcribe audio
  transcribed = transcribe(input_audio)

  # Merge lines in transcribed text
  merge_lines(transcribed)

  # Get model name(s) from direct / indirect path
  nlp_model = model_name(init_lang, target_lang)

  init_results = model_init(nlp_model)

  ### Check if direct / indirect path & translate accordingly
  # Direct path
  if len(init_results) == 1:
    tokenizer, model = init_results[0]
    translated_text = translate_text(transcribed, tokenizer, model)

  # Indirect path
  else:
    tokenizer1, model1 = init_results[0]
    intermediate_text = translate_text(transcribed, tokenizer1, model1)
    tokenizer2, model2 = init_results[1]
    translated_text = translate_text(intermediate_text, tokenizer2, model2)

  # Set correct Chinese code for TTS
  if (target_lang == 'zh'):
    target_lang = 'zh-cn'

  # Simulated output from a function that generates speech
  output_audio = generate_speech(translated_text, input_audio, target_lang)

  # The backend endpoint for uploading audio files
  POST_url = "http://127.0.0.1:5000/upload-audio-final"

  # Construct the filename for the audio file
  output_audio_base = os.path.splitext(os.path.basename(output_audio))[0] + '.wav'
  print("Generated audio file:", output_audio_base)

  # Open the generated audio file in binary mode for reading
  with open(output_audio, 'rb') as audio_file:
      # Prepare the file data as a dictionary of the form {'file': file_tuple}
      # file_tuple should be (filename, fileobject, content_type)
      files = {'file': (output_audio_base, audio_file, 'audio/wav')}
      # Assuming you have a way to specify or retrieve the translation ID
      # Include the translation ID in the form data
      data = {'translation_id': translation_id}

      # Make the POST request with both the file and the additional data
      response = requests.post(POST_url, files=files, data=data)

      # Print the response from the server
      print("Response status code:", response.status_code)
      print("Response body:", response.text)

  # API PUT - send translation ID to backend
  PUT_url = f"http://localhost:5000/translation/{translation_id}"
  out_params = {

  }

  headers = {
    'Content-Type': 'application/json'
  }
  response = requests.put(PUT_url, data=json.dumps(out_params), headers=headers)

if __name__ == '__main__':
  main()