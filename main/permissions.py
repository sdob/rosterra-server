from django.http import Http404
from rest_framework import permissions

from models import Company

class IsManagerOrReadOnly(permissions.BasePermission):
    """Allow write access to managers when a company is in the mix."""
    def has_object_permission(self, request, view, obj):
        model_cls = getattr(view, 'model', None)
        queryset = getattr(view, 'queryset', None)
        if model_cls is None and queryset is not None:
            model_cls = queryset.model

        if request.method in permissions.SAFE_METHODS:
            return True
        # If it is meaningful to talk about the object being 'managed',
        # then call its is_managed_by method.
        if hasattr(obj, 'is_managed_by'):
            has_perm = obj.is_managed_by(request.user.profile)
            return has_perm
        # If something is not 'managed_by'-relevant, then return False
        return False

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Only allow write access if the object is foreign-keyed to
    the profile of the requesting user.
    """
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'user'):
            if request.method in permissions.SAFE_METHODS:
                return True
            return request.user == obj.user
        #print "no employee found"
        return False
