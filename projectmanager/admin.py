from django.contrib import admin
from .models import Team, Membership

# Register your models here.


class TeamAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name',)


class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'team')


admin.site.register(Team, TeamAdmin)
admin.site.register(Membership, MembershipAdmin)
