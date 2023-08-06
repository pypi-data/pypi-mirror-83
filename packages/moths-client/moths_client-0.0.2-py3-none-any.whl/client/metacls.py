import dis


class ClientVerifier(type):

    def __init__(self, clsname, bases, clsdict):

        methods = []
        for func in clsdict:

            try:
                ret = dis.get_instructions(clsdict[func])

            except TypeError:
                pass
            else:
                for i in ret:
                    if i.opname == "LOAD_ATTR" or i.opname == "LOAD_METHOD":
                        if i.argval not in methods:
                            methods.append(i.argval)

        for command in ('accept', 'listen'):
            if command in methods:
                raise TypeError('Restricted methods spotted!')

        if 'read' in methods or 'send' in methods or 'presence' in methods:
            pass
        else:
            raise TypeError('No socket operations found!')
        # print(methods)
        super().__init__(clsname, bases, clsdict)
