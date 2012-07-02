import urlparse
import oauth2 as oauth
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

CONSUMER = oauth.Consumer(settings.GITHUB_ID, settings.GITHUB_SECRET)
CLIENT = oauth.Client(CONSUMER)

PARAMS = {
    'client_id': settings.GITHUB_ID,
    'scope': 'repo',
    'redirect_url': 'http://callowayproject.com/authorize/',
}

URL_PARAMS = '&'.join(['%s=%s' % (k, v) for k, v in PARAMS.items()])
AUTHORIZE_URL = 'https://github.com/login/oauth/authorize?%s' % URL_PARAMS

GITHUB_SECRET = settings.GITHUB_SECRET

# consumer = oauth.Consumer(consumer_key, consumer_secret)
# client = oauth.Client(consumer)

# Redirect to github authorize
def get_auth(request):
    return HttpResponseRedirect(AUTHORIZE_URL)

def authorize(request):
    if request.REQUEST.has_key('code'):
        code = request.REQUEST['code']
        