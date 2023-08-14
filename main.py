import cv2
import streamlit as st
import speech_recognition as sr
from PIL import Image, ImageOps, ImageChops
import os

def main():

    import pyaudio

    pa = pyaudio.PyAudio()

    print('\navailable devices:')

    for i in range(pa.get_device_count()):
        dev = pa.get_device_info_by_index(i)
        name = dev['name'].encode('utf-8')
        print(i, name, dev['maxInputChannels'], dev['maxOutputChannels'])

    print('\ndefault input & output device:')
    print(pa.get_default_input_device_info())
    print(pa.get_default_output_device_info())


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
    with microphone(device_index=2) as source:

        recognizer.adjust_for_ambient_noise(source, duration=0.2)
        st.write("Listening...")
        audio = recognizer.listen(source)
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
        # horizontal_scroll = st.container().horizontal_scroll()

        for i in s:
            loc = os.path.join(alphabet_dir, i.upper() + ".png")
            print(loc)
            if os.path.exists(loc):
                # original_image = Image.open(loc)
                # background_image = Image.new("RGBA", original_image.size, background_color)
                # resized_background = background_image.resize(original_image.size, Image.ANTIALIAS)
                # merged_image = Image.alpha_composite(resized_background, original_image)
                
                # Display the merged image in the horizontal scroll container
                from PIL import Image
                from io import BytesIO 

                image = Image.open(loc).convert("RGBA")
                new_image = Image.new("RGBA", image.size, "WHITE") # Create a white rgba background
                new_image.paste(image, (0, 0), image)              # Paste the image on the background. Go to the links given below for details.
                new_image.convert('RGB').save('test.jpg', "JPEG")  # Save as JPEG
                # orig = Image.new(mode='RGBA', size=(240, 60))
                # stream = BytesIO()
                # orig.save(stream, "PNG")
                # new = Image.open(stream)
                st.image(new_image, caption=i)
            else:
                st.warning(f"Image {i}.png not found.")

if __name__ == "__main__":
    main()
