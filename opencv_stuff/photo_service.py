"""
Bottle HTTP service that sends a picture from camera on GET request.
"""

from bottle import response, route, run
import cv2


@route('/')
def index():
    # Would have used something like this to limit the frame buffer to 1,
    # but this is either buggy in OpenCV 2.4 (which is the one available with
    # apt-get in Raspabian Jessie) or not supported by my camera.
    # cap.set(cv2.cv.CV_CAP_PROP_FRAME_COUNT, 1)
    #
    # cv2.VideoCapture would be created and released globally then.

    cap = cv2.VideoCapture(0)
    _, frame = cap.read()
    cap.release()
    
    _, image_buffer = cv2.imencode('.jpg', frame)
    image_bytes = image_buffer.tostring()

    response.status = 200
    response.headers['Content-Type'] = 'image/jpeg'
    return image_bytes


run(host='0.0.0.0', port=8080)

