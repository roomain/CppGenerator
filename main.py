import sys
import parsing_class as PC
from pathlib import Path


print("Class Generator - {}".format(sys.argv))
print("parse header files and generate custom json serializer")
if len(sys.argv) > 1:
    print("Parse headers from {}".format(sys.argv[1]))
    parsedFilelist = []
    for filepath in Path(sys.argv[1]).rglob('*.h'):
        parser = PC.HeaderParser(filepath)
        parser.parse()
        parsedFilelist.append(parser)

    for parser in parsedFilelist:
        parser.implementLoader()
else:
    print("Missing argument")