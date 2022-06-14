"""
Copyright (C) 2020 Intel Corporation

SPDX-License-Identifier: BSD-3-Clause
"""

from sklearn.metrics.pairwise import cosine_similarity
from collections import deque, OrderedDict


class TrackableObject:
    def __init__(self, bbox, reid, centroid):
        self.bbox = bbox
        self.reid = reid
        self.centroids = []
        self.centroids.append(centroid)
        self.updated = False


class PersonTrackers(object):
    def __init__(self, trackers, line, line_above, line_below, callback=None, callback2=None, callback3=None):
        self.trackers = trackers
        self.dissapeared = OrderedDict()
        self.trackId_generator = 0
        self.similarity_threshold = 0.7
        self.max_disappeared = 10
        self.callback = callback
        self.callback2 = callback2
        self.callback3 = callback3
        self.line = line
        self.line_above = line_above
        self.line_below = line_below

    def similarity(self, trackers):
        sim = deque()
        if len(self.trackers) > 0:
            trackers_number = len(trackers)
            track_copy = self.trackers.items()
            if trackers_number == 0:
                trackers_copy = self.trackers.copy()
                for trackerId, data in trackers_copy.items():
                    self.dissapeared[trackerId] += 1
                    if self.dissapeared[trackerId] > self.max_disappeared:
                        self.deregister(trackerId)

            else:
                for tracker in trackers:
                    for trackerId, data in track_copy:
                        try:
                            cosine = cosine_similarity(tracker.reid, data.reid)
                        except ValueError as e:
                            print(e)
                            continue
                        if cosine > self.similarity_threshold:
                            sim.append([trackerId, cosine[0][0]])
                    if sim:
                        max_similarity = self.get_max_similarity(sim)
                        if max_similarity is None:
                            continue
                        self.trackers[max_similarity].reid = tracker.reid
                        self.trackers[max_similarity].bbox = tracker.bbox
                        self.trackers[max_similarity].centroids.append(tracker.centroids[0])
                        self.dissapeared[max_similarity] = 0
                        self.trackers[max_similarity].updated = True
                    else:
                        self.trackers.update({self.trackId_generator: tracker})
                        self.trackers[self.trackId_generator].updated = True
                        self.dissapeared.update({self.trackId_generator: 0})
                        self.trackId_generator += 1

                if trackers_number <= len(track_copy):
                    trackers_copy = self.trackers.copy()
                    for trackerId, data in trackers_copy.items():
                        if not data.updated:
                            self.dissapeared[trackerId] += 1
                            if self.dissapeared[trackerId] > self.max_disappeared:
                                self.deregister(trackerId)
                                continue
                        self.trackers[trackerId].updated = False
        else:
            self.register(trackers)

    def register(self, trackers):
        for tracker in trackers:
            self.trackers.update({self.trackId_generator: tracker})
            self.dissapeared.update({self.trackId_generator: 0})
            self.trackId_generator += 1

    def deregister(self, trackerId):
        if self.callback:
            first = self.trackers[trackerId].centroids[0]
            last = self.trackers[trackerId].centroids[-1]
            self.callback(self.line, first, last)
        if self.callback2:
            first = self.trackers[trackerId].centroids[0]
            last = self.trackers[trackerId].centroids[-1]
            self.callback2(self.line_above, first, last)
        if self.callback3:
            first = self.trackers[trackerId].centroids[0]
            last = self.trackers[trackerId].centroids[-1]
            self.callback3(self.line_below, first, last)
        del self.trackers[trackerId]
        del self.dissapeared[trackerId]

    def get_max_similarity(self, simil_list):
        def take_second(cosine):
            return cosine[1]
        simil = sorted(simil_list, key=take_second, reverse=True)
        for sim in simil:
            if not self.trackers[sim[0]].updated:
                return sim[0]
        return None

    def clear(self):
        self.trackers.clear()
        self.trackId_generator = 0

