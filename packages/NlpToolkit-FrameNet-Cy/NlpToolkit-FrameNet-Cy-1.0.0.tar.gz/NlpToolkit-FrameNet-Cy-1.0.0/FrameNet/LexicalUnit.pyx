from xml.dom.minidom import Element


cdef class LexicalUnit:

    def __init__(self, id: str, root: Element):
        self.frameElements = []
        self.synSetId = id
        for element in root:
            self.frameElements.append(element.text)

    cpdef int size(self):
        return len(self.frameElements)

    cpdef list getFrameElements(self):
        return self.frameElements
