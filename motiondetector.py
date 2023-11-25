import numpy as np
import imutils
import cv2

# @see https://www.pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/
class Detective:
    def __init__(self, weight=0.5):
        self.weight = weight # accumulation weight
        self.back = None # background
        
    def update(self, im):
        if self.back is None:
            self.back = im.copy().astype("float")
            return
        cv2.accumulateWeighted(im, self.back, self.weight)

    def detect(self, im, tvar=25):
        delta = cv2.absdiff(self.back.astype("uint8"), im)
        thresh = cv2.threshold(delta, tvar, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)

        contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        (minx, miny) = (np.inf, np.inf)
        (maxx, maxy) = (-np.inf, -np.inf)

        if len(contours) == 0:
            return None

        for c in contours:
            (x, y, w, h) = cv2.boundingRect(c)
            (minx, miny) = (min(minx, x), min(miny, y))
            (maxx, maxy) = (max(maxx, x + w), max(maxy, y + h))

        return (thresh, (minx, miny, maxx, maxy))

