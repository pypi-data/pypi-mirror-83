# -*- coding: UTF-8 -*-

import typing

import sentry_sdk
import tornado.web
import tornado.ioloop
from apispec import APISpec
from tornado.options import define, options

from tornado_widgets.handler import WidgetsJSON404Handler
from tornado_widgets.log import generate_widgets_default_log_request
from tornado_widgets.router import Router
from tornado_widgets.sentry import TornadoWidgetsIntegration
from tornado_widgets.utils import default_random_nonce_func


class App(object):

    def __init__(self, *, name: str, config: typing.Any = None,
                 settings: dict = None):

        self.name = name
        self._config_options(config=config)

        self.loop = None
        self.application = None
        self.settings = dict(
            debug=options.debug,
            gzip=True,
            log_function=generate_widgets_default_log_request(
                app_name=self.name),
            default_handler_class=WidgetsJSON404Handler,
            default_handler_args=dict(status_code=404),
            random_nonce_func=default_random_nonce_func,
        )
        if settings:
            self.settings.update(**settings)
        self.prepare_funcs = []
        self.routers = []
        self.spec = None

    @staticmethod
    def _config_options(*, config):
        define(name='debug', default=config.DEBUG, type=bool)
        define(name='port', default=config.PORT, type=int)
        sentry_default = getattr(config, 'WIDGETS_SENTRY_DSN', '')
        define(name='widgets-sentry-dsn', default=sentry_default, type=str)
        widgets_success_code = getattr(config, 'WIDGETS_SUCCESS_CODE', 0)
        define(name='widgets-success-code', default=widgets_success_code,
               type=int)
        widgets_force_extra = getattr(config, 'WIDGETS_FORCE_EXTRA', False)
        define(name='widgets-force-extra', default=widgets_force_extra,
               type=bool)
        widgets_simple_stat_influxdb_dsn = getattr(
            config, 'WIDGETS_SIMPLE_STAT_INFLUXDB_DSN', '')
        define(name='widgets-simple-stat-influxdb-dsn',
               default=widgets_simple_stat_influxdb_dsn, type=str)
        options.parse_command_line()

    def register_router(self, *, route_obj: Router):
        self.routers.append(route_obj)

    def register_spec(self, *, spec_obj: APISpec):
        self.spec = spec_obj

    def register_prepare_func(self, *, func):
        self.prepare_funcs.append(func)

    @property
    def _route_as_list(self):
        result = []
        for item in self.routers:
            result.extend([(k, v) for k, v in item.route_mapper.items()])
        return result

    def _gen_swagger_handler(self, routes):
        for r in routes:
            self.spec.path(urlspec=r)

        spec = self.spec
        from tornado_widgets.handler import JSONHandler

        class SwaggerHandler(JSONHandler):
            async def get(self):
                self.write(spec.to_dict())
        return SwaggerHandler

    def run(self, *, use_uvloop: bool = True):
        if use_uvloop:
            import asyncio
            import uvloop
            asyncio.set_event_loop_policy(policy=uvloop.EventLoopPolicy())
        self.loop = tornado.ioloop.IOLoop.current()
        for item in self.prepare_funcs:
            self.loop.run_sync(func=item)
        route_as_list = self._route_as_list
        if options.debug and self.spec:
            route_as_list.append(
                ('/swagger.json',
                 self._gen_swagger_handler(routes=route_as_list)))
        self.application = tornado.web.Application(
            handlers=route_as_list, **self.settings)
        self.application.listen(port=options.port)
        sentry_dsn = options.widgets_sentry_dsn
        if sentry_dsn:
            sentry_sdk.init(
                dsn=sentry_dsn, integrations=[TornadoWidgetsIntegration()],
                default_integrations=False)
        self.loop.start()
