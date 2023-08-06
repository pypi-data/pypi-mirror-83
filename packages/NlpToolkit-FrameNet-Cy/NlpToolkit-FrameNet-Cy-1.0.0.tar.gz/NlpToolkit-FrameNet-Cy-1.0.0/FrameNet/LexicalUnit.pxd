cdef class LexicalUnit:

    cdef str synSetId
    cdef list frameElements

    cpdef int size(self)
    cpdef list getFrameElements(self)
