import speech_recognition as sr
import pyttsx3
import cohere

recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Replace this with your actual cohere API key
cohere_client = cohere.Client('dHSL7yHsPR3tbxDTciQswNzJrKVm0magwzaTVNXI')

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en')
        print(f"User said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Could you please repeat?")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return ""

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def get_cohere_response(prompt):
    if "law" in prompt or "justice" in prompt:
        prompt = f"Give me a detailed explanation about {prompt} in the context of law and justice."
    else:
        prompt = f"Give me a detailed response about {prompt}."

    response = cohere_client.generate(
        model='command-xlarge-nightly',
        prompt=prompt,
        max_tokens=150
    )
    return response.generations[0].text.strip()

def assistant():
    speak("Hello! I am your voice assistant. How can I help you today?")

    while True:
        command = listen()

        if command:
            if "bye" in command:
                speak("Goodbye!")
                break
            else:
                response = get_cohere_response(command)
                speak(response)
        else:
            speak("I didn't hear anything. Could you please repeat?")

# Corrected entry point
if __name__ == "__main__":
    assistant()
