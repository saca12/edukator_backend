from rest_framework import serializers

from .models import OfflineContent


class OfflineContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflineContent
        fields = [
            "id",
            "student",
            "content_type",
            "related_entity_id",
            "local_file_path",
            "last_synced",
        ]
        read_only_fields = ["id", "student", "last_synced"]

