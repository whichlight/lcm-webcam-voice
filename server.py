from flask import Flask, render_template, jsonify
import fal
import requests
import base64
from PIL import Image
import cv2
import time

app = Flask(__name__)


# Function to read the latest image URL
def read_latest_image_url():
    try:
        with open("latest_image_url.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return None


# Function to convert image to base64
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string


def capture_image(cap):
    # Capture one frame
    for i in range(5):
        cap.read()
    ret, frame = cap.read()

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        return

    # Calculate the center slice dimensions
    imgsize = 1024
    offset = int(imgsize / 2)
    center_x, center_y = frame.shape[1] // 2, frame.shape[0] // 2
    start_x, start_y = center_x - offset, center_y - offset
    end_x, end_y = center_x + offset, center_y + offset

    # Crop
    cropped_frame = frame[start_y:end_y, start_x:end_x]
    cv2.imwrite("center_frame.jpg", cropped_frame)
    print("img saved")

    # Base64 encode
    retval, buffer = cv2.imencode(".jpg", cropped_frame)
    base64_string = base64.b64encode(buffer).decode()

    return base64_string


# Read the prompt from the file
def get_prompt_run_lcm():
    with open("voice_prompt.txt", "r") as file:
        prompt = file.read().strip()

    # take pic
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")

    # Convert the image to base64
    image_base64 = capture_image(cap)
    image_url = f"data:image/jpeg;base64,{image_base64}"

    # Submitting the request
    print(prompt)
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
    return image_url


@app.route("/latest-image-url")
def latest_image_url():
    image_url = read_latest_image_url()
    return jsonify({"image_url": image_url})


# Route to display the image
@app.route("/")
def show_image():
    image_url = read_latest_image_url()
    return render_template("image.html", image_url=image_url)


if __name__ == "__main__":
    app.run(debug=True)
