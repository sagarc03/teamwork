from django.contrib import admin
from .models import Team, Membership, Project

# Register your models here.


class TeamAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name',)


class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'team')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'endDate')


admin.site.register(Team, TeamAdmin)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(Project, ProjectAdmin)
