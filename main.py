import streamlit as st
import speech_recognition as sr
from PIL import Image, ImageOps, ImageChops
import os

def main():
    st.title("Image Display with Speech Recognition")

    r = sr.Recognizer()
    mic = sr.Microphone()

    input_mode = st.radio("Select Input Mode:", ["Speech Recognition", "Text Input"])

    if input_mode == "Speech Recognition":
        start_button = st.button("Start Speech Recognition")
        if start_button:
            process_speech(r, mic)
    else:
        text_input = st.text_input("Enter text:")
        if text_input:
            st.write("You entered:", text_input)
            background_color = st.color_picker("Select Background Color", "#FFFFFF")
            display_images(text_input, background_color)

def process_speech(recognizer, microphone):
    recognizer.adjust_for_ambient_noise(microphone, duration=0.2)
    st.write("Listening...")
    audio = recognizer.listen(microphone)
    st.write("Processing speech...")

    try:
        MyText = recognizer.recognize_google(audio)
        MyText = MyText.lower()
        st.write("You said:", MyText)
        display_images(MyText)
    except sr.RequestError as e:
        st.error("Could not request results; {0}".format(e))
    except sr.UnknownValueError:
        st.error("An unknown error occurred")

def display_images(text, background_color="#FFFFFF"):
    s = text.replace(" ", "_")
    alphabet_dir = os.path.join(os.getcwd(), "Alphabets")

    with st.container():
        for i in s:
            loc = os.path.join(alphabet_dir, i.upper() + ".png")
            print(loc)
            if os.path.exists(loc):
                image = Image.open(loc).convert("RGBA")
                new_image = Image.new("RGBA", image.size, "WHITE")
                new_image.paste(image, (0, 0), image)
                new_image.convert('RGB').save('test.jpg', "JPEG")
                st.image(new_image, caption=i)
            else:
                st.warning(f"Image {i}.png not found.")

if __name__ == "__main__":
    main()
