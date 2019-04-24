

from aioconfig import Container, Leaf, Manager


class Server:
    def __init__(self):
        self.p1 = 1
        self.p2 = "two"
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

    def __init__(self,name, parent, server):
        super().__init__(name, parent)
        self._server = server
        return

    def get(self):
        return self._server.get_p2()


def test_construct():

    s = Server()

    m = Manager()
    running = m.get_node('config.running')
    server = Container('server')
    running.add_child(server)

    p1 = SimpleLiveLeaf('p1', server, s.get_p1, None, None)
    server.add_child(p1)

    p2 = P2Node('p2', server, s)
    server.add_child(p2)
