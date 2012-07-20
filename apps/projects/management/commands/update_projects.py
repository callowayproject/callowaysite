from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Update the projects from github"

    def handle(self, *args, **options):
        from pygithub3 import Github
        from projects.models import Project
        from django.conf import settings

        gh = Github(login=settings.GITHUB_USER, password=settings.GITHUB_PASSWORD)
        repos = gh.repos.list(user='callowayproject').all()

        for repo in repos:
            try:
                proj = Project.objects.get(external_id=repo.id)
                proj.name = repo.name
                proj.description = repo.description
                proj.url = repo.html_url
                proj.is_fork = repo.fork
                if repo.pushed_at:
                    proj.updated = repo.pushed_at
                else:
                    proj.updated = repo.updated_at
                proj.save()
            except Project.DoesNotExist:
                proj = Project(
                    name=repo.name,
                    description=repo.description,
                    code_url=repo.html_url,
                    is_fork=repo.fork,
                    external_id=repo.id,
                    project_type=1,
                    status=1
                )
                proj.save()
