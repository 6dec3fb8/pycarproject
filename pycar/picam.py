#!/usr/bin/python3

#   This module is used to control the Raspi camera using its native
# package `picamera` and process its image using the opencv.
#
# structure
# (temp):
# thread,0.5s->data->queue
#
# A contour list is:
# [ (x, y, area, contour), * ]
# and will sort by area.

__all__ = [
    'ContourProducingThread',
]
# imports

import logging
import cv2
import threading
import time
import queue
import numpy as np
from picamera import PiCamera

TC_RED = (0, 0, 255)
TC_GREEN = (0, 255, 0)
TC_BLUE = (255, 0, 0)

_contour_color = TC_RED
_center_color = TC_GREEN

# functions


def _process_image(img, threshold):
    """
    To process the image and return an binary image.
    """
    # imgHLS = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # imgsplit = cv2.split(imgHLS)
    imgsplit = cv2.split(imgHSV)

    # Threshold
    ret, imgBi = cv2.threshold(
            imgsplit[2],
            threshold,
            255,
            cv2.THRESH_BINARY
            )
    if not ret:
        return None

    # clear small blackholes
    close_kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT, (3, 3)
            )
    img_final = cv2.morphologyEx(
            imgBi, cv2.MORPH_CLOSE, close_kernel
            )

    return img_final

def _get_contour_list(
        image, show_image=False,
        threshold=220,
        max_returns=-1):
    """
    return a list of contour location and size.
    max_returns < 0 means return all the contours.
    """
    img_proceed = _process_image(image, threshold)
    # TODO:
    # Calc contours and return.
    # contours, hierarchy = cv2.findContours(img_proceed, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    img_tmp, contours, hierarchy = cv2.findContours(
        img_proceed, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    # img_contour = np.zeros((*img_proceed.shape, 3), dtype=np.uint8)
    img_show = image
    if contours:
        # cv2.drawContours(img_contour, contours,
        # draw on source picture
        img_show = cv2.drawContours(image, contours,
                    -1,  # draw all contours
                    # (0, 255, 0) # green
                    _contour_color
                    )
    # cv2.imshow('contours', img_contour)
    if show_image:
        cv2.imshow('contours', img_show)
        cv2.waitKey(1)
    if contours:
        return _process_contours(contours, max_returns)
    else:
        return []


def _process_contours(contours, max_returns):
    """
    Return a list of contour informations and sorted by area.

    :param list contours: the contours return by cv2.findContours
    :param int max_returns: limit the return number
    :return: a list of tuple(x, y, area, contour)
    :rtype:(int, int, float, list)
    """
    result = []
    for contour in contours:
        moments = cv2.moments(contour)
        if moments['m00'] > 0:
            x, y, area = (int(moments['m10'] / moments['m00']),
                        int(moments['m01'] / moments['m00']),
                        moments['m00'])
            result.append((x, y, area, contour))
    result.sort(key=lambda x:x[2], reverse=True)
    if max_returns > 0:
        return result[:max_returns]
    else:
        return result
    pass



# classes

class ContourProducingThread(threading.Thread):
    """
    Produce the contour data.
    """
    def __init__(self, threshold=220, resolution=(640, 480),
                 max_returns=1, framerate=25, shutter_speed=6000,
                 exposure_compensation=0):#-18):
        super(ContourProducingThread, self).__init__()
        self._vcam = PiCamera(resolution=resolution, framerate=framerate)
        self._vcam.shutter_speed = shutter_speed
        self._vcam.exposure_compensation = exposure_compensation

        self._queue = queue.Queue(2)
        self._exit_event = threading.Event()
        self._condition_noticer = threading.Condition()

        self._max_returns = max_returns
        self._logger = logging.getLogger(__name__)
        self._logger.info(
            "The PI ver. Contour producer is built."
        )

    def run(self):
        wid, hei = self._vcam.resolution
        image_capture = np.zeros((hei, wid, 3), dtype=np.uint8)
        cam_iterator = self._vcam.capture_continuous(
            image_capture, 'bgr',
            use_video_port=True
        )
        self._logger.info(
            "Ready to run the capture loop."
        )
        while not self._exit_event.is_set():
            next(cam_iterator)
            contour_info_list = _get_contour_list(image_capture, show_image=True)

            # write
            with self._condition_noticer:
                try:
                    self._queue.put_nowait(contour_info_list)
                except queue.Full:
                    # drop 1
                    self._logger.warning("Dropped 1 data!")
                    self._queue.get()
                    self._queue.put_nowait(contour_info_list)
                # Notice all waitiog threads that the data is produced and ready to be used.
                self._condition_noticer.notify_all()
                self._logger.info(
                    "Inserted an contour info."
                )
                time.sleep(0.015)
        del cam_iterator
        self._vcam.close()
        self._logger.info(
            "The thread exits."
        )

    @property
    def exit_event(self):
        return self._exit_event

    @exit_event.setter
    def exit_event(self, value):
        raise RuntimeError("Cannot change exit_event at runtime!")

    @property
    def queue_out(self):
        return self._queue

    @queue_out.setter
    def queue_out(self, value):
        raise RuntimeError("Cannot change queue_out at runtime!")

    @property
    def noticer(self):
        return self._condition_noticer

    @noticer.setter
    def noticer(self, value):
        raise RuntimeError("Cannot change the noticer at runtime!")

# tests

def _test_1():
    print('TEST 01')
    th = ContourProducingThread()
    cv = th.noticer
    q = th.queue_out
    t0 = time.time()
    th.start()
    print("Start.")
    try:
        while True:
            with cv:
                result = cv.wait(1/10)
                if result:
                    contours = q.get()
                    if contours:
                        x, y, area, _ = contours[0]
                        print("[%f] contour(%d, %d) of area %f" %
                            (time.time()-t0, x, y, area))
                    else:
                        print("[%f] No contour." %
                            (time.time()-t0))
                else:
                    print("Timeout")
            time.sleep(1/10)
    except KeyboardInterrupt:
        th.exit_event.set()
        th.join()
        print("\nExiting...")


if __name__ == '__main__':
    _test_1()
