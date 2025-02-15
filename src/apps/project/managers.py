from django.db import models


class ProjectQuerySet(models.QuerySet):

    def active(self):
        return self.filter(status='active')

    def completed(self):
        return self.filter(status='completed')

    def by_owner(self, user):
        return self.filter(owner=user)


class ProjectManager(models.Manager):

    def get_queryset(self):
        return ProjectQuerySet(self.model, using=self._db)

    def active_project(self):
        return self.get_queryset().active()

    def completed_projects(self):
        return self.get_queryset().completed()

    def user_projects(self, user):
        return self.get_queryset().filter(members__user=user)


class ProjectMemberManager(models.Manager):

        def is_member(self, project, user):
            return self.filter(project=project, user=user).exists()

        def get_user_roles(self, project, user):
            member = self.filter(project=project, user=user)
            return member.role if member else None