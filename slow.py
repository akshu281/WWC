import os
import speech_recognition as sr
from tqdm import tqdm

#Audio
from pydub import AudioSegment
from pydub.utils import make_chunks
import pydub

#Split audio into chunks
pydub.AudioSegment.converter = "C:\\ffmpeg\\bin\\ffmpeg.exe"
#AudioSegment.ffmpeg = "C:\\ffmpeg\\bin\\ffmpeg.exe"
myaudio = AudioSegment.from_mp3("E:\\Women who code\\sample.wav", "wav") 
chunk_length_ms = 100000 # pydub calculates in millisec
chunks = make_chunks(myaudio, chunk_length_ms) #Make chunks of 30 sec
print(len(chunks))

#Export all of the individual chunks as wav files

for i, chunk in enumerate(chunks):
    chunk_name = "E:\\Women who code\\chunks\\chunk{0}.wav".format(i)
    print("exporting", chunk_name)
    chunk.export(chunk_name, format="wav")

with open("E:\\Women who code\\apikey.json") as f:
    GOOGLE_CLOUD_SPEECH_CREDENTIALS = f.read()

r = sr.Recognizer()
files = sorted(os.listdir('E:\\Women who code\\chunks'))

all_text = []

for f in tqdm(files):
    name = "E:\\Women who code\\chunks\\" + f
    # Load audio file
    with sr.AudioFile(name) as source:
        audio = r.record(source)
    # Transcribe audio file
    text = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
    all_text.append(text)

transcript = ""
for i, t in enumerate(all_text):
    total_seconds = i * 30
    # Cool shortcut from:
    # https://stackoverflow.com/questions/775049/python-time-seconds-to-hms
    # to get hours, minutes and seconds
    m, s = divmod(total_seconds, 60)
    h, m = divmod(m, 60)

    # Format time as h:m:s - 30 seconds of text
    transcript = transcript + "{:0>2d}:{:0>2d}:{:0>2d} {}\n".format(h, m, s, t)

print(transcript)
with open("E:\\Women who code\\chunks\\transcript.txt", "w") as f:
    f.write(transcript)