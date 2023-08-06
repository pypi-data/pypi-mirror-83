from FrameNet.LexicalUnit cimport LexicalUnit


cdef class Frame:

    cdef str name
    cdef list lexicalUnits

    cpdef LexicalUnit getLexicalUnit(self, int index)
    cpdef int size(self)
    cpdef str getName(self)
