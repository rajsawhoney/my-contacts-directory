from rest_framework import serializers

class MarkAsSpamViewSchema(serializers.Serializer):
    id = serializers.CharField(
        help_text="ID for the contact to mark as spam.", required=True)
    