#!/usr/bin/python3

#   This module is used to control
# the Raspi camera with opencv.
#
# structure
# (temp):
# thread,0.5s->data->queue
#
# A contour list is:
# [ [x, y, area], * ]
# and will sort by area.

# imports

import logging
import cv2
import threading
import time
import numpy as np
try:
    from picamera import PiCamera
    _use_picamera = True
except:
    _use_picamera = False


# functions

def _read_image(cam, resolution = (640, 480)):
    image = None
    if _use_picamera:
        # assume that cam is type 'PiCamera'
        wid, hei = resolution
        nparrsize = (hei, wid, 3)
        image = np.empty(nparrsize, dtype=np.uint8)
        cam.resolution = resolution
        cam.capture(image, 'bgr')
        print(image)
    else:
        # assume that cam in type'cv2.VideoCapture
        res, image = cam.read()
        if not res:
            image = None
    return image


def _process_image(img, threshold, _debug):
    # imgHLS = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # imgsplit = cv2.split(imgHLS)
    imgsplit = cv2.split(imgHSV)

    # show H, S and V
    if _debug:
        cv2.imshow('H',imgsplit[0])
        cv2.imshow('S',imgsplit[1])
        cv2.imshow('V',imgsplit[2])
        cv2.waitKey(0)

    # Threshold
    ret, imgBi = cv2.threshold(
            imgsplit[2],
            threshold,
            255,
            cv2.THRESH_BINARY
            )
    if not ret:
        return None

    if _debug:
        cv2.imshow('Bi', imgBi)
        cv2.waitKey(0)
    # img_final = cv2.GaussianBlur(imgBi, (3, 3), 1.5)

    # clear small blackholes
    close_kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT, (3, 3)
            )
    img_final = cv2.morphologyEx(
            imgBi, cv2.MORPH_CLOSE, close_kernel
            )

    if _debug:
        cv2.imshow('Biclose', img_final)
        cv2.waitKey(0)
    return img_final


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


def _get_contour_list(vcamera, show_image=False,
        resolution=(640, 480), threshold=220,
        max_returns=-1, _debug=False):
    """
    return a list of contour location and size.
    max_returns < 0 means return all the contours.
    """
    # ret, img = cvcamera.read()
    img = _read_image(vcamera, resolution)
    if img is None:
        # opencv failed
        return None
    if _debug:
        cv2.imshow('Camera', img)
        cv2.waitKey(0)
    img_proceed = _process_image(img, threshold, _debug)
    # TODO:
    # Calc contours and return.
    # contours, hierarchy = cv2.findContours(img_proceed, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    img_tmp, contours, hierarchy = cv2.findContours(img_proceed, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if _debug:
        print("Contours:", contours)
        print("Hierachy:", hierarchy)

    img_contour = np.zeros((*img_proceed.shape, 3), dtype=np.uint8)
    if contours:
        cv2.drawContours(img_contour, contours,
                -1,  # draw all contours
                (0, 255, 0) # greem
                )
    cv2.imshow('contours', img_contour)
    if _debug:
        cv2.waitKey(0)
    cv2.waitKey(1)
    if contours:
        return _process_contours(contours, max_returns)
    else:
        return []


def _debug_paint_contour_and_masscenter(contourinfo, shape):
    """
    Only used in debugging!
    :param [(int, int, float, list)] contourinfo:
        a list of tuple(x, y, area, contour)
    :param (int, int) shape:
        numpy array size format shape of original image
    """
    if not contourinfo:
        return None
    contours = [item[3] for item in contourinfo]
    points = [(item[0], item[1]) for item in contourinfo]
    image = np.zeros((*shape, 3), dtype=np.uint8)
    #                                          V--green
    cv2.drawContours(image, contours, -1, (0, 255, 0))
    for p in points:
        #                               V---red
        cv2.circle(image, p, 2, (0, 0, 255))
    cv2.imshow('Contours and center', image)
    cv2.waitKey(0)


class ContourProducingThread(threading.Thread):
    """
    the thread to produce light contours per 0.5s
    """
    def __init__(self, queueCtlr, queueOut, time_interval=0.5):
        super(ContourProducingThread, self).__init__()
        self._t_interval = time_interval
        self._q_control = queueCtlr
        self._q_output = queueOut
        self._logger = logging.getLogger(__name__)
        self._logger.info(
            "Contour producer is constructed."
        )
        # TODO:
        # other codes here

    def run(self):
        # TODO:
        # job
        pass


# test drive

def _test_1():
    if _use_picamera:
        vcam = PiCamera()
        vcam.exposure_compensation = -15
    else:
        vcam = cv2.VideoCapture(0)
        # vcam.set(cv2.CAP_PROP_XI_EXPOSURE, -9)
    _, tempimage = vcam.read()
    x, y, _ = tempimage.shape
    contour_list = _get_contour_list(vcam, threshold=240,  _debug=False) # , _debug=True)
    print(contour_list)
    _debug_paint_contour_and_masscenter(contour_list, (x, y))
    time.sleep(3)
    if _use_picamera:
        vcam.close()
    else:
        vcam.release()


# main
if __name__ == '__main__':
    _test_1()
