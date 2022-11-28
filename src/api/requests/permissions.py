from rest_framework import permissions

from request.constants import MANAGER_TYPE


class ManagerPermission(permissions.BasePermission):
    """
    Permission class focused on giving permission if the user is type manager
    """

    def has_permission(self, request, view):
        return request.user.type == MANAGER_TYPE
