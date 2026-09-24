import ipaddress
import logging
from aiohttp import web

log = logging.getLogger(__name__)


def is_loopback_host(host: str) -> bool:
    if host.lower() == 'localhost':
        return True
    try:
        return ipaddress.ip_address(host.strip('[]')).is_loopback
    except ValueError:
        return False


def is_api_binding_safe(conf) -> bool:
    return conf.allowed_origin != '*' or is_loopback_host(conf.api_host)


def ensure_request_allowed(request, conf):
    if is_request_allowed(request, conf):
        return
    if conf.allowed_origin:
        log.warning(
            "API requests with Origin '%s' are not allowed, "
            "configuration 'allowed_origin' limits requests to: '%s'",
            request.headers.get('Origin'), conf.allowed_origin
        )
    else:
        log.warning(
            "API requests with Origin '%s' are not allowed, "
            "update configuration 'allowed_origin' to enable this origin.",
            request.headers.get('Origin')
        )
    raise web.HTTPForbidden()


def is_request_allowed(request, conf) -> bool:
    origin = request.headers.get('Origin')
    return (
        origin is None or
        origin == conf.allowed_origin or
        conf.allowed_origin == '*'
    )
