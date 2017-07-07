import cv2

from brightness import Brightness

'''import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt'''

DEBUG = False
SCALE_FACTOR = 1.3
MIN_NEIGHBOR = 5

BLUE = (255, 0, 0)  # B,G,R
GREEN = (0, 255, 0)
OFF_THRESHOLD = 2


'''def imshow(image):
    plt.axis("off")
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.show()
'''


def reduce_gray_image(image):
    # Resize image for faster processing
    frame = cv2.resize(original_frame, (0, 0), fx=0.5, fy=0.5,
                       interpolation=cv2.INTER_NEAREST)
    # Gray scale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return frame, gray


if __name__ == '__main__':
    webcam = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(
        './haar/haarcascade_frontalface_alt2.xml')
    eye_cascade = cv2.CascadeClassifier('./haar/haarcascade_eye.xml')
    original_size = None
    maximum_size = 0
    screen = Brightness()
    original_bright = screen.get_brightness()
    current_bright = None

    while True:
        # Read from webcam
        got_frame, original_frame = webcam.read()
        if got_frame:
            frame, gray = reduce_gray_image(original_frame)
            # Detect faces
            faces = face_cascade.detectMultiScale(
                gray, SCALE_FACTOR, MIN_NEIGHBOR)
            bright = current_bright
            for (fx, fy, fw, fh) in faces:
                if DEBUG:
                    cv2.rectangle(frame, (fx, fy), (fx+fw, fy+fh), BLUE, 2)
                area = float(fw*fh)
                if not original_size:
                    original_size = area
                    maximum_size = area * OFF_THRESHOLD
                else:
                    if area > maximum_size:
                        bright = 0
                    elif area > original_size:
                        area_percent = area / maximum_size
                        bright = original_bright - (
                            original_bright * area_percent)
                    else:
                        bright = original_bright

                if bright != current_bright:
                    current_bright = bright
                    screen.set_brightness(current_bright)
                if DEBUG:
                    print fx, fy, fw, fh
            if DEBUG:
                cv2.imwrite('photo.jpg', frame)

    # Stop the capture
    webcam.release()
    screen.set_brightness(original_bright)
