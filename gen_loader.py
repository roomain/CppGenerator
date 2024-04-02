##define INIT_IMPL(classname) \
#public: \
#   static inline void init(classname& a_toInit, const Class& a_value) \
#   { _INIT_##classname(a_toInit, a_value) }
def implementLoader(file, classname, parsedClass):
    file.write("#define _INIT_{}\n".format(classname))
    for member in parsedClass.members:
        file.write("a_value.getMember<{}>(\"{}\", a_toInit.{});\\\n".format(member.type, member.name, member.name))


