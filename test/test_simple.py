

import asyncio

from aioconfig import Object, Property, Manager, FUNCS


class Session:

    def __init__(self, name: str):
        self._name = name
        self.sp1 = "sp1"
        self.sp2 = "sp2"
        return

    def set_sp1(self, value):
        self.sp1 = value
        return

    def get_sp1(self):
        return self.sp1

    def set_sp2(self, value):
        self.sp2 = value
        return

    def get_sp2(self):
        return self.sp2

    def destroy(self):
        return


class Server:

    def __init__(self):
        self.p1 = 1
        self.p2 = "two"

        self.sessions = {}

        self.loop = asyncio.get_event_loop()
        self.manager = Manager()
        return

    def set_p1(self, value):
        self.p1 = value
        return

    def get_p1(self):
        return self.p1

    def set_p2(self, value):
        self.p2 = value
        return

    def get_p2(self):
        return self.p2

    def create_session(self, name):
        session = Session(name)
        self.sessions[name] = session
        return session

    def init_manager(self, do_init=False):
        if do_init:
            running = self.manager.get_node('config.running')
            server = self.create_server(running)
            self.create_p1(server)
            self.create_p2(server)
            self.create_sessions(running)

        else:
            self.manager.load("sqlite3://test.db")

        return

    def create_server(self, parent: Object):
        return parent.add_child(Object("server"))

    def create_sessions(self, parent: Object):
        return parent.add_child(Object("sessions"))

    def create_p1(self, parent: Object):
        return parent.add_child(SimpleLiveProperty("p1", parent, self.get_p1))

    def create_p2(self, parent: Object):
        return parent.add_child(P2Node("p2", parent, self))

    def run(self):
        self.loop.run_forever()
        return


class SimpleLiveProperty(Property):

    def __init__(self, name, parent, getter, setter=None, deleter=None):
        super().__init__(name, parent)
        self._set = setter
        self._get = getter
        self._del = deleter
        return

    def get(self) -> object:
        return self._get()

    def set(self, value):
        return self._set(value)

    def delete(self):
        return self._del()


class P2Node(Property):

    def __init__(self, name, parent, server):
        super().__init__(name, parent)
        self._server = server
        return

    def get(self):
        return self._server.get_p2()


def test_construct():
    s = Server()
    s.init_manager(True)
    #s.run()

