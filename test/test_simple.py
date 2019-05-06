

import asyncio

from aioconfig import List, Object, Property, Manager


################################################################
# Test application

class Session:

    def __init__(self, server: 'Server', name: str):
        self._server = server
        self._name = name
        self.sp1 = "sp1"
        self.sp2 = "sp2"

        self.dead = False
        self.task = asyncio.ensure_future(self.process())
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
        self.dead = True
        return

    async def process(self):
        while not self.dead:
            print(self._name)
            await asyncio.sleep(1)

        return


class Server:

    def __init__(self):
        self.p1 = 1
        self.p2 = "two"
        self.sessions = {}

        self.loop = asyncio.get_event_loop()
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
        session = Session(self, name)
        self.sessions[name] = session
        return session


################################################################
# Management classes

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


class SessionManager(Object):

    def __init__(self, name, parent, session):
        super().__init__(name, parent)
        self._session = session

        self.add_child(SimpleLiveProperty("sp1", self,
                                          session.get_sp1,
                                          session.set_sp1))

        self.add_child(SimpleLiveProperty("sp2", self,
                                          session.get_sp2,
                                          session.set_sp2))
        return


class SessionsManager(List):

    def __init__(self, name, parent):
        super().__init__(name, parent)
        return

    def add_session(self, name):
        pass

    def delete_session(self, name):
        pass

    def get_sessions(self):
        pass

    def get_session(self, index: int):
        pass


class ServerManager(Object):
    pass


################################################################
# Test functions

async def sequence(server, manager):

    await asyncio.sleep(5)

    sessions: List = manager.get_node('config.running.sessions')

    session = Session(server, "sa")
    session_manager = SessionManager("sa", sessions, session)
    sessions.append_child(session_manager)

    await asyncio.sleep(5)

    return


def test_construct():

    s = Server()
    m = Manager()

    running = m.get_node('config.running')
    server = running.add_child(Object("server", running))
    server.add_child(SimpleLiveProperty("p1", server, s.get_p1))
    server.add_child(P2Node("p2", server, s))
    running.add_child(List("sessions", running))

    m.add_access("rest://0.0.0.0:443")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(m.start())
    loop.run_until_complete(sequence(s, m))
    loop.run_until_complete(m.stop())


if __name__ == "__main__":
    test_construct()