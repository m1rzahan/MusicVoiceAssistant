
import speech_recognition as sr
import pyttsx3
import pywhatkit
import webbrowser

def playSoundCloud(text):
    return "https://soundcloud.com/search?q=" + text.replace(" ", "+")
def open_url_in_browser(url):

    webbrowser.open(url)



r=sr.Recognizer()
print(sr.Microphone.list_microphone_names())
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source,duration=1)

    print("say anything : ")
    audio= r.listen(source)
    try:
        text = r.recognize_google(audio,language="tr")
        print(text)
        if "YouTube" in text:
            pywhatkit.playonyt(text)
        elif "SoundCloud" in text:
            formatted_url = playSoundCloud(text)
            open_url_in_browser(formatted_url)

    except:
        print("sorry, could not recognise")
