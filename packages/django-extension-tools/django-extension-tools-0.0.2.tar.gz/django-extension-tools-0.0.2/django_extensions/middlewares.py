from django.conf import settings
from django.http import Http404
from django.utils.deprecation import MiddlewareMixin


def _get_client_ip(request) -> str:
    """ Get client ip address from request instance. We can fetch ip address
        from these classes.
        - django.core.handlers.wsgi.WSGIRequest
        - rest_framework.request.Request
    """
    ip: str
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class AdminIPRestrictionMiddleware(MiddlewareMixin):

    def __init__(self, get_response=None):
        self.get_response = get_response
        self.allowed_admin_ip_list = getattr(
            settings,
            'ALLOWED_ADMIN_IP_LIST',
            []
        )
        self.admin_app_name = 'admin'

    def process_view(self, request, view_func, view_args, view_kwargs):
        app_name: str = request.resolver_match.app_name

        if app_name == self.admin_app_name:
            ip: str = _get_client_ip(request)
            if ip not in self.allowed_admin_ip_list:
                raise Http404()
        return None
