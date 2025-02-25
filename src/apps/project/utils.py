def get_project_members_count(project):
    return project.members.count()


def get_user_projects(user):
    return user.projects.all()