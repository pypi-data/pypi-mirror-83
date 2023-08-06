import dis


class ServerVerifier(type):

    def __init__(self, clsname, bases, clsdict):

        methods = []

        for func in clsdict:

            try:
                ret = dis.get_instructions(clsdict[func])

            except TypeError:
                pass
            else:

                for i in ret:

                    if i.opname == "LOAD_METHOD":
                        if i.argval not in methods:
                            methods.append(i.argval)

        if 'connect' in methods:
            raise TypeError("The 'connect' "
                            "method is restricted on server side!")
        # print(methods)
        super().__init__(clsname, bases, clsdict)

