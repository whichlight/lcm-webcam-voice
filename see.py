import cv2
import time


def capture_and_save_image(cap, filename):
    # Capture one frame
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

    # Crop to 512x512 from the center
    cropped_frame = frame[start_y:end_y, start_x:end_x]
    cv2.imshow("Cropped Camera Feed", cropped_frame)

    # Save the image
    cv2.imwrite(filename, cropped_frame)
    print(f"Image saved as {filename}")


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open camera")

    while True:
        capture_and_save_image(cap, "center_frame.jpg")
        time.sleep(0.3)
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
