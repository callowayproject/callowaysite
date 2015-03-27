from django.db.models.query import Q
# from django.forms.models import inlineformset_factory
# from django.shortcuts import get_object_or_404, render_to_response
# from django.template import RequestContext

# from djangopypi.decorators import user_owns_package, user_maintains_package
from djangopypi.models import Package  # , Release
from djangopypi.forms import SimplePackageSearchForm

from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
# from django.views.generic.edit import CreateView, UpdateView


class PackageListView(ListView):
    template_name = 'package'
    model = Package
    context_object_name = 'package_list'


class SimpleIndexView(PackageListView):
    template_name = 'djangopypi/package_list_simple.html'


class PackageDetailView(DetailView):
    context_object_name = 'package'
    model = Package
    slug_field = 'name'
    slug_url_kwarg = 'package'

# def details(request, package, proxy_folder='pypi', **kwargs):
#     kwargs.setdefault('template_object_name', 'package')
#     kwargs.setdefault('queryset', Package.objects.all())
#     try:
#         return list_detail.object_detail(request, object_id=package, **kwargs)
#     except Http404, e:
#         if settings.DJANGOPYPI_PROXY_MISSING:
#             return HttpResponseRedirect('%s/%s/%s/' %
#                                         (settings.DJANGOPYPI_PROXY_BASE_URL.rstrip('/'),
#                                          proxy_folder,
#                                          package))
#         raise Http404(u'%s is not a registered package' % (package,))


class PackageSimpleDetailView(PackageDetailView):
    template_name = 'djangopypi/package_detail_simple.html'


class PackageDoapView(PackageDetailView):
    template_name = 'djangopypi/package_doap.xml'
    content_type = 'text/xml'


class PackageSearchView(PackageListView, FormView):
    form_class = SimplePackageSearchForm

    def form_valid(self, form):
        q = form.cleaned_data['query']
        self.queryset = self.get_queryset().filter(Q(name__contains=q) |
                                              Q(releases__package_info__contains=q)).distinct()
        return self.render_to_response()

# @user_owns_package()
# def manage(request, package, **kwargs):
#     kwargs['object_id'] = package
#     kwargs.setdefault('form_class', PackageForm)
#     kwargs.setdefault('template_name', 'djangopypi/package_manage.html')
#     kwargs.setdefault('template_object_name', 'package')

#     return create_update.update_object(request, **kwargs)

# @user_maintains_package()
# def manage_versions(request, package, **kwargs):
#     package = get_object_or_404(Package, name=package)
#     kwargs.setdefault('formset_factory_kwargs', {})
#     kwargs['formset_factory_kwargs'].setdefault('fields', ('hidden',))
#     kwargs['formset_factory_kwargs']['extra'] = 0

#     kwargs.setdefault('formset_factory', inlineformset_factory(Package, Release, **kwargs['formset_factory_kwargs']))
#     kwargs.setdefault('template_name', 'djangopypi/package_manage_versions.html')
#     kwargs.setdefault('template_object_name', 'package')
#     kwargs.setdefault('extra_context',{})
#     kwargs.setdefault('mimetype',settings.DEFAULT_CONTENT_TYPE)
#     kwargs['extra_context'][kwargs['template_object_name']] = package
#     kwargs.setdefault('formset_kwargs',{})
#     kwargs['formset_kwargs']['instance'] = package

#     if request.method == 'POST':
#         formset = kwargs['formset_factory'](data=request.POST, **kwargs['formset_kwargs'])
#         if formset.is_valid():
#             formset.save()
#             return create_update.redirect(kwargs.get('post_save_redirect', None),
#                                           package)

#     formset = kwargs['formset_factory'](**kwargs['formset_kwargs'])

#     kwargs['extra_context']['formset'] = formset

#     return render_to_response(kwargs['template_name'], kwargs['extra_context'],
#                               context_instance=RequestContext(request),
#                               mimetype=kwargs['mimetype'])
