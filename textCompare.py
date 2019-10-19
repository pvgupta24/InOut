import sys
sys.path.append('/Users/anumehaagrawal/Documents/Hacks/InOut/generateQuestions')
import paralleldots
import azure.cognitiveservices.speech as speechsdk
from generateQuestions import main
import os
from dotenv import load_dotenv
load_dotenv()

#import configparser

# Semantic similarity of two texts
def compareTranscripts(text1, text2):
    API_KEY = os.getenv('TRANSCRIPT_API')
    paralleldots.set_api_key(API_KEY)
    response=paralleldots.similarity(text1,text2)
    return response['similarity_score']



#Convert speech to text
def audioTranscript(filenameSent):
    API_KEY = os.getenv('AUDIO_TRANSCRIPT_API')
    speech_key, service_region = API_KEY, "westus"
    initial_silence_timeout_ms = 40 * 1e3
    template = "wss://{}.stt.speech.microsoft.com/speech/recognition" \
            "/conversation/cognitiveservices/v1?initialSilenceTimeoutMs={:d}"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key,
            endpoint=template.format(service_region, int(initial_silence_timeout_ms)))
    audio_config = speechsdk.audio.AudioConfig(filename=filenameSent)
    # Creates a speech recognizer using a file as audio input.
    # The default language is "en-us".
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    result = speech_recognizer.recognize_once()

    # Check the result
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return "{}".format(result.text)
    else:
        return "No speech detected"
   
#Generates questions from  given text.
def generateQuestionsFromText(text):
    questions = main.getAnswers(text)
    finalQuestions = []
    for i in range(len(questions)):
        if(i%2):
            finalQuestions.append(questions[i])
    return finalQuestions
