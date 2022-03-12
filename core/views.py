from django.contrib.auth import authenticate
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.tasks import send_mail_to
# from celery import signature
import pytz
import json
import uuid

from core.models import Team, TeamMember, AssignTask, Task, User

# Create your views here.
from core.serializers import TaskSerializer, TaskReportSerializer


class CreateTeamViewSet(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        if not request.user.is_leader:
            return Response({"success": False, "msg": "Failed to authenticate."}, status=status.HTTP_401_UNAUTHORIZED)

        team, is_created = Team.objects.get_or_create(name=request.data["team_name"])
        members = request.data["members"]

        for member in members:
            TeamMember(team=team, user_id=member).save()

        return Response({"success": True, "msg": "Team created successfully."})


class AvailabilityViewset(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        if not request.user.is_leader:
            return Response({"success": False, "msg": "Failed to authenticate."}, status=status.HTTP_401_UNAUTHORIZED)

        data = []
        members = TeamMember.objects.filter(team_id=request.GET["team_id"])
        for member in members:
            if AssignTask.objects.filter(member=member.user, task__status__in=[Task.IN_PROGRESS, Task.ASSIGNED]).exists():
                dicter = {member.user.name: False}
            else:
                dicter = {member.user.name: True}
            data.append(dicter)

        return Response({"success": True, "data": data})


class TaskViewset(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        if not self.request.user.is_leader:
            if len(self.request.data.keys()) > 1 or not self.request.data.get("status"):
                return Response({"success": False, "msg": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        t = self.get_serializer(instance, data=self.request.data, partial=True)
        if t.is_valid():
            t.save()
            return Response({"success": True, "msg": "Task Updated."})
        else:
            print(t.errors)
            return Response({"success": False, "msg": "Incorrect parameters."}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        self.request.data.update({"created_by": self.request.user.id})

        if not request.user.is_leader:
            return Response({"success": False, "msg": "Forbidden."}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            member = self.request.data["team_member"]
        except KeyError:
            return Response({"success": False, "msg": "Incorrect parameters."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if member available
        if AssignTask.objects.filter(member_id=member, task__status=Task.IN_PROGRESS).exists():
            return Response({"success": False, "msg": "Team member not available."}, status=status.HTTP_400_BAD_REQUEST)

        t = self.get_serializer(data=self.request.data)
        if t.is_valid():
            t = t.save()
            at = AssignTask(task=t, member_id=request.data["team_member"])
            at.save()

            # TODO: change to schedule
            send_mail_to.delay("Task deadline alert.", f"Task {t.name} is about hit the deadline",
                               [t.created_by.email, at.member.email])

            # # Schedule Email
            # task_s = signature(
            #     "send_email_to",
            # )
            # json_dicter = json.loads({"subject": "Task deadline alert.",
            #                           "message": f"Task {t.name} is about hit the deadline",
            #                           "receivers": [t.created_by.email, at.member.email]})
            # eta1 = t.end.astimezone(pytz.timezone(pytz.UTC))
            # task_id = str(uuid.uuid4())
            # task_s.apply_async(args=(json_dicter, task_id), eta=eta1, task_id=task_id)


            return Response({"success": True, "msg": "Team created successfully."})

        else:
            print(t.errors)
            return Response({"success": False, "msg": "Incorrect parameters."}, status=status.HTTP_400_BAD_REQUEST)


class StatusChangeReportViewset(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = AssignTask.objects.all()
    serializer_class = TaskReportSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset.filter(task__updated_at__date=self.request.GET.get("date"))
        return queryset

    def list(self, request, *args, **kwargs):
        if not request.user.is_leader:
            return Response({"success": False, "msg": "Forbidden."}, status=status.HTTP_401_UNAUTHORIZED)
        return super(StatusChangeReportViewset, self).list(request, *args, **kwargs)

