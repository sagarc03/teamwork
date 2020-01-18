from django.contrib import admin
from .models import (
        Team, Membership, Project, Task
        )

# Register your models here.


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name',)


class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'team')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'endDate')


class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'startDate', 'endDate')



admin.site.register(Team, TeamAdmin)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
