from django.shortcuts import render_to_response
from django.template import RequestContext
from projects.models import Project


def project_list(request):
    """
    Return a list of projects grouped by project type
    """
    contentapps = Project.objects.filter(project_type=0).order_by('status', 'name')
    decoratorapps = Project.objects.filter(project_type=1).order_by('status', 'name')
    utilities = Project.objects.filter(project_type=2).order_by('status', 'name')
    pythonapps = Project.objects.filter(project_type=3).order_by('status', 'name')
    websites = Project.objects.filter(project_type=4).order_by('status', 'name')

    return render_to_response('project_list.html', {
            'contentapps': contentapps,
            'decoratorapps': decoratorapps,
            'utilities': utilities,
            'pythonapps': pythonapps,
            'websites': websites
        },
        context_instance=RequestContext(request)
    )
