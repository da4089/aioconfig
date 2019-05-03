

import asyncio
import aioconfig

from aioconfig import Container, Leaf, Manager, FUNCS


class Session:

    @aioconfig.create_element("sessions.*")
    def __init__(self, name: str):
        self._name = name
        self.sp1 = "sp1"
        self.sp2 = "sp2"
        return

    @aioconfig.set("sessions.*.sp1")
    def set_sp1(self, value):
        self.sp1 = value
        return

    @aioconfig.get("sessions.*.sp1")
    def get_sp1(self):
        return self.sp1

    @aioconfig.set("sessions.*.sp2")
    def set_sp2(self, value):
        self.sp2 = value
        return

    @aioconfig.get("sessions.*.sp2")
    def get_sp2(self):
        return self.sp2

    @aioconfig.delete("sessions.*")
    def destroy(self):
        return


class Server:

    @aioconfig.create_object("server")
    def __init__(self):
        self.p1 = 1
        self.p2 = "two"

        self.loop = asyncio.get_event_loop()
        self.manager = Manager()
        return

    @aioconfig.set("server.p1")
    def set_p1(self, value):
        self.p1 = value
        return

    @aioconfig.get("server.p1")
    def get_p1(self):
        return self.p1

    @aioconfig.set("server.p2")
    def set_p2(self, value):
        self.p2 = value
        return

    @aioconfig.get("server.p2")
    def get_p2(self):
        return self.p2

    @aioconfig.create_child("sessions")
    def create_session(self, name):
        session = Session(name)
        self._sessions[name] = session
        return session

    def init_manager(self, do_init=False):
        if do_init:
            running = self.manager.get_node('config.running')
            server = self.create_server(running)
            self.create_p1(server)
            self.create_p2(server)

        else:
            self.manager.load("sqlite3://test.db")

        return

    # FIXME: try to get rid of these!

    def create_server(self, parent: Container):
        return parent.add_child(Container("server"))

    def create_p1(self, parent: Container):
        return parent.add_child(SimpleLiveLeaf("p1", parent, self.get_p1))

    def create_p2(self, parent: Container):
        return parent.add_child(P2Node("p2", parent, self))

    def run(self):
        self.loop.run_forever()
        return


# FIXME: this should be elsewhere, I guess?!

class SimpleLiveLeaf(Leaf):

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


# FIXME: this should remain an option: a dedicated class to manage a node.

class P2Node(Leaf):

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

    print(FUNCS)