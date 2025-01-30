# https://pypdf.readthedocs.io/en/stable/modules/PageRange.html
import pypdf
# import pyttsx3 as pytts
# from gtts import gTTS as tts
# For pulse audio - a WSL to Windows connection
import os
import torch

# See MyCroft-AI.gitbook.io/docs
# https://pypi.org/project/TTS/
from TTS.api import TTS

def text_to_speech_pytts(text, voice_id=None):
    os.environ['PULSE_SERVER'] = 'tcp:localhost'
    engine = pytts.init()
    voices = engine.getProperty('voices')

    # for voice in voices:
    #     print(voice.id)
    if voice_id is None:
        engine.setProperty('voice', "English (America)")

    engine.setProperty('rate', 150)

    # engine.say(text)
    engine.save_to_file(text, '/mnt/c/Users/KSull/Downloads/test.mp3')
    engine.runAndWait()


def text_to_speech_gtts(text, lang='en', accent='com'):
    engine = tts(text=text, lang=lang, tld=accent)
    engine.save('/mnt/c/Users/KSull/Downloads/test.mp3')

def text_to_speech_tts(text, lang='en', accent='com'):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(device)
    # tts --list_models
    # print(TTS().list_models())
    # tts = TTS("tts_models/en/ljspeech/speedy-speech").to(device)
    tts = TTS(
        "tts_models/en/jenny/jenny",
        progress_bar=True,
        gpu=True
    ).to(device)

    # bash >> tts --list_models

    # text="This is a long sentence that should be a good indication of how well the model does I think. But I don't; know..."


    mp3 = tts.tts_to_file(
        text=text,
        # text="This is a small test file to figure out if I want this voice?"
        # speaker_wav="my/cloning/audio.wav",
        # language="en",
        file_path="/mnt/c/Users/KSull/Downloads/test.mp3"
    )

def read_pdf(filepath, save_file, start=None, end=None):
    with open(filepath, 'rb') as file:
        pdf_reader = pypdf.PdfReader(file)
        if start is not None:
            start = max(start -1, 0)
        else:
            start = 0

        if end is not None:
            end = min(end, len(pdf_reader.pages))

        text = ""

        for page_num in range(start, end):
            page = pdf_reader.pages[page_num]
            # text += f"\n--- Page {page_num + 1} ---\n"
            tmp = page.extract_text()

            # This is to remove page numbers
            last_nl = tmp.rfind('\n')
            tmp = tmp if last_nl < 0 else tmp[:last_nl]


            # Annoying word splits
            split_word = f"{chr(8208)}\n"
            tmp = tmp.replace(split_word, '')
            # these are slanted quotes. 
            tmp = tmp.replace(chr(8220), '"')
            tmp = tmp.replace(chr(8221), '"')

            text += tmp + '\n'
        
        print(text)
        with open(save_file, 'w') as file:
            file.write(text)
        # print(start)
        # print(end)


if __name__ == '__main__':
    # text_to_speech_tts('Hello, please work nicely')
    text_file = './.artifacts/ch5.txt'
    if False:
        read_pdf(
            '/mnt/c/Users/KSull/Downloads/Designing Data-Intensive Applications The Big Ideas Behind Reliable, Scalable, and Maintainable Systems ( PDFDrive ).pdf',
            save_file=text_file,
            start=167,
            end=220
        )

    if True:
        with open(text_file, 'r') as file:
            text = file.read()

        # Removing new lines
        text = text.replace('\n', ' ')
        # This is —
        text = text.replace(chr(8212), '; ')

        text_to_speech_tts(text)
