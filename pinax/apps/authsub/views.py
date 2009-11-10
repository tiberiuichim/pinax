from django.core.urlresolvers import reverse
from django.http import get_host
from django.utils.html import escape
from gdata.auth import extract_auth_sub_token_from_url
import gdata.contacts.service

from django.http import HttpResponseRedirect

## based on http://www.djangosnippets.org/snippets/706/

GOOGLE_CONTACTS_URI = 'http://www.google.com/m8/feeds/'

def get_url_host(request):
    if request.is_secure():
        protocol = 'https'
    else:
        protocol = 'http'
    host = escape(get_host(request))
    return '%s://%s' % (protocol, host)

def get_full_url(request):
    return get_url_host(request) + request.get_full_path()

def get_auth_sub_url(next):
    scope = GOOGLE_CONTACTS_URI
    secure = False
    session = True
    contacts_service = gdata.contacts.service.ContactsService()
    return contacts_service.GenerateAuthSubURL(next, scope, secure, session);

def login(request, redirect_to=None):
    if redirect_to is None:
        redirect_to = reverse('invitations_contacts')
    if "token" in request.GET:
        # add token to session for now
        #request.session['authsub_token'] = request.GET["token"]
        single_use_token = extract_auth_sub_token_from_url(get_full_url(request))
        request.session['authsub_token'] = single_use_token 
        return HttpResponseRedirect(redirect_to)
    else:
        next = get_full_url(request)
        auth_sub_url = get_auth_sub_url(next)
        return HttpResponseRedirect(auth_sub_url)
