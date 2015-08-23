import os
from logging import getLogger

from django.http import (HttpResponseBadRequest, HttpResponseForbidden,
                         HttpResponseServerError, HttpResponse)
from django.utils.translation import ugettext_lazy as _
from django.utils.datastructures import MultiValueDict

from djangopypi import settings
from djangopypi.decorators import basic_auth
from djangopypi.models import Package, Release, Distribution, Classifier


log = getLogger('djangopypi')

ALREADY_EXISTS_FMT = _(
    "A file named '%s' already exists for %s. Please create a new release.")


@basic_auth
def register_or_upload(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Only post requests are supported')

    name = request.POST.get('name', None).strip()
    if not name:
        return HttpResponseBadRequest('No package name specified')

    try:
        package = Package.objects.get(name=name)
        log.debug('distutils - register_or_upload - Found package: %s' % name)
    except Package.DoesNotExist:
        package = Package.objects.create(name=name)
        package.owners.add(request.user)
        log.debug('distutils - register_or_upload - Created package: %s' % name)

    if (request.user not in package.owners.all() and
            request.user not in package.maintainers.all()):

        return HttpResponseForbidden('You are not an owner/maintainer of %s' % (package.name,))

    version = request.POST.get('version', None).strip()
    metadata_version = request.POST.get('metadata_version', None).strip()

    if not version or not metadata_version:
        return HttpResponseBadRequest('Release version and metadata version must be specified')

    if metadata_version not in settings.METADATA_FIELDS:
        return HttpResponseBadRequest('Metadata version must be one of: %s'
                                      (', '.join(settings.METADATA_FIELDS.keys()),))

    release, created = Release.objects.get_or_create(package=package,
                                                     version=version)
    if created:
        log.debug('distutils - register_or_upload - Created release: %s' % version)
    else:
        log.debug('distutils - register_or_upload - Found release: %s' % version)
    if (('classifiers' in request.POST or 'download_url' in request.POST) and
            metadata_version == '1.0'):
        metadata_version = '1.1'

    release.metadata_version = metadata_version

    fields = settings.METADATA_FIELDS[metadata_version]

    if 'classifiers' in request.POST:
        request.POST.setlist('classifier', request.POST.getlist('classifiers'))

    release.package_info = MultiValueDict(dict(filter(lambda t: t[0] in fields,
                                                      request.POST.iterlists())))

    for key, value in release.package_info.iterlists():
        release.package_info.setlist(key,
                                     filter(lambda v: v != 'UNKNOWN', value))

    release.save()
    if 'content' not in request.FILES:
        return HttpResponse('release registered')

    uploaded = request.FILES.get('content')

    for dist in release.distributions.all():
        if os.path.basename(dist.content.name) == uploaded.name:
            """ Need to add handling optionally deleting old and putting up new """
            return HttpResponseBadRequest('That file has already been uploaded...')

    md5_digest = request.POST.get('md5_digest', '').strip()

    try:
        new_obj = Distribution.objects.create(
            release=release,
            content=uploaded,
            filetype=request.POST.get('filetype', 'sdist').strip(),
            pyversion=request.POST.get('pyversion', '').strip(),
            uploader=request.user,
            comment=request.POST.get('comment', '').strip(),
            signature=request.POST.get('gpg_signature', '').strip(),
            md5_digest=md5_digest)

        from djangopypi.signals import get_hash
        my_digest = get_hash(new_obj)
        if my_digest != md5_digest:
            new_obj.md5_digest = my_digest
            new_obj.save()

    except Exception as e:
        log.exception('Failure when storing upload')
        log.exception(e.msg)
        return HttpResponseServerError('Failure when storing upload')

    return HttpResponse('upload accepted')


def list_classifiers(request, mimetype='text/plain'):
    response = HttpResponse(mimetype=mimetype)
    response.write(u'\n'.join(map(lambda c: c.name, Classifier.objects.all())))
    return response
