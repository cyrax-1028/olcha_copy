from rest_framework.permissions import BasePermission
from datetime import timedelta
from django.utils.timezone import now


class DeleteProductPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE":
            return now() - obj.created_at <= timedelta(minutes=2)
        return True


class IsWeekdayPermission(BasePermission):
    def has_permission(self, request, view):
        today = now().weekday()
        return today in range(5)

