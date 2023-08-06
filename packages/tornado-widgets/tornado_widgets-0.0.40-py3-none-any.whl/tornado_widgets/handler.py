# -*- coding: UTF-8 -*-

from typing import Optional, Awaitable, Callable

import orjson
import tornado.web
from marshmallow import Schema
from marshmallow.exceptions import MarshmallowError, ValidationError
from tornado import httputil
from tornado.log import access_log
from tornado.options import options

from tornado_widgets.error import BaseError, WidgetsParameterError
from tornado_widgets.utils import default_random_nonce_func


class BaseHandler(tornado.web.RequestHandler):

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        raise NotImplemented    # NOQA

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.random_nonce = self.settings.get(
            'random_nonce_func', default_random_nonce_func)()
        self.headers = dict()
        self.query_args = dict()
        self.form_data = dict()
        self.json_body = dict()

    def options(self, *args, **kwargs) -> None:
        access_log.info('OPTIONS CALLED: %s, %s', args, kwargs)
        self.set_status(204)

    def set_default_headers(self) -> None:
        if options.debug:
            self.set_header('Access-Control-Allow-Origin', '*')
            self.set_header('Access-Control-Allow-Methods',
                            'GET, POST, PUT, DELETE, OPTIONS, HEAD, PATCH')
            self.set_header('Access-Control-Max-Age', '3600')
            self.set_header('Access-Control-Allow-Headers',
                            'Content-Type, Access-Control-Allow-Headers')

    def get_headers(self) -> dict:
        return dict(self.request.headers.get_all())

    @staticmethod
    def _decode(*, src, schema: Schema = None) -> dict:
        result = dict()
        for key, value in src.items():
            result[key] = [item.decode() for item in value]
            if len(result[key]) == 1:
                result[key] = result[key][0]
        if schema:
            return schema.load(result)
        return result

    def get_query_args(self, *, schema: Schema = None) -> dict:
        return self._decode(src=self.request.query_arguments, schema=schema)

    def get_form_data(self, *, schema: Schema = None) -> dict:
        return self._decode(src=self.request.body_arguments, schema=schema)

    def get_json_body(self, schema: Schema = None) -> dict:
        content_type = self.request.headers.get('Content-Type')
        if not content_type:
            return dict()
        if not content_type.startswith('application/json'):
            return dict()
        try:
            result = orjson.loads(self.request.body or b'{}')
        except orjson.JSONDecodeError:
            raise WidgetsParameterError
        if schema:
            return schema.load(result)
        return result

    def widgets_get_argument(self, key, casting_func: Callable = None):
        source = ['query_args', 'form_data', 'json_body']
        for s in source:
            value = getattr(self, s, dict()).get(key)
            if value:
                return casting_func(value)


class JSONHandler(BaseHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widgets_extra = dict()
        self.json_result = None

    def set_extra(self, *, extra: dict = None) -> None:
        if extra:
            self.widgets_extra.update(**extra)

    def write_json(self, data: dict = None, code: int = None, msg: str = None,
                   http_status: int = 200) -> None:
        code = code if code is not None else options.widgets_success_code
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.set_status(http_status)
        result = dict(code=code, msg=msg, data=data, _extra=self.widgets_extra)
        if (not options.widgets_force_extra) and (not self.widgets_extra):
            del result['_extra']
        self.json_result = result
        result_bytes = orjson.dumps(
            result, option=(orjson.OPT_SORT_KEYS | orjson.OPT_STRICT_INTEGER),
        ).replace(b'</', b'<\\/')
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.finish(chunk=result_bytes)

    def write_error(self, status_code: int, **kwargs) -> None:
        default = dict(
            code=1000,
            msg='内部错误',
            data=None,
            http_status=status_code,
        )
        if 'exc_info' in kwargs:
            _, err_instance, traceback = kwargs['exc_info']
            if isinstance(err_instance, MarshmallowError):
                self.write_json(
                    code=1001,
                    msg='参数异常',
                    data=(err_instance.normalized_messages()
                          if isinstance(err_instance, ValidationError)
                          else err_instance.args),
                    http_status=400,
                )
            elif isinstance(err_instance, BaseError):
                self.write_json(
                    code=err_instance.code,
                    msg=err_instance.msg,
                    data=err_instance.data,
                    http_status=err_instance.http_status,
                )
            elif isinstance(err_instance, tornado.web.HTTPError):
                self.write_json(
                    code=err_instance.status_code,
                    msg=err_instance.reason or httputil.responses.get(
                        err_instance.status_code, 'Unknown'),
                    data=None,
                    http_status=err_instance.status_code,
                )
            else:
                self.write_json(**default)
        else:
            self.write_json(**default)


class WidgetsJSON404Handler(JSONHandler):

    def initialize(self, status_code: int) -> None:
        self.set_status(status_code)

    def prepare(self) -> None:
        raise tornado.web.HTTPError(self._status_code)
