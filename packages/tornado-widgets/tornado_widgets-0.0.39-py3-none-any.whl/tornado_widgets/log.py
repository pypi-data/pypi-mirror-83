# -*- coding: UTF-8 -*-

from datetime import datetime, timedelta

import chardet
import orjson
import requests
from tornado.options import options
from tornado.log import access_log, app_log

from tornado_widgets.handler import BaseHandler

try:
    from influxdb_client import InfluxDBClient, Point
    from influxdb_client.client.bucket_api import BucketsApi
    from influxdb_client.client.write_api import WriteApi, ASYNCHRONOUS
except ImportError:
    app_log.warning(
        'The InfluxDB Python Driver not installed. '
        'Widgets Simple Stat InfluxDB Module will NEVER be loaded.')
    InfluxDBClient, Point, BucketsApi, WriteApi, ASYNCHRONOUS = (
        None, None, None, None, None)


class InfluxDBHelper(object):

    def __init__(self, app_name: str):
        self._app_name = app_name
        self._client = InfluxDBClient(
            url=options.widgets_simple_stat_influxdb_dsn.replace(
                'influxdb://', 'http://'),
            token='', org='', enable_gzip=True, timeout=1000)
        self._buckets_api = self._client.buckets_api()
        self._query_api = self._client.query_api()
        self._write_api = self._client.write_api(write_options=ASYNCHRONOUS)
        self._bucket_is_valid = False
        self._check_bucket_time = None

    def _http_create_bucket(self):
        try:
            requests.Session()
            response = requests.post(
                url=f'{self._client.url}/query?q='
                    f'CREATE DATABASE widgets_stat_{self._app_name}')
            return 300 > response.status_code >= 200
        except Exception as e:
            app_log.warning('Bucket Create Exception: ', e)
            return False

    def _ensure_bucket(self):
        now = datetime.now()
        if not self._check_bucket_time:
            self._bucket_is_valid = self._http_create_bucket()
            self._check_bucket_time = now
        elif self._check_bucket_time + timedelta(minutes=1) < now:
            self._bucket_is_valid = self._http_create_bucket()
            self._check_bucket_time = now

    def write_point(self, point: Point):
        self._ensure_bucket()
        if self._bucket_is_valid:
            self._write_api.write(
                bucket=f'widgets_stat_{self._app_name}', record=point)


def _simple_stat_influxdb(app_name, handler):
    _influxdb = getattr(_simple_stat_influxdb, '_influxdb', None)
    if not _influxdb:
        _simple_stat_influxdb._influxdb = InfluxDBHelper(app_name=app_name)
    _influxdb: InfluxDBHelper = getattr(
        _simple_stat_influxdb, '_influxdb', None)
    try:
        point = Point(measurement_name='request').tag(
            key='path', value=handler.request.path,
        ).tag(
            key='method', value=handler.request.method,
        ).tag(
            key='status', value=handler.get_status(),
        ).field(
            field='random_nonce', value=handler.random_nonce,
        ).field(
            field='ip', value=handler.request.remote_ip,
        ).field(
            field='latency', value=handler.request.request_time(),
        )
        _influxdb.write_point(point=point)
    except Exception as e:
        app_log.warning('Simple Stat InfluxDB Module Write Points Error: ', e)


def generate_widgets_default_log_request(app_name: str):

    def log_request(handler: BaseHandler):
        if handler.get_status() < 400:
            log_method = access_log.info
        elif handler.get_status() < 500:
            log_method = access_log.warning
        else:
            log_method = access_log.error
        request_time = 1000.0 * handler.request.request_time()

        headers = orjson.dumps(
            dict(handler.request.headers.get_all()),
            option=orjson.OPT_SORT_KEYS | orjson.OPT_STRICT_INTEGER)
        if headers:
            log_method(f'[{handler.random_nonce}] HEADERS: {headers.decode()}')
        query = handler.request.query
        if query:
            log_method(f'[{handler.random_nonce}] QUERY: {query}')
        if handler.request.method.upper() not in ('GET', 'OPTIONS'):
            content_type = handler.request.headers.get('Content-Type', '')
            if not content_type:
                log_method(f'[{handler.random_nonce}] '
                           f'BODY: **HIDDEN (Missing Content-Type)**')
            elif content_type.lower().startswith('multipart/form-data'):
                log_method(f'[{handler.random_nonce}] '
                           f'BODY: **HIDDEN (multipart/form-data Detected)**')
            else:
                body = handler.request.body
                if body:
                    encoding = chardet.detect(body)['encoding'] or 'utf-8'
                    try:
                        log_method(f'[{handler.random_nonce}] '
                                   f'BODY: {body.decode(encoding=encoding)}')
                    except UnicodeDecodeError:
                        try:
                            log_method(f'[{handler.random_nonce}] '
                                       f'BODY: {body.decode()}')
                        except UnicodeDecodeError:
                            log_method(
                                f'[{handler.random_nonce}] '
                                f'BODY: **HIDDEN (UnicodeDecodeError)**')

        log_method(
            f'[{handler.random_nonce}] ' '%d %s %.2fms',
            handler.get_status(),
            handler._request_summary(),     # NOQA
            request_time,
        )

        if InfluxDBClient and options.widgets_simple_stat_influxdb_dsn:
            _simple_stat_influxdb(app_name=app_name, handler=handler)

    return log_request
