"""jsonp transport"""
import re
from urllib.parse import unquote_plus

from aiohttp import web, hdrs

from .base import StreamingTransport
from .utils import CACHE_CONTROL, session_cookie, cors_headers
from ..protocol import dumps, loads, ENCODING


class JSONPolling(StreamingTransport):

    check_callback = re.compile(r"^[a-zA-Z0-9_\.]+$")
    callback = ""

    async def send(self, text):
        data = "/**/%s(%s);\r\n" % (self.callback, dumps(text))
        await self.response.write(data.encode(ENCODING))
        return True

    async def process(self):
        session = self.session
        request = self.request
        meth = request.method

        if request.method == hdrs.METH_GET:
            try:
                callback = self.callback = request.query.get("c")
            except Exception:
                callback = self.callback = request.GET.get("c")

            if not callback:
                await self.session._remote_closed()
                return web.HTTPInternalServerError(text='"callback" parameter required')

            elif not self.check_callback.match(callback):
                await self.session._remote_closed()
                return web.HTTPInternalServerError(text='invalid "callback" parameter')

            headers = (
                (hdrs.CONTENT_TYPE, "application/javascript; charset=UTF-8"),
                (hdrs.CACHE_CONTROL, CACHE_CONTROL),
            )
            headers += session_cookie(request)
            headers += cors_headers(request.headers)

            resp = self.response = web.StreamResponse(headers=headers)
            await resp.prepare(request)

            await self.handle_session()
            return resp

        elif request.method == hdrs.METH_POST:
            data = await request.read()

            ctype = request.content_type.lower()
            if ctype == "application/x-www-form-urlencoded":
                if not data.startswith(b"d="):
                    return web.HTTPInternalServerError(text="Payload expected.")

                data = unquote_plus(data[2:].decode(ENCODING))
            else:
                data = data.decode(ENCODING)

            if not data:
                return web.HTTPInternalServerError(text="Payload expected.")

            try:
                messages = loads(data)
            except Exception:
                return web.HTTPInternalServerError(text="Broken JSON encoding.")

            await session._remote_messages(messages)

            headers = (
                (hdrs.CONTENT_TYPE, "text/html;charset=UTF-8"),
                (hdrs.CACHE_CONTROL, CACHE_CONTROL),
            )
            headers += session_cookie(request)
            return web.Response(body=b"ok", headers=headers)

        else:
            return web.HTTPBadRequest(text="No support for such method: %s" % meth)
