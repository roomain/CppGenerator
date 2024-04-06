##define INIT_IMPL(classname) \
#public: \
#   static inline void init(classname& a_toInit, const Class& a_value) \
#   { _INIT_##classname(a_toInit, a_value) }

class ClassMember:
    name = ""
    type = ""

    def print(self):
        print("{} {}".format(self.type, self.name))
    def __init__(self, type, name):
        self.name = name
        self.type = type
    def isValid(self):
        return len(self.name) > 0 and len(self.type) > 0


class Class:
    def __init__(self, name):
        self.classname = name
        self.members = []

    def print(self):
        print(self.classname)
        for member in self.members:
            member.print()
    def implement(self, file):
        # implements loader
        file.write("#define _INIT_{}\n".format(self.classname))
        for member in self.members:
            file.write("a_value.getMember<{}>(\"{}\", a_toInit.{});\\\n".format(member.type, member.name, member.name))
        file.write("\n\n")
        # implements writer
        file.write("#define _SAVE_{}\n".format(self.classname))
        for member in self.members:
            file.write("a_value.saveMember<{}>(\"{}\", a_toInit.{});\\\n".format(member.type, member.name, member.name))

class BracketCounter:
    start = 0
    end = 0
    def isValid(self):
        return self.start > 0
    def isFinished(self):
        return self.isValid() and (self.start == self.end)

    def count(self, line):
        self.start += line.count('{')
        self.end += line.count('}')

class ParsedFile:
    def __init__(self, file):
        self.file = open(file)
        self.lines = self.file.readlines()
        self.lineCount = len(self.lines)
        self.lineIter = 0

    def nextLine(self):
        if self.lineIter >= self.lineCount:
            return ""
        line = self.lines[self.lineIter]
        self.lineIter += 1
        return line

    def nextTrimmedLine(self):
        return self.nextLine().strip()

    def atEnd(self):
        return self.lineIter >= self.lineCount

#def implementLoader(file, classname, parsedClass):
#    file.write("#define _INIT_{}\n".format(classname))
#    for member in parsedClass.members:
#        file.write("a_value.getMember<{}>(\"{}\", a_toInit.{});\\\n".format(member.type, member.name, member.name))


