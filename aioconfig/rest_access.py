# -*- coding: utf-8 -*-
########################################################################
# aioconfig
# Copyright (C) 2019, David Arnold.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
########################################################################

import aiohttp.web
import aiohttp_cors
import ssl

from .access import AccessAdaptor


class RestAccessAdaptor(AccessAdaptor):
    def __init__(self, manager, loop, config):
        """Constructor.

        :param manager: Reference to Manager to access.
        :param loop: Event loop.
        :param config: Path to adaptor configuration."""

        super().__init__(manager, loop, config)

        self._app = None
        self._cors = None
        self._runner = None
        self._site = None

        self._port = 443

        self._root = None
        return

    async def start(self):
        """Start the accessor running."""

        try:
            self._app = aiohttp.web.Application()
            self._cors = aiohttp_cors.setup(
                self._app,
                defaults={
                    "*": aiohttp_cors.ResourceOptions(
                        allow_methods=["GET", "PUT", "POST", "DELETE"],
                        allow_credentials=True,
                        expose_headers="*",
                        allow_headers="*")})

            self._cors.add(self._app.router.add_route("GET",
                                                      "/{tail:.*}",
                                                      self.handle))
            self._cors.add(self._app.router.add_route("PUT",
                                                      "/{tail:.*}",
                                                      self.handle))
            self._cors.add(self._app.router.add_route("POST",
                                                      "/{tail:.*}",
                                                      self.handle))
            self._cors.add(self._app.router.add_route("DELETE",
                                                      "/{tail:.*}",
                                                      self.handle))

            ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            ssl_context.load_cert_chain('domain_srv.crt', 'domain_srv.key')

            self._runner = aiohttp.web.AppRunner(self._app)
            await self._runner.setup()

            self._site = aiohttp.web.TCPSite(self._runner,
                                             host="0.0.0.0",
                                             port=self._port,
                                             ssl_context=ssl_context)
            await self._site.start()

        except:
            pass

        return

    async def stop(self):
        """Stop running this accessor."""

        if self._site:
            await self._site.stop()
            self._site = None

        if self._runner:
            await self._runner.cleanup()
            self._runner = None

        if self._app:
            await self._app.shutdown()
            await self._app.cleanup()
            self._app = None

        return

    async def change_port(self, new_port: int):
        pass

    async def handle(self, request):
        if request.path == '/':
            path = []
        else:
            path = request.path[1:].split('/')

        return await self._root.handle(path, request)
