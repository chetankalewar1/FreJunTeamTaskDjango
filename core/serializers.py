from rest_framework import serializers
from core.models import Task, AssignTask


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class TaskReportSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = AssignTask
        fields = ("name", "member", "status")

    def get_name(self, obj):
        return obj.member.name

    def get_status(self, obj):
        return obj.task.status
