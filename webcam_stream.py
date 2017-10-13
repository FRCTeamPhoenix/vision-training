import cv2
import numpy as np
import v4l2capture
import v4l2ctl
import select

cap = v4l2capture.Video_device("/dev/video1")
size_x, size_y = cap.set_format(640, 480, fourcc='MJPG')
cap.set_exposure_auto(1)
cap.create_buffers(30)
cap.queue_all_buffers()
cap.start()
select.select((cap,), (), ())
image_data = cap.read_and_queue()
v4l2ctl.set(1, v4l2ctl.PROP_EXPOSURE_ABS, 10)

while True:
    # Capture frame-by-frame
    select.select((cap,), (), ())
    image_data = cap.read_and_queue()

    frame = cv2.imdecode(np.frombuffer(image_data, dtype=np.uint8), cv2.cv.CV_LOAD_IMAGE_COLOR)

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.close()
cv2.destroyAllWindows()
