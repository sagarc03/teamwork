from django.contrib import admin
from .models import (
        Team, Membership, Project, Task, ToDo
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

class ToDoAdmin(admin.ModelAdmin):
    list_display = ('todo', 'status')



admin.site.register(Team, TeamAdmin)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(ToDo, ToDoAdmin)
