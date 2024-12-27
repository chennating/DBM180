import google.generativeai as genai
import httpx
import os
import base64
import PIL.Image
from dotenv import load_dotenv
import time
from datetime import datetime, timedelta
#import speech_recognition as sr  # Optional: For basic audio processing



def test_text_gen_multimodal_one_image_prompt():
    # [START text_gen_multimodal_one_image_prompt_streaming]
    image = PIL.Image.open("/Users/chennating/Downloads/toys-insta.jpg")
    prompt = "tell a story based on the image for kids"
    response = model.generate_content([prompt, image])
    print(response.text)
    #image_path = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Palace_of_Westminster_from_the_dome_on_Methodist_Central_Hall.jpg/2560px-Palace_of_Westminster_from_the_dome_on_Methodist_Central_Hall.jpg"
    #image = httpx.get(image_path)
    #prompt = "tell a story based on the image for kids"
    #response = model.generate_content([{'mime_type':'image/jpeg', 'data': base64.b64encode(image.content).decode('utf-8')}, prompt])   
'''
if __name__ == "__main__":
    genai.configure(api_key="AIzaSyBtAgbk1lcOrnNDutpsBc0kSveT3D5bBPQ")
    model = genai.GenerativeModel("gemini-1.5-flash")
    #test_text_gen_multimodal_one_image_prompt()
'''

load_dotenv()

genai.configure(api_key="AIzaSyBtAgbk1lcOrnNDutpsBc0kSveT3D5bBPQ")
model = genai.GenerativeModel("gemini-1.5-flash")


def caption_image(image_path):
    """Generates a brief caption for the given image."""
    try:
        image = PIL.Image.open("/Users/chennating/Downloads/toys-insta.jpg")
    except FileNotFoundError:
        return "Error: Image file not found."

    prompt = "Briefly describe the main elements of this image for kids."
    response = model.generate_content([image, prompt])
    return response.text

def get_user_prompt(audio=False):
    """Gets additional prompt from the user (audio or text)."""
    if audio:
      print("Start audio recording, please speak")
      text = record_and_transcribe_audio()
      if text:
         print(f"You said: {text}")
         return text
      else:
          return input("What do you want to add to the story? (name, characteristics, background, etc.) (text)")
    else:
        return input("What do you want to add to the story? (name, characteristics, background, etc.)(text)")

def record_and_transcribe_audio():
    """Records audio and transcribes to text (basic example)."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say something...")
        try:
          audio = recognizer.listen(source, phrase_time_limit=5)  # Adjust recording duration
          text = recognizer.recognize_google(audio) #You need to install speechrecognition lib and have a google cloud api key to make it work
          return text
        except sr.WaitTimeoutError:
            print("no speech detected, recording failed.")
            return None
        except sr.UnknownValueError:
            print("could not understand audio.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None


def generate_story_phase1(image_path, additional_settings):
    """Generates the first part of the story with a twist and a question."""
    try:
      image = PIL.Image.open("/Users/chennating/Downloads/toys-insta.jpg")
    except FileNotFoundError:
        return "Error: Image file not found."
    prompt = f"""Based on the following image and information provided, write a story for kids. The story should last 2-4 minutes, include a twist, end with a question for them about the following story. The story setting should include {additional_settings}.
        """
    response = model.generate_content([image,prompt])
    return response.text

def continue_story(previous_story, user_answer):
    """Continues the story based on the user's answer."""
    prompt = f"""Continue the story based on the previous story and user's answer. 
    previous story: {previous_story}
    user_answer: {user_answer}"""
    response = model.generate_content(prompt)
    return response.text

def get_user_answer():
    """Get the user's answer to the story's question."""
    return input("What do you think the answer is?: ")

def timed_story(image_path, audio = False):
    """Generates a story based on image and user inputs with time limit
    """
    start_time = datetime.now()
    time_limit = timedelta(minutes=4) #4 minutes limit, can be change to anything

    image_caption = caption_image(image_path)
    print(f"AI says: {image_caption}")

    extra_prompt = get_user_prompt(audio)
    print(f"user extra setting: {extra_prompt}")

    phase1_story = generate_story_phase1(image_path, extra_prompt)
    print(f"AI Story phase 1: {phase1_story}")

    user_answer = get_user_answer()
    print(f"User's answer: {user_answer}")

    phase2_story = continue_story(phase1_story, user_answer)
    print(f"AI Story phase 2: {phase2_story}")

    end_time = datetime.now()
    story_duration = end_time - start_time

    if story_duration > time_limit:
      print(f"Story exceed the time limit, it should have take less than {time_limit.total_seconds()/60} minutes, current story took {story_duration.total_seconds()/60} minutes")
    else:
      print(f"Story end. It takes {story_duration.total_seconds()/60} minutes.")


if __name__ == "__main__":
    image_file = "/Users/chennating/Downloads/toys-insta.jpg" #Replace with your image
    timed_story(image_file)