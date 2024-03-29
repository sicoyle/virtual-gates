"""
Copyright (C) 2020 Intel Corporation

SPDX-License-Identifier: BSD-3-Clause
"""

import cv2

# BGR   RGB
COLOR = {"yellow": (0, 255, 255),
         "white":  (255, 255, 255),
         "black":  (0, 0, 0),
         "red":    (0, 0, 255),
         "green":  (0, 128, 0),
         "blue":   (0, 0, 255),
         "grey":   (127, 127, 127),
         "orange": (0, 128, 255),
         "pink":   (203, 192, 255),
         "magenta":(255, 0, 255),
         "green2": (154, 250, 0)
         }


class Draw:
    @staticmethod
    def line(frame, coords, color="yellow", thickness=4):
        xmin, ymin, xmax, ymax = coords
        cv2.line(frame, (xmin, ymin), (xmax, ymax), COLOR[color], thickness)

    @staticmethod
    def rectangle(frame, coords, color="yellow", thickness=2):
        xmin, ymin, xmax, ymax = coords
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), COLOR[color], thickness)

    @staticmethod
    def circle(frame, center, radius, color, thickness=1):
        cv2.circle(frame, center, radius, COLOR[color], thickness, lineType=8, shift=0)

    @staticmethod
    def point(frame, center, color):
        cv2.circle(frame, center, 4, COLOR[color], -1)

    @staticmethod
    def dataAbove(frame, data):
        for (i, (k, v)) in enumerate(data.items()):
            text = "{}: {}".format(k, v)
            cv2.putText(frame, text, (10, ((i * 20) + 60)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR["orange"], 2)

    @staticmethod
    def data(frame, data):
        for (i, (k, v)) in enumerate(data.items()):
            text = "{}: {}".format(k, v)
            cv2.putText(frame, text, (10, ((i * 20) + 100)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR["red"], 2)

    @staticmethod
    def dataBelow(frame, data):
        for (i, (k, v)) in enumerate(data.items()):
            text = "{}: {}".format(k, v)
            cv2.putText(frame, text, (10, ((i * 20) + 140)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR["pink"], 2)

    @staticmethod
    def dataFirst(frame, data):
        for (i, (k, v)) in enumerate(data.items()):
            text = "{}: {}".format(k, v)
            cv2.putText(frame, text, (10, ((i * 20) + 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR["grey"], 2)

    @staticmethod
    def dataLast(frame, data):
        for (i, (k, v)) in enumerate(data.items()):
            text = "{}: {}".format(k, v)
            cv2.putText(frame, text, (10, ((i * 20) + 180)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR["magenta"], 2)

    @staticmethod
    def dataAverage(frame, data):
        for (i, (k, v)) in enumerate(data.items()):
            text = "{}: {}".format(k, v)
            cv2.putText(frame, text, (10, ((i * 20) + 220)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR["white"], 2)

