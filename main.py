import sys
import parsing_class
from pathlib import Path



class Generated:
    def __init__(self, file, directory):
        self.filepath = file
        self.directory = directory
        self.valid = False
        self.memberList = []

    def findClassname(self, wordlist):
        if len(wordlist) < 3:
            return wordlist[1]
        else:
            return wordlist[2]
    def findClass(self, index, lineCount, lines):
        line = lines[index].strip()
        while not (line.startswith("class")) and index < lineCount:
            if line.startswith("template"):
                return ""
            elif line.startswith("//"):
                index += 1
            elif line.startswith("/*"):
                index += 1
                while not (line.endsWith("*/")) and index < lineCount:
                    line = lines[index].strip()
                    index += 1
            line = lines[index].strip()
            index += 1

        if index < lineCount:
            return self.findClassname(line.split())

    def findMemberData(self, wordlist):
        if len(wordlist) >= 2:
            member = GeneratedMember()
            member.type = wordlist[0]
            member.name = wordlist[1][:len(wordlist[1]) - 1]
            return member

    def findMember(self, index, lineCount, lines):
        index += 1
        member = GeneratedMember()
        while (member.type == "") and index < lineCount:
            line = lines[index].strip()
            if line.startswith("//"):
                index += 1
            elif line.startswith("/*"):
                index += 1
                while not (line.endsWith("*/")) and index < lineCount:
                    line = lines[index].strip()
                    index += 1
            else:
                member = self.findMemberData(line.split())
            index += 1
        return member

    def parse(self):
        file = open(self.filepath)
        lines = file.readlines()
        lineCount = len(lines)
        index = 0
        while index < lineCount:
            line = lines[index].strip()
            if line.startswith("CLASS_DEF"):
                self.classname = self.findClass(index, lineCount, lines)
            elif line.startswith("MEMBER_DEF"):
                self.memberList.append(self.findMember(index, lineCount, lines))
            index += 1

    def print(self):
        print("--------------------------------------------")
        print(self.classname)
        for member in self.memberList:
            print(member.str())


def getHeaders(directory):
    for filepath in Path(directory).rglob('*.h'):
        print("Parse headers: {}".format(filepath))
        generatedClass = Generated(filepath, filepath.parent)
        generatedClass.parse()
        generatedClass.print()


print("Class Generator - {}".format(sys.argv))
print("parse header files and generate custom json serializer")
if len(sys.argv) > 1:
    print("Parse headers from {}".format(sys.argv[1]))
    getHeaders(sys.argv[1])
else:
    print("Missing argument")
