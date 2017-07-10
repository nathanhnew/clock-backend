from rest_framework import permissions


class IsStaffOrTarget(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow user to list all users if staff
        return view.action == 'retrieve' or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # Allow logged in user to view their own Detials
        return request.user.is_staff or object == request.user
