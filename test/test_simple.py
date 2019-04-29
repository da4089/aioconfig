

import asyncio

from aioconfig import Container, Leaf, Manager


class Server:
    def __init__(self):
        self.p1 = 1
        self.p2 = "two"

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

    def init_manager(self, do_init=False):
        if do_init:
            running = self.manager.get_node('config.running')
            server = self.create_running_node("server", running)
            self.create_running_node("server.p1", server)
            self.create_running_node("server.p2", server)

        else:
            self.manager.load("sqlite3://test.db")

        return

    def create_running_node(self, name, parent):
        if name == "server":
            server = Container('server')
            parent.add_child(server)
            return server

        elif name == "server.p1":
            p1 = SimpleLiveLeaf('p1', parent, self.get_p1, None, None)
            parent.add_child(p1)
            return p1

        elif name == "server.p2":
            p2 = P2Node('p2', parent, self)
            parent.add_child(p2)
            return p2

        return

    def run(self):
        self.loop.run_forever()
        return


class SimpleLiveLeaf(Leaf):

    def __init__(self, name, parent, getter, setter, deleter):
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
    s.run()
