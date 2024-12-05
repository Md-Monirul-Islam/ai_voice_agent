import openai
from apikey import api_data
import pyttsx3
import speech_recognition as sr
import webbrowser

openai.api_key=api_data

completion=openai.Completion()

# def Reply(question):
#     prompt=f'Chando: {question}\n Jarvis: '
#     response=completion.create(prompt=prompt, engine="text-davinci-002", stop=['\\Chando'], max_tokens=200)
#     answer=response.choices[0].text.strip()
#     return answer

import time
import openai

def Reply(question):
    prompt = f"Chando: {question}\nJarvis: "
    retries = 3
    while retries > 0:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Jarvis, a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=200,
            )
            return response['choices'][0]['message']['content'].strip()
        except openai.error.RateLimitError:
            retries -= 1
            print("Rate limit hit. Retrying...")
            time.sleep(2)  # Wait before retrying
    raise Exception("Rate limit exceeded. Please check your usage and try again later.")


# def Reply(question):
#     prompt = f"Chando: {question}\nJarvis:"
#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",  # Use "text-davinci-003" if turbo is not available
#             messages=[{"role": "user", "content": prompt}],
#             max_tokens=200,
#             stop=["\\Chando"]  # Fixed escape sequence
#         )
#         answer = response['choices'][0]['message']['content'].strip()
#         return answer
#     except Exception as e:
#         print(f"Error: {e}")
#         return "I'm sorry, I couldn't process that request."


engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

speak("Hello How Are You? ")

def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening....')
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing.....")
        query=r.recognize_google(audio, language='en-in')
        print("Chando Said: {} \n".format(query))
    except Exception as e:
        print("Say That Again....")
        return "None"
    return query


if __name__ == '__main__':
    while True:
        query=takeCommand().lower()
        ans=Reply(query)
        print(ans)
        speak(ans)
        if 'open youtube' in query:
            webbrowser.open("www.youtube.com")
        if 'open google' in query:
            webbrowser.open("www.google.com")
        if 'bye' in query:
            break



