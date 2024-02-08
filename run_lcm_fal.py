import fal
import requests
import base64
from PIL import Image
import time


# Function to convert image to base64
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string


# Read the prompt from the file
def get_prompt_run_lcm():
    try:
        with open("voice_prompt.txt", "r") as file:
            prompt = file.read().strip()

        # Convert the image to base64
        image_base64 = image_to_base64("center_frame.jpg")
        image_url = f"data:image/jpeg;base64,{image_base64}"

        # Submitting the request
        handler = fal.apps.submit(
            "110602490-lcm-sd15-i2i",
            arguments={
                "prompt": prompt,
                "image_url": image_url,
                "strength": 0.8,
                "seed": 42,
                "guidance_scale": 1,
                "num_inference_steps": 2,
                "sync_mode": 0,
                "enable_safety_checks": 0,
            },
        )

        for event in handler.iter_events():
            if isinstance(event, fal.apps.InProgress):
                print("Request in progress")
                print(event.logs)

        # Fetching the result
        # print(dir(handler))
        result = handler.get()
        print(result["images"])

        # Saving the output image to a file
        if result and "images" in result and len(result["images"]) > 0:
            image_url = result["images"][0]["url"]
            with open("latest_image_url.txt", "w") as file:
                file.write(image_url)

        """
            response = requests.get(image_url)
            if response.status_code == 200:
                with open("output_image.jpg", "wb") as file:
                    file.write(response.content)
                print("Output image saved as output_image.jpg")
            else:
                print("Failed to download the image from the URL provided.")
        """
    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(1)


if __name__ == "__main__":
    while True:
        get_prompt_run_lcm()
