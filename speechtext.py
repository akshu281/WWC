#Audio
from pydub import AudioSegment
from pydub.utils import make_chunks
import pydub

#speech to Text
import os
import speech_recognition as sr
from tqdm import tqdm
from multiprocessing.dummy import Pool
#Directory Path
inpath="E:\\Women who code\\"

def speech(inputfile,lang):
    print("Inside Speech")
    #inputfile="Test.wav"
    #Split audio into chunks
    pydub.AudioSegment.converter = "C:\\ffmpeg\\bin\\ffmpeg.exe"
    audio=inpath+inputfile
    print(audio)
    myaudio = AudioSegment.from_mp3(audio, "wav") 
    chunk_length_ms = 30000 # pydub calculates in millisec
    chunks = make_chunks(myaudio, chunk_length_ms) #Make chunks of 30 sec
    # print(len(chunks))

    #Export all of the individual chunks as wav files

    for i, chunk in enumerate(chunks):
        chunks_path=inpath+"chunks\\"
        chunk_name = chunks_path+"chunk{0}.wav".format(i)
        # print("exporting", chunk_name)
        chunk.export(chunk_name, format="wav")

    all_text=[]
    #API
    pool = Pool(8) # Number of concurrent threads

    with open(inpath+"apikey.json") as f:
        GOOGLE_CLOUD_SPEECH_CREDENTIALS = f.read()
        # print(GOOGLE_CLOUD_SPEECH_CREDENTIALS)

    r = sr.Recognizer()
    files = os.listdir(chunks_path)
    print(files)
    # sampleout=""
    def transcribe(data):
        idx, file = data
        name = chunks_path + file
        print(name + " started")
        # Load audio file
        with sr.AudioFile(name) as source:
            print("Audio Loaded")
            audio = r.record(source)
        # Transcribe audio file
        print("Reaching transcribing")
        text = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS,language=lang)
        print(name + " done")
        return {
            "idx": idx,
            "text": text
        }

    all_text = pool.map(transcribe, enumerate(files))
    pool.close()
    pool.join()

    transcript = ""
    # print(transcript+" is empty")
    # print(all_text+" is all text")
    for t in sorted(all_text, key=lambda x: x['idx']):
        transcript = transcript + "{}\n".format(t['text'])
        
    print(transcript)

    with open(inpath+"transcript.txt", "w") as f:
        f.write(transcript)

if __name__ == "__main__":
    speech("sample.wav","en-US")
    print("Transcript Done !!!!")