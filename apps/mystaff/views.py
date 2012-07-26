from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from .models import MyStaffMember

def index(request, template_name='mystaff/index.html'):
    """
    The list of employees or staff members
    """
    return render_to_response(template_name,
                              {'staff': MyStaffMember.objects.active()},
                              context_instance=RequestContext(request))
