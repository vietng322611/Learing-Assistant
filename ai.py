import textract
import sys
import speech_recognition as sr

r = sr.Recognizer()
mic = sr.Microphone()
doc = textract.process("./test.docx")
text = ' '.join(doc.decode("utf-8").split("\n\n"))
print(text)

def get_input(recognizer, microphone):
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response = recognizer.recognize_google(audio, language='vi')
    except sr.RequestError:
        # API was unreachable or unresponsive
        return 1
    except sr.UnknownValueError:
        # speech was unintelligible
        return 2
    return response

def get_output(r, mic):
    data = get_input(r, mic)
    if data == 1:
        print("API was unreachable or unresponsive")
        return
    elif data == 2:
        print("Error occurred")
        return
    elif data == 'dừng':
        return sys.exit()