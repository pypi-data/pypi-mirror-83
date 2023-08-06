from xml.dom.minidom import Element


cdef class Frame:

    def __init__(self, name: str, root: Element):
        self.lexicalUnits = []
        self.name = name
        for lexicalUnit in root:
            self.lexicalUnits.append(LexicalUnit(lexicalUnit.attrib["ID"], lexicalUnit))

    cpdef LexicalUnit getLexicalUnit(self, int index):
        return self.lexicalUnits[index]

    cpdef int size(self):
        return len(self.lexicalUnits)

    cpdef str getName(self):
        return self.name
