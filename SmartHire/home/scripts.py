import cv2
import time
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import speech_recognition as sr
import multiprocessing

def add_question_overlay(frame, question):
    img_pil = Image.fromarray(frame)

    font = ImageFont.truetype("arial.ttf", 20)
    text_color = (255, 0, 255)  # White color

    draw = ImageDraw.Draw(img_pil)
    draw.text((10, 30), question, font=font, fill=text_color)

    frame_with_overlay = np.array(img_pil)

    return frame_with_overlay

def record_video():
    cap = cv2.VideoCapture(0)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
   
    size = (frame_width, frame_height)
    result = cv2.VideoWriter('interview.avi', 
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         15, size)

    questions = [
        "What is your name?",
        "Tell us about your experience.",
        "What are your strengths?",
        "Why do you want this job?",
        # Add more questions here
    ]

    time_limit = 5

    for question in questions:
        start_time = time.time()

        while time.time() - start_time < time_limit:
            ret, frame = cap.read()
            result.write(frame)
        
            frame_with_overlay = add_question_overlay(frame, question)

            cv2.imshow('Interview Question', frame_with_overlay)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

def record_audio():
    recognizer = sr.Recognizer()

# Set the recording duration in seconds
    recording_duration = 10  # Adjust this as needed

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Recording...")
        audio = recognizer.listen(source, timeout=recording_duration)

    # recognize the speech
    try:
        transcript = recognizer.recognize_google(audio)
        print("You said: " + transcript)
        with open('transcript.txt', 'w') as f:
            f.write(transcript)

        # save the audio
        with open("output.wav", "wb") as f:
            f.write(audio.get_wav_data())
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand your audio")
    except sr.RequestError as e:
        print("Google Speech Recognition error: {0}".format(e))
    except KeyboardInterrupt:
        print("Recording interrupted")

    print("Recording completed.")

if __name__ == "__main__":
    p1 = multiprocessing.Process(target=record_video)
    p2 = multiprocessing.Process(target=record_audio)

    # Start the processes
    p1.start()
    p2.start()

    # Wait for the processes to finish
    p1.join()
    p2.join()