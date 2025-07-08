from django_filters.rest_framework import FilterSet, ChoiceFilter
from users.models import User


class AdminUserFilter(FilterSet):
    role = ChoiceFilter(choices=User.roles)

    class Meta:
        model = User
        fields = ['role']