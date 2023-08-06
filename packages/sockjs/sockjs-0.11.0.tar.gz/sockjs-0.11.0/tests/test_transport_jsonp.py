from unittest import mock

from aiohttp import web

import pytest
from aiohttp.test_utils import make_mocked_coro

from sockjs.transports import jsonp


@pytest.fixture
def make_transport(make_request, make_manager, make_handler, make_fut):
    def maker(method="GET", path="/", query_params={}):
        handler = make_handler(None)
        manager = make_manager(handler)
        request = make_request(method, path, query_params=query_params)
        session = manager.get("TestSessionJsonP", create=True, request=request)
        request.app.freeze()
        return jsonp.JSONPolling(manager, session, request)

    return maker


async def test_streaming_send(make_transport):
    trans = make_transport()
    trans.callback = "cb"

    resp = trans.response = mock.Mock()
    resp.write = make_mocked_coro(None)
    stop = await trans.send("text data")
    resp.write.assert_called_with(b'/**/cb("text data");\r\n')
    assert stop


async def test_process(make_transport, make_fut):
    transp = make_transport(query_params={"c": "calback"})
    transp.handle_session = make_fut(1)
    resp = await transp.process()
    assert transp.handle_session.called
    assert resp.status == 200


async def test_process_no_callback(make_transport, make_fut):
    transp = make_transport()
    transp.session = mock.Mock()
    transp.session._remote_closed = make_fut(1)

    resp = await transp.process()
    assert transp.session._remote_closed.called
    assert resp.status == 500


async def test_process_bad_callback(make_transport, make_fut):
    transp = make_transport(query_params={"c": "calback!!!!"})
    transp.session = mock.Mock()
    transp.session._remote_closed = make_fut(1)

    resp = await transp.process()
    assert transp.session._remote_closed.called
    assert resp.status == 500


async def test_process_not_supported(make_transport):
    transp = make_transport(method="PUT")
    resp = await transp.process()
    assert resp.status == 400


async def xtest_process_bad_encoding(make_transport, make_fut):
    transp = make_transport(method="POST")
    transp.request.read = make_fut(b"test")
    transp.request.content_type
    transp.request._content_type = "application/x-www-form-urlencoded"
    resp = await transp.process()
    assert resp.status == 500


async def xtest_process_no_payload(make_transport, make_fut):
    transp = make_transport(method="POST")
    transp.request.read = make_fut(b"d=")
    transp.request.content_type
    transp.request._content_type = "application/x-www-form-urlencoded"
    resp = await transp.process()
    assert resp.status == 500


async def xtest_process_bad_json(make_transport, make_fut):
    transp = make_transport(method="POST")
    transp.request.read = make_fut(b"{]")
    resp = await transp.process()
    assert resp.status == 500


async def xtest_process_message(make_transport, make_fut):
    transp = make_transport(method="POST")
    transp.session._remote_messages = make_fut(1)
    transp.request.read = make_fut(b'["msg1","msg2"]')
    resp = await transp.process()
    assert resp.status == 200
    transp.session._remote_messages.assert_called_with(["msg1", "msg2"])


async def test_session_has_request(make_transport, make_fut):
    transp = make_transport(method="POST")
    transp.session._remote_messages = make_fut(1)
    assert isinstance(transp.session.request, web.Request)
