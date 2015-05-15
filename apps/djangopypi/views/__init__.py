from logging import getLogger

from django.http import HttpResponseNotAllowed

from djangopypi.decorators import csrf_exempt
from djangopypi.http import parse_distutils_request
from djangopypi.views.xmlrpc import parse_xmlrpc_request
from djangopypi.settings import FALLBACK_VIEW, ACTION_VIEWS
from djangopypi.utils import import_item

log = getLogger('djangopypi.views')


@csrf_exempt
def root(request, fallback_view=None, **kwargs):
    """ Root view of the package index, handle incoming actions from distutils
    or redirect to a more user friendly view """
    if request.method == 'POST':
        if request.META['CONTENT_TYPE'] == 'text/xml':
            log.debug('XMLRPC request received')
            return parse_xmlrpc_request(request)
        log.debug('Distutils request received')
        parse_distutils_request(request)
        action = request.POST.get(':action', '')
        action = action.strip()
    else:
        action = request.GET.get(':action', '')
        action = action.strip()

    if not action:
        log.debug('No action in root view')
        if fallback_view is None:
            fallback_view = import_item(FALLBACK_VIEW)
        return fallback_view.as_view()(request, **kwargs)

    if action not in ACTION_VIEWS:
        log.error('Invalid action encountered: %s' % (action,))
        return HttpResponseNotAllowed(ACTION_VIEWS.keys())

    log.debug('Applying configured action view for %s' % (action,))
    action_view = import_item(ACTION_VIEWS[action])
    return action_view(request, **kwargs)
