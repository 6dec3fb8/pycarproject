#!/usr/bin/python3

#   This module is used to control
# the Raspi camera with opencv.
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
try:
    from picamera import PiCamera
    _use_picamera = True
except:
    _use_picamera = False

TC_RED = (0, 0, 255)
TC_GREEN = (0, 255, 0)
TC_BLUE = (255, 0, 0)

_contour_color = TC_RED
_center_color = TC_GREEN

# functions

def _get_video(index=0):
    """
    get the video #index. Will check whether use normal or pycamera.
    :param int index: the index of camera. Ignored if using PiCamera.
    """
    if _use_picamera:
        vcam = PiCamera()
        vcam.exposure_compensation = -15
    else:
        vcam = cv2.VideoCapture(index)
        # vcam.set(cv2.CAP_PROP_XI_EXPOSURE, -9)
    return vcam


def _release_video(vcam):
    """
    release the video by different video type.
    """
    if _use_picamera:
        vcam.close()
    else:
        vcam.release()


def _read_image(cam, resolution = (640, 480)):
    """
    Read an image from camera.
    Resolution is ignored when using system camera.
    However it is useful when using on Raspi.
    """
    image = None
    if _use_picamera:
        # assume that cam is type 'PiCamera'
        wid, hei = resolution
        nparrsize = (hei, wid, 3)
        image = np.empty(nparrsize, dtype=np.uint8)
        cam.resolution = resolution
        cam.capture(image, 'bgr')
        # print(image)
    else:
        # assume that cam in type'cv2.VideoCapture
        res, image = cam.read()
        if not res:
            image = None
    return image


def _process_image(img, threshold, _debug):
    """
    To process the image and return an binary image.
    """
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

    # img_contour = np.zeros((*img_proceed.shape, 3), dtype=np.uint8)
    if contours:
        # cv2.drawContours(img_contour, contours,
        # draw on source picture
        img_show = cv2.drawContours(img, contours,
                    -1,  # draw all contours
                    # (0, 255, 0) # green
                    _contour_color
                    )
    # cv2.imshow('contours', img_contour)
    cv2.imshow('contours', img_show)
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
    cv2.drawContours(image, contours, -1, _contour_color)
    for p in points:
        #                               V---red
        cv2.circle(image, p, 2, _center_color)
    cv2.imshow('Contours and center', image)
    cv2.waitKey(0)


def _print_contour_info(contourinfo):
    """
    DEBUGGING function!
    :param list contourinfo:
        list of tuple (x: int, y: int, area: float, contour: list)
    """
    format_data = []
    for x, y, area, _ in contourinfo:
        format_data.append(
            "<Contour(%d, %d):%f>" % (
                x, y, area
            )
        )
    print('[', ', '.join(format_data), ']')

class ContourProducingThread(threading.Thread):
    """
    The thread used to produce light contours per 0.05s
    """
    def __init__(self, buf_size=3, time_interval=0.05,
                 threshold=220, max_returns=1):
        """
        The constructor of the thread.
        :param threading.Event stop_event:
            when this event is set, the whole thread stops.
        :param queue queue_out: The queue to put data produced
        :param float time_interval: Seconds between each VideoCapture.
        """
        super(ContourProducingThread, self).__init__()
        self._t_interval = time_interval
        # changed to attributes(properties)
        self._exit_event = threading.Event()
        self._q_output = queue.Queue(buf_size)
        # noticer
        self._condition_noticer = threading.Condition()
        self._threshold = threshold
        self._max_returns = max_returns
        # initialize the camera
        self._vcam = _get_video()
        self._logger = logging.getLogger(__name__)
        self._logger.info(
            "Contour producer is constructed."
        )
        # TODO:
        # other codes here

    def run(self):
        # TODO:
        # job
        self._logger.info("ContourProducingThread is running.")
        while not self._exit_event.is_set():
            # do the producer job
            contour_info_list = _get_contour_list(
                self._vcam,
                self._threshold,
                self._max_returns
            )
            # write
            with self._condition_noticer:
                try:
                    self._q_output.put_nowait(contour_info_list)
                except queue.Full:
                    # drop 1
                    self._logger.warning("Dropped 1 data!")
                    self._q_output.get()
                    self._q_output.put_nowait(contour_info_list)
                # Notice all waitiog threads that the data is produced and ready to be used.
                self._condition_noticer.notify_all()
                self._logger.info(
                    "Inserted an contour info."
                )
            time.sleep(self._t_interval)
        # exiting the thread
        self._logger.info("Contour producer Thread exit.")

    @property
    def exit_event(self):
        return self._exit_event

    @exit_event.setter
    def exit_event(self, value):
        raise RuntimeError("Cannot change exit_event at runtime!")

    @property
    def queue_out(self):
        return self._q_output

    @queue_out.setter
    def queue_out(self, value):
        raise RuntimeError("Cannot change queue_out at runtime!")

    @property
    def noticer(self):
        return self._condition_noticer

    @noticer.setter
    def noticer(self, value):
        raise RuntimeError("Cannot change the noticer at runtime!")


# test drive

def _test_1():
    vcam = _get_video()
    _, tempimage = vcam.read()
    x, y, _ = tempimage.shape
    contour_list = _get_contour_list(
        vcam,
        threshold=240,
        max_returns=3,
        _debug=True
    ) # , _debug=True)
    # print(contour_list)
    _print_contour_info(contour_list)
    _debug_paint_contour_and_masscenter(contour_list, (x, y))
    # time.sleep(3)
    _release_video(vcam)


def _test_2():
    time_interval = 0.05
    stop_event = threading.Event()
    q = queue.Queue(5)
    th = ContourProducingThread(
        stop_event,
        q,
        time_interval
    )
    th.start()
    try:
        while True:
            try:
                item = q.get_nowait()
            except queue.Empty:
                print("Queue empty! Not syncing")
            else:
                if item:
                    x, y, area, _ = item[0]
                    print("Detected contour at (%d, %d) with area of %f" %
                          (x, y, area))
                else:
                    print("No contour detected!")
            time.sleep(time_interval + 0.07)
    except KeyboardInterrupt:
        stop_event.set()
        th.join()
        print()
        print("Exiting...")


def _test_3():
    time_interval = 0.05
    th = ContourProducingThread(
        time_interval = 0.05
    )
    q = th.queue_out
    halt_ev = th.exit_event
    noticer = th.noticer
    th.start()
    try:
        while True:
            with noticer:
                result = noticer.wait(time_interval)
                if result:
                    x, y, area, _ = q.get()[0]
                    print("Detected contour at (%d, %d) with area of %f" %
                          (x, y, area))
    except KeyboardInterrupt:
        halt_ev.set()
        th.join()
        print()
        print("Exiting...")



# main
if __name__ == '__main__':
    _test_3()
