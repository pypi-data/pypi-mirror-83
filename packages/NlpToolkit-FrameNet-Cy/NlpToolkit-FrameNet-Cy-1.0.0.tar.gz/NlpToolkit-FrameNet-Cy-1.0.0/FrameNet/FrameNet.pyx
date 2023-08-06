import os
import xml.etree.ElementTree
from FrameNet.Frame cimport Frame


cdef class FrameNet:

    cdef list frames

    def __init__(self, directory="../Frames/"):
        self.frames = []
        for r, d, f in os.walk(directory):
            for file in f:
                root = xml.etree.ElementTree.parse(os.path.join(r, file)).getroot()
                self.frames.append(Frame(file, root))

    cpdef int size(self):
        return len(self.frames)

    cpdef Frame getFrame(self, int index):
        return self.frames[index]
