#Audio
from pydub import AudioSegment
from pydub.utils import make_chunks
import pydub

#speech to Text
import os
import speech_recognition as sr
from tqdm import tqdm
from multiprocessing.dummy import Pool

#Split audio into chunks
pydub.AudioSegment.converter = "C:\\ffmpeg\\bin\\ffmpeg.exe"
#AudioSegment.ffmpeg = "C:\\ffmpeg\\bin\\ffmpeg.exe"
myaudio = AudioSegment.from_mp3("E:\\Women who code\\hindi.wav", "wav") 
chunk_length_ms = 30000 # pydub calculates in millisec
chunks = make_chunks(myaudio, chunk_length_ms) #Make chunks of 30 sec
print(len(chunks))

#Export all of the individual chunks as wav files

for i, chunk in enumerate(chunks):
    chunk_name = "E:\\Women who code\\chunks\\chunk{0}.wav".format(i)
    print("exporting", chunk_name)
    chunk.export(chunk_name, format="wav")

all_text=[]
#API
pool = Pool(8) # Number of concurrent threads

#keyfile="E:\\Women who code\\speechtextkey.json"
with open("E:\\Women who code\\apikey.json") as f:
    GOOGLE_CLOUD_SPEECH_CREDENTIALS = f.read()
    print(GOOGLE_CLOUD_SPEECH_CREDENTIALS)

r = sr.Recognizer()
#files = sorted(os.listdir('E:\\Women who code\\chunks'))
files = os.listdir('E:\\Women who code\\chunks')
print(files)
sampleout=""
def transcribe(data):
    idx, file = data
    name = "E:\\Women who code\\chunks\\" + file
    #name=data
    print(name + " started")
    # Load audio file
    with sr.AudioFile(name) as source:
        print("Audio Loaded")
        audio = r.record(source)
    # Transcribe audio file
    print("Reaching transcribing")
    text = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS,language="hi-IN")
    print(name + " done")
    # sampleout=sampleout+" "+text
    return {
        "idx": idx,
        "text": text
    }

all_text = pool.map(transcribe, enumerate(files))
pool.close()
pool.join()

transcript = ""
print(transcript+" is empty")
# print(all_text+" is all text")
for t in sorted(all_text, key=lambda x: x['idx']):
    #sampleout=sampleout+t['text']
    #total_seconds = t['idx'] * 30
    # Cool shortcut from:
    # https://stackoverflow.com/questions/775049/python-time-seconds-to-hms
    # to get hours, minutes and seconds
    #m, s = divmod(total_seconds, 60)
    #h, m = divmod(m, 60)

    # Format time as h:m:s - 30 seconds of text
    transcript = transcript + "{}\n".format(t['text'])
    
print(transcript)
# print(sampleout)

with open("E:\\Women who code\\transcript.txt", "w") as f:
    f.write(transcript)