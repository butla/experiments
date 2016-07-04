"""
Bottle HTTP service that streams the image from camera as MJPEG (Motion JPEG)
to a single client.
"""

from bottle import response, route, run
import cv2

cap = cv2.VideoCapture(0)


@route('/')
def index():
    response.status = 200
    response.headers['Content-Type'] = 'multipart/x-mixed-replace;boundary=frame'
    return video_stream()


# based on http://www.chioka.in/python-live-video-streaming-example/
def video_stream():
    while True:
        _, frame = cap.read() 
        _, image_buffer = cv2.imencode('.jpg', frame)
        image_bytes = image_buffer.tostring()
        yield ('--frame\r\n'
               'Content-Type: image/jpeg\r\n\r\n' + image_bytes + '\r\n\r\n')


try:
    run(host='0.0.0.0', port=8080)
except KeyboardInterrupt:
    cap.release()
    print('Bye!')

