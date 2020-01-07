from rest_framework import permissions
from .models import Membership


class IsOwnerOrAdminProject(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        membership = Membership.objects.filter(user=request.user).first()
        return membership.team == obj.team or request.user.is_staff
