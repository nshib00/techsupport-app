from rest_framework.serializers import ModelSerializer
from techsupport.common.mixins import XSSProtectionMixin


class BaseModelSerializer(XSSProtectionMixin, ModelSerializer):
    pass