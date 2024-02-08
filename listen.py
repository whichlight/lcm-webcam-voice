import speech_recognition as sr

filename = "voice_prompt.txt"


def main():
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    while True:
        try:
            # Use the microphone as source for input
            with sr.Microphone() as source:
                print("\nListening...")
                # Adjust the recognizer sensitivity to ambient noise
                recognizer.adjust_for_ambient_noise(source, duration=0.8)
                # Record the audio from the microphone
                audio = recognizer.listen(source)

                # Using Google's speech recognition to convert audio to text
                print("Processing...")
                text = recognizer.recognize_google(audio)
                print(f"You said: {text}")
                with open(filename, "w") as file:
                    file.write(text + "\n")

        except sr.UnknownValueError:
            # Catch the error if speech is unintelligible
            print("Sorry, I could not understand. Please try again.")
        except sr.RequestError as e:
            # Catch the error if there's a problem with the internet connection
            print(
                f"Could not request results; check your internet connection. Error details: {e}"
            )
        except KeyboardInterrupt:
            # Exit the loop when Ctrl+C is pressed
            print("\nExiting...")
            break


if __name__ == "__main__":
    main()
